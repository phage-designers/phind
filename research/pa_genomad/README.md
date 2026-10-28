# *P. aeruginosa* geNomad prophage hits (Pa cohort)

Prophage/virus calls from **geNomad** over a 46,990-genome *Pseudomonas
aeruginosa* cohort. Source: `Pa_genomad_results.xlsx` (2 sheets), converted to
TSV and gzipped on 2026-10-28. This cohort is **disjoint** from the repo's
*E. coli* 26k set (0 accessions in common with `26k_ecoli_accession.txt` /
`all_valid_accessions.txt`).

## Files

| File | Rows (excl. header) | Size | Contents |
|---|---|---|---|
| `all_genomad_hits_complete.tsv.gz` | 864,767 | 14 MB | One row per geNomad hit: (genome, seq) |
| `pa_per_genome_summary.tsv.gz` | 46,990 | 490 KB | Rollup: one row per genome |
| `pa_list.tsv.gz` | 46,990 | 141 KB | Cohort accession list (`Genome` column) |

## Cohort composition

- 46,990 genomes: ~14.6k NCBI `GCF_*` assemblies + ~32.4k internal-style ids
  (e.g. `15043`, `16_538171` — provenance of these ids not yet documented here).
- 46,989 of 46,990 genomes have ≥1 hit; 46,914 have ≥1 `Provirus` topology call.
- Every genome has at least one hit with `virus_score >= 0.9`.

## Hits table column dictionary (geNomad `summary` output)

`Genome` (accession), `seq_name` (contig id; provirus calls carry
`|provirus_START_END`), `length` (bp), `topology` (`Provirus` /
`No terminal repeats` / other), `coordinates` (`NA` or `START-END` on the
contig), `n_genes`, `genetic_code`, `virus_score` (0–1 confidence),
`fdr`, `n_hallmarks` (marker genes), `marker_enrichment`, `taxonomy`
(semicolon ranks; trailing `;` = missing ranks).

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

## Usage

```sh
zcat pa_per_genome_summary.tsv.gz | column -t | head
zcat all_genomad_hits_complete.tsv.gz | awk -F'\t' '$1=="GCF_041355445.1"'
```
