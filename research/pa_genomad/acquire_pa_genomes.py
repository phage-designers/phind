#!/usr/bin/env python3
"""Acquire the public *P. aeruginosa* cohort as PanSN bgzip genome objects.

46,900 public accessions (32,308 GCA GenBank + 14,592 GCF RefSeq) from
research/pa_genomad/pa_public_accessions_all.txt. The 90 lab genomes are NOT
here (pending SafeSend ZIP).

Reuses the proven helpers from ntm/v3/scripts/acquire_v3_genomes.py:
contig renaming to PanSN `{acc}#1#{contig}`, bgzip + samtools faidx + bgzi -r.

Resume-first: a genome is skipped when <acc>.pansn.fa.gz.fai exists and is
non-empty. Source chain per accession: ENA fasta API -> NCBI datasets ZIP.

Output: $NVME/pa/genomes/canonical_objects/<acc>/<acc>.pansn.fa.gz{,.fai,.gzi}
        $NVME/pa/genomes/acquisition_manifest.tsv
"""
from __future__ import annotations
import argparse, csv, io, os, sys, threading, time, urllib.parse, zipfile
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

REPO = "/home/erikg/phind"
sys.path.insert(0, f"{REPO}/ntm/v3/scripts")
from acquire_v3_genomes import (  # noqa: E402
    DATASETS_BASE, ENA_FASTA_BASE, RateLimiter, gunzip, http_get,
    rename_fasta_to_pansn, write_bgzip_faidx,
)

NV = "/mnt/nvme3n1/erikg/phind-genome-work"
OUT = f"{NV}/pa/genomes/canonical_objects"
MANIFEST = f"{NV}/pa/genomes/acquisition_manifest.tsv"
LIM = RateLimiter(8.0)
LOCK = threading.Lock()


def fetch(acc: str) -> tuple[bytes, str]:
    errs = []
    try:
        return gunzip(http_get(ENA_FASTA_BASE.format(acc=acc), LIM)), "ena"
    except Exception as e:  # noqa: BLE001
        errs.append(f"ena:{e}")
    try:
        q = urllib.parse.urlencode(
            {"include_annotation_type": ["GENOME_FASTA"], "filename": f"{acc}.zip"},
            doseq=True)
        data = http_get(DATASETS_BASE.format(acc=acc) + "?" + q, LIM)
        with zipfile.ZipFile(io.BytesIO(data)) as zf:
            m = next((n for n in zf.namelist() if n.endswith("_genomic.fna")), None)
            if m is None:
                raise RuntimeError("no _genomic.fna")
            return zf.read(m), "datasets"
    except Exception as e:  # noqa: BLE001
        errs.append(f"datasets:{e}")
    raise RuntimeError("; ".join(errs))


def one(acc: str) -> dict:
    d = Path(OUT) / acc
    fai = d / f"{acc}.pansn.fa.gz.fai"
    gz = d / f"{acc}.pansn.fa.gz"
    rec = {"accession": acc, "status": "", "source": "", "contigs": "", "total_bp": "", "error": ""}
    if fai.exists() and fai.stat().st_size > 0 and gz.exists() and gz.stat().st_size > 0:
        rec["status"] = "reused"
        return rec
    try:
        fa, src = fetch(acc)
        pansn = rename_fasta_to_pansn(fa, acc)
        d.mkdir(parents=True, exist_ok=True)
        log = {}
        stats = write_bgzip_faidx(pansn, d, acc, log)
        rec.update(status="ok", source=src, contigs=stats["contigs"], total_bp=stats["total_bp"])
    except Exception as e:  # noqa: BLE001
        rec.update(status="fail", error=str(e)[:200])
    return rec


def main() -> int:
    global OUT
    ap = argparse.ArgumentParser()
    ap.add_argument("--accessions", default=f"{REPO}/research/pa_genomad/pa_public_accessions_all.txt")
    ap.add_argument("--out", default=OUT)
    ap.add_argument("--jobs", type=int, default=16)
    ap.add_argument("--limit", type=int, default=None)
    ap.add_argument("--accession", action="append")
    args = ap.parse_args()
    OUT = args.out
    manifest = os.path.join(os.path.dirname(OUT.rstrip("/")), "acquisition_manifest.tsv")
    os.makedirs(OUT, exist_ok=True)
    os.makedirs(os.path.dirname(manifest), exist_ok=True)

    accs = args.accession or [l.strip() for l in open(args.accessions) if l.strip()]
    if args.limit:
        accs = accs[: args.limit]
    print(f"acquiring {len(accs)} public accessions -> {OUT} (jobs={args.jobs})", flush=True)

    results, done, ok, reused, failed = [], 0, 0, 0, 0
    t0 = time.time()
    with ThreadPoolExecutor(max_workers=max(1, args.jobs)) as ex:
        futs = {ex.submit(one, a): a for a in accs}
        for f in as_completed(futs):
            r = f.result()
            results.append(r)
            done += 1
            if r["status"] == "ok": ok += 1
            elif r["status"] == "reused": reused += 1
            else: failed += 1
            if done % 200 == 0:
                rate = done / max(1e-9, time.time() - t0)
                print(f"  {done}/{len(accs)}  ok={ok} reused={reused} failed={failed}  "
                      f"({rate:.1f}/s, eta {int((len(accs)-done)/max(rate,1e-9))}s)", flush=True)

    with open(manifest, "w", newline="") as fh:
        w = csv.DictWriter(fh, fieldnames=["accession", "status", "source", "contigs", "total_bp", "error"],
                           delimiter="\t")
        w.writeheader()
        for r in sorted(results, key=lambda r: r["accession"]):
            w.writerow(r)
    print(f"ACQUISITION_DONE ok={ok} reused={reused} failed={failed} total={len(results)} -> {manifest}", flush=True)
    return 0 if failed == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
