All artifacts read; every number checked. Report follows.

# Review: PHIND top-level README (2026-10-15)

**Verdict: OK with notes.** Every quantitative claim matches its artifact (table below). The problems are editorial: a mixed-purpose heading, method text placed before results, intra-file number duplication, and three sentences of incident-report register.

## 1. Structure

The cold-arrival order is nearly right: title → value proposition → current-release headline is good. Two defects:

- **"How it works" interrupts the evidence.** A reader who just read "893 + 411, median 14.3 kb" wants the *details of those results* next, not four methodology steps. Move `## How it works` to **after** `## What has been done` (rename that to `## Results`), so the order becomes: headline → results → how → scope → code.
- **Load-bearing content below the fold.** The v3-withdrawal notice ("**Use v3.1 for current NTM results.** It supersedes v3 after a mosaic reconstruction defect…", lines ~96–100) sits at the *end* of the NTM subsection, but `export/phage_ntm_v3/` still exists on disk. Anyone grabbing v3 FASTAs must see this immediately. Promote it to the start of the NTM subsection, and add one clause to the top blurb: "It supersedes the withdrawn v3 catalog."

## 2. The heading "What the evidence establishes"

It earns its content but not its form: it fuses a genuine methodological result, a product summary, and limitations into one grab-bag. **Split it**: the methodological result *is* the v3.1 story and belongs inside the NTM subsection, merged with the existing "Use v3.1" paragraph. What remains becomes a short, honest closing section.

**Exact replacement.** Delete `## What the evidence establishes` (all three paragraphs). Replace the paragraph beginning "**Use v3.1 for current NTM results.**" with:

> **Use v3.1; the v3 ML catalog is withdrawn.** v3's walk only *favoured* observed adjacencies and accumulated blocks to a length budget, and CheckV scored the resulting mosaics near-complete, because concatenating every common block includes every marker gene — completeness rose monotonically with the length-to-expected ratio. v3.1 restricts paths to observed adjacencies, terminates at natural termini, and targets marker-derived genome lengths: median length falls from ~2.7× to ~1.0× expected, and completeness falls with it. The general lesson: annotation coverage and sequence plausibility do not establish a reconstructed genome — **the order of genomic blocks is independently informative and must be modelled and reported as such.**

Then insert before `## Code, data, and reproducibility`:

> ## Scope and limitations
>
> PHIND produces reproducible, population-derived candidate sequences with per-sequence provenance and phage-consistent annotations, plus external confirmation of reconstructed junctions for a selected *E. coli* panel. It does not establish whole-genome reconstruction accuracy, infectivity, host range, safety, or clinical efficacy: annotation, reference similarity, and assembly matches are computational evidence; experimental recovery and functional testing remain required.

## 3. Claim/evidence alignment

See the table. All numbers **match**. Two wording caveats, not mismatches: (a) "1,304 sequences … **reconstructed** from 36,857 prophages" — the 411 singletons are *observed pass-throughs*, not reconstructions; write "derived from". (b) "Matching a member's block order does not establish an identical nucleotide sequence" is correct and well-placed.

| Claim in README | Artifact, expected | Observed | Match |
|---|---|---|---|
| E. coli 479 reconstructed + 106 singletons | `research/ml_phage_genomes/RELEASE.md`: 585 incl. 106 singletons | 479+106 | ✓ |
| 132,393 prophages / 26,232 assemblies | same + `export/phage_ecoli26k/README.md` | same | ✓ |
| 39/59 junction baits confirmed | `research/ecoli_screen/REPORT.md` lines 27, 107 | same | ✓ |
| 22,625 pairs / 10,389 accessions / 510 BioProjects / 15,105 assemblies / ~4.8 h | `ecoli_screen/REPORT.md` §1, §4 | same | ✓ |
| Terminase 364 / capsid 331 / tail 446 | recomputed from `research/phage_annotation/per_genome_annotation_qc.tsv` (62.2% / 56.6% / 76.2% of 585) | same | ✓ |
| CheckV 268 HQ / 128 med / 165 low / 24 undet. (E. coli) | recomputed from same TSV | same | ✓ |
| NTM 893 + 411 = 1,304; 893 ancestral | `ntm/v3.1/REPORT.md`, `ntm/v3/RELEASE.md`, export README | same | ✓ |
| Median 14.3 kb | export README: 14,324 bp | 14.3 | ✓ |
| 124 of 1,304 CheckV high-quality | export README QC table | same | ✓ |
| Median completeness 28.4% among 1,026 with an estimate | export: 28.4%, 278 not-determined → 1,026 | same | ✓ |
| 408 single-member / 485 mixed | REPORT: 408/893 = 45.7% → 485 chimeric | same | ✓ |
| 86.7% no relative within MASH 0.30 of 6,060 | `NOVELTY.md`: 1,130/1,304 | same | ✓ |
| ~2.7× → ~1.0× length; monotone completeness | REPORT A/B table, v3/RELEASE | same | ✓ |
| 697/1,304 fallback target | REPORT "Remaining lever" | same | ✓ |

## 4. Redundancy and drift risk

The README restates numbers that already live in `ntm/v3.1/REPORT.md` and `export/phage_ntm_v31/README.md` — acceptable for a landing page — but it also **repeats numbers within itself**: 893/411, median 14.3 kb, and 408/485 each appear both in the top blurb and in the NTM body section. On a v3.2 those five figures can disagree *inside one file*. Fix: keep numbers only in the body; slim the blurb to "1,304 candidate fragments (median 14.3 kb) — details below."

## 5. Tone

"Current release / Earlier" is clear but undated; add dates (NTM v3.1: 2026-10-07; E. coli: 2026-08-06). The methodological finding mostly reads as a real result; three weak sentences:

1. "**The correction demonstrates why annotation and completeness must be assessed alongside genome structure.**" → "The revision shows that annotation and completeness metrics can actively reward a mosaic: genome structure must be assessed in its own right."
2. "…**removed the defect** — length fell from roughly 2.7x to roughly 1.0x expected, and completeness **dropped to its honest value**." → "…brought median length from ~2.7× to ~1.0× the expected genome length, with completeness falling accordingly (median 28.4%)."
3. "Remaining work on this dataset: 697 of 1,304 clades use a fragment-length fallback target that under-estimates genome length, **which is the clearest route to recovering additional completeness**." (dangling "which") → "…a fragment-length fallback target ~22% below the marker-based expected length; re-targeting those clades in a second pass is the clearest route to higher completeness."

## 6. Missing (4 items)

1. No triage recipe for users: the export README's "How to pick fragments" (`chimerism_verdict`, `length_ratio_vs_target`, `checkv_completeness` filters) is the most actionable content in the repo and the root README never points to it.
2. No host composition: 76% of prophages come from *Mycobacteroides abscessus* (NOVELTY.md) — the first thing a phage biologist asks.
3. No release dates or version identifiers for either catalog.
4. No data-access/licensing statement: Logan accessions carry access restrictions, and a program officer needs to know what can be redistributed.

## Prioritized edits

1. Split "What the evidence establishes" per §2 (exact text above); promote the v3-withdrawal notice to the top of the NTM subsection.
2. Move "How it works" after Results; rename "What has been done" → "Results".
3. De-duplicate the blurb numbers per §4.
4. Apply the three §5 rewrites; change "reconstructed from 36,857 prophages" → "derived from"; add release dates.
5. Add a "Getting the sequences" pointer (one line to `export/phage_ntm_v31/#how-to-pick-fragments`) and the *M. abscessus* host-composition sentence.