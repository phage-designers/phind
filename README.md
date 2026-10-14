# PHIND

## Reconstructing phage genome candidates from bacterial sequencing data

PHIND uses **pangenome graphs to reconstruct candidate phage genomes from
prophages**, the phage sequences embedded in bacterial genomes. Its value is to
turn the abundant, often fragmentary record of phages in bacterial sequencing
data into explicit sequence hypotheses for phage discovery, comparative
genomics, and experimental testing.

A single bacterial genome may preserve only part of a phage. Related prophages
across a population preserve overlapping sequence blocks and different genome
arrangements. PHIND models that shared structure, then constructs candidate paths
weighted by block frequency and adjacency evidence. The graph acts as a discrete model of genome
structure: homologous blocks form a vocabulary, and their observed order and
frequency inform candidate genomes.

**The pipeline has been applied to two datasets:** an *E. coli* collection
yielding **479 reconstructed candidates plus 106 observed singletons**, and a
Mycobacteriaceae collection yielding **893 reconstructed fragments plus 411
observed singletons** in the current NTM v3.1 release.

## How it works

1. **Find related prophages.** Extract prophage sequences from bacterial
   assemblies and group them into sequence-similar clades using MASH.
2. **Model shared sequence and structure.** Align within clades with
   `allwave`, segment the alignments, and use `impg` to identify homologous
   blocks. Block occurrence and adjacency define the reconstruction graph.
3. **Reconstruct candidate sequences.** Sample paths through the graph and
   infer a sequence within each block. The typical-genome mode, called **ML**
   in the releases, uses majority-rule block consensus; the **ancestral**
   mode uses per-block neighbor-joining trees and Fitch parsimony.
4. **Check and prioritize.** Retain source provenance, annotate phage-related
   genes, estimate completeness and contamination, inspect path structure,
   and test selected modules and junctions against external sequence data.

The current NTM v3.1 method restricts paths to observed adjacencies and uses
per-clade length targets and natural termini. The earlier *E. coli* release
uses adjacency-weighted sampling with a length budget.

## What has been done

### *E. coli*: population-scale reconstruction and external sequence support

- **Input:** 132,393 prophage elements from 26,232 assemblies. Reconstruction
  used 19,638 members of the selected communities, resolved into 585 tight
  clades.
- **Release:** 479 reconstructed candidates and 106 singleton pass-through
  sequences. Median length is 45.2 kb; 78 entries are shorter than 10 kb.
  [Release and methods](research/ml_phage_genomes/RELEASE.md) ·
  [Clade definitions](research/clades/README.md) ·
  [Sequences and metadata](export/phage_ecoli26k/)
- **Phage-consistent annotation:** across all 585 entries, Pharokka/PHROG
  detects terminase in 364, capsid in 331, and tail proteins in 446.
  CheckV classifies 268 as high-quality and 128 as medium-quality; 165 are
  low-quality and 24 undetermined.
  [Per-sequence annotation and QC](research/phage_annotation/per_genome_annotation_qc.tsv)
- **External corroboration:** a preregistered panel from 24 reconstructed
  clades was screened against 15,105 public Logan assemblies. It produced
  22,625 alignment-confirmed bait/accession pairs across 10,389 accessions
  from 510 BioProjects. **39 of 59 reconstructed junction baits** had confirmed
  hits; shuffled negative controls had none. The screen took about 4.8 hours,
  including metadata preparation.
  [Panel design](research/ecoli_bait/panel/README.md) ·
  [Screen report and controls](research/ecoli_screen/REPORT.md)

This screen supports specific reconstructed modules and junctions. It is not a
whole-genome validation of all 585 entries; related isolates can also contribute
multiple accessions.

### Mycobacteriaceae / NTM v3.1: reconstruction with explicit fragment and path QC

- **Input:** 36,857 prophages from a union cohort of 34,163 Mycobacteriaceae
  genomes: 26,890 NTM and 7,273 *M. tuberculosis* complex genomes.
- **Current release:** 1,304 sequences comprising 893 reconstructed fragments
  and 411 observed singletons, plus 893 ancestral-state alternatives.
  Median released-sequence length is 14.3 kb.
- **Quality:** 124 of 1,304 entries are CheckV high-quality. Median estimated
  completeness is 28.4% among the 1,026 entries with an estimate.
  Of the 893 reconstructed paths, 408 follow a single member's partition
  order and 485 mix genome contexts. Matching a member's block order does
  not establish an identical nucleotide sequence or biological function.
- **Reference comparison:** 86.7% of entries have no close nucleotide
  relative (MASH distance > 0.30) among 6,060 curated actinobacteriophages.
  The reference is biased toward fast-growing-host isolates; protein-level
  comparison is still needed before claiming biological novelty.

[Current sequences and trust manifest](export/phage_ntm_v31/) ·
[Method comparison and path audit](ntm/v3.1/REPORT.md) ·
[Reference-comparison controls and caveats](ntm/v3.1/NOVELTY.md)

**Use v3.1 for current NTM results.** It supersedes v3 after a mosaic
reconstruction defect was identified: combining many blocks inflated both
sequence length and CheckV completeness. The correction demonstrates why annotation and completeness must
be assessed alongside genome structure.

## What the evidence establishes

PHIND has produced reproducible, population-derived candidate sequences with
phage-consistent annotations and, for a selected *E. coli* panel, external
support for reconstructed sequence junctions. It provides a way to prioritize
phage lineages and sequence hypotheses from existing sequencing collections.

Whole-genome reconstruction accuracy, infectivity, host range, safety, and
clinical efficacy remain unvalidated by these results. Annotation, reference
similarity, and assembly matches are computational evidence; experimental
recovery and functional testing are still required.

## Code, data, and reproducibility

- Core reconstruction: [`scripts/traverse_partitions.py`](scripts/traverse_partitions.py)
  and [tests](scripts/test_traverse_partitions.py)
- *E. coli* build commands, manifests, and data requirements:
  [clade pipeline](research/clades/README.md) and
  [release](research/ml_phage_genomes/RELEASE.md)
- NTM v3.1 drivers, analyses, and remaining work:
  [method index](ntm/v3.1/README.md)
- Downloadable sequence exports:
  [*E. coli*](export/phage_ecoli26k/) and [NTM v3.1](export/phage_ntm_v31/)
- [Historical operational README](docs/history/README-pre-overview-2026-10-14.md):
  preserved commands, recovery notes, and the earlier development plan

Release FASTAs and metadata are available in the export directories. Large
source assemblies and derived alignments are not all stored in Git; follow
the dataset-specific instructions and manifests before attempting a full rerun.
