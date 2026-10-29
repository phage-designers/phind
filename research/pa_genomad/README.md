# *P. aeruginosa* geNomad prophage hits (Pa cohort)

Prophage/virus calls from **geNomad** over a **46,990-genome** *Pseudomonas
aeruginosa* cohort. Source: `Pa_genomad_results.xlsx` (2 sheets), converted to
TSV and gzipped 2026-10-28. The cohort is **disjoint** from the repo's *E. coli*
26k set (0 accessions in common).

## Cohort composition — corrected 2026-11-05

The genome ids are **overwhelmingly public NCBI accessions**, not internal ids:

| id namespace | genomes | hits | status |
|---|---:|---:|---|
| `GCA_<9 digits>.<ver>` (GenBank) | **32,308** | 541,853 | public, downloadable |
| `GCF_<9 digits>.<ver>` (RefSeq) | **14,592** | 320,941 | public, downloadable |
| internal / lab (`15043`, `16_538171`, `FBPa_*`, `PID_*`, `Pa_old`, …) | **90** | ~836 | pending collaborator delivery |

- **There are no GCA/GCF twin pairs** in this cohort: the 46,900 public numeric
  assembly ids are held exactly once, as either `GCA` or `GCF`.
- An earlier version of this README described the 32,308 non-GCF entries as
  "internal-style ids … provenance not yet documented". **That was wrong** — they
  are ordinary GenBank `GCA_` accessions, resolvable and downloadable from NCBI/ENA.
- The collaborator reports **93** lab genomes; the summary table contains **90**.
  The 3-genome difference is **unreconciled** and should be resolved when the
  SafeSend ZIP arrives.

### Accession lists

| file | contents |
|---|---|
| `pa_public_accessions_all.txt` | **46,900** — the correct public set (`GCA_` ∪ `GCF_`) |
| `pa_lab_genomes_pending.txt` | **90** — lab ids awaiting the SafeSend ZIP |
| `pa_public_accessions.txt` | *legacy, superseded:* 14,592 `GCF_`-only. RefSeq-only, so it silently drops 32,308 public GenBank assemblies. Use `pa_public_accessions_all.txt`. |

## Files

| File | Rows (excl. header) | Contents |
|---|---:|---|
| `all_genomad_hits_complete.tsv.gz` | 864,767 | one row per geNomad hit — **the whole cohort** |
| `all_genomad_hits_public.tsv.gz` | **320,941** | **`GCF_` genomes only** (RefSeq); not "the public subset" |
| `pa_per_genome_summary.tsv.gz` | 46,990 | rollup, one row per genome |
| `pa_list.tsv.gz` | 46,990 | cohort accession list (`Genome` column) |

> **Warning — `all_genomad_hits_public.tsv.gz` is RefSeq-only.** It contains
> 320,941 of the 864,767 hits because it was filtered on `GCF_` rather than on
> "public". Use `all_genomad_hits_complete.tsv.gz` for the full cohort.

> **Data-quality note — stray header mid-file.** `pa_per_genome_summary.tsv.gz`
> has **no header on line 1**; a header row (`Genome n_hits n_provirus …`) sits at
> **line 46,930**, because the XLSX→TSV conversion concatenated two sheets and
> dropped only the first sheet's header. Parsers must skip any row whose second
> field is non-numeric (rows 1–46,929 are sheet 1, rows 46,931–46,991 are sheet 2).
> `pa_list.tsv.gz` should be preferred for the accession list.

## Dataset shape (46,990 genomes)

- 46,989 of 46,990 genomes have ≥1 hit; 46,914 have ≥1 `Provirus` topology call.
- Every genome has at least one hit with `virus_score >= 0.9`.
- Per genome: `n_hits` median **10** (mean 18.4, max 1,452); `n_provirus` median **4**
  (mean 4.8, max 20); `n_caudoviricetes` median 5.
- Longest hit per genome: median **44.5 kb**; **92.6%** of genomes have a ≥20 kb hit
  and only 6 have a longest hit <5 kb — i.e. these are phage-scale calls, not noise.

## Hits table column dictionary (geNomad `summary` output)

`Genome` (accession), `seq_name` (contig id; provirus calls carry
`|provirus_START_END`), `length` (bp), `topology` (`Provirus` /
`No terminal repeats` / other), `coordinates` (`NA` or `START-END` on the contig),
`n_genes`, `genetic_code`, `virus_score` (0–1 confidence), `fdr`, `n_hallmarks`
(marker genes), `marker_enrichment`, `taxonomy` (semicolon ranks; trailing `;` =
missing ranks).

## Taxonomy snapshot (hits rows)

| Rank 1–4 (kingdom;phylum) | hits |
|---|---:|
| Viruses;Duplodnaviria;…;Uroviricota (Caudoviricetes) | 452,974 |
| Unclassified | 332,332 |
| Viruses;Monodnaviria;…;Hofneiviricota | 78,927 |
| Viruses;Varidnaviria;…;Nucleocytoviricota | 268 |
| Viruses;Monodnaviria;…;Phixviricota | 126 |
| other (Riboviria, Preplasmiviricota, …) | ~140 |

## Per-genome summary columns

`Genome`, `n_hits`, `n_provirus`, `n_caudoviricetes`, `n_hallmark1`
(hits with ≥1 hallmark), `max_virus_score`, `max_len_kb`, `total_hit_kb`.

## Genome acquisition

`acquire_pa_genomes.py` fetches the 46,900 public accessions as **PanSN bgzip**
objects, matching the NTM convention:

```
$NVME/pa/genomes/canonical_objects/<acc>/<acc>.pansn.fa.gz{,.fai,.gzi}
$NVME/pa/genomes/acquisition_manifest.tsv     # per-accession status/source/contigs/bp
```

```sh
python3 research/pa_genomad/acquire_pa_genomes.py --jobs 48
# resume-first: skips accessions whose .fai already exists and is non-empty
```

- contigs are renamed to PanSN `{acc}#1#{contig}`, so the `.fai` bare name equals
  geNomad's `seq_name` and the hit coordinates map directly onto the object
  (verified on GCA_000412735.1, GCA_000505965.1, GCA_000506085.1).
- source chain: ENA fasta API → NCBI datasets ZIP.
- ~2 MB per genome bgzipped; ~94 GB for the full public set.

### Acquisition result (2026-11-06)

| | |
|---|---|
| public accessions attempted | 46,900 |
| **acquired** | **46,899 (99.998%)** |
| unobtainable | **1** — `GCF_030224345.1` |
| output | 83 GB on disk, **316.7 Gbp**, `acquisition_manifest.tsv` |

`GCF_030224345.1` (7.0 Mb, Contig, Loyola University Chicago, "Genomic Catalog of
Human Bladder Bacteria") is **`assemblyStatus: suppressed` at NCBI**. Suppressed
assemblies serve no sequence: the datasets ZIP contains only metadata, and its
paired GenBank twin `GCA_030224345.1` is likewise unavailable. If a replacement
assembly appears for BioSample SAMN34998785, add it and re-run (resume-first).

Coordinate interface verified at scale: **1,412/1,412 geNomad `seq_name`s resolved**
in the `.fai` bare names across a random 300-genome sample (100%).

## Usage

```sh
zcat pa_per_genome_summary.tsv.gz | column -t | head
zcat all_genomad_hits_complete.tsv.gz | awk -F'\t' '$1=="GCF_041355445.1"'
```
