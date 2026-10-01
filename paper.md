# The D'Agapeyeff Column-14 Anomaly: Statistical Confirmation and Negative Semantic Results

**A characterization and replication-plus-quantification note — not a solution attempt.**

Date: 2026-10-01
Authors: Chief & Mentor (independent replication), with thanks to Nick Pelling for the original observation.

## Abstract

The D'Agapeyeff cipher (1939, 196 digit-pairs) contains a genuine anomaly: when laid out as a 14×14 grid, the final column concentrates the rarest symbols far beyond chance (p≈9e-10). This observation was first published by Nick Pelling in January 2014 as a blog post; Pelling did not include a significance test. We independently confirm the anomaly with quantified statistics, a pre-registered permutation null (10,000 draws), and confirmation across four frozen data variants. The cipher's main body (182 pairs, 13 symbols) is flat — flatter than all 240 shuffled-English controls — and shows no bigram-level structure (mutual information, conditional entropy, repeat rates, and bigram chi-square all at null). Four pre-registered semantic readings of column 14 (embedded date, geographic coordinate, row checksum, positional trend) all returned negative against the null. Two of the four reading tests were weak by construction (binary scores); the checksum and positional tests, and the bigram discriminator, carried real falsification risk. Per a pre-registered cap rule, column 14 is declared **structurally distinct, semantically unresolved**. No solution is claimed. All code, seeds, and the self-test harness (including a regression test for a historical scoring bug) are published alongside this note for reproduction.

## 1. The object

Alexander D'Agapeyeff's *Codes and Ciphers* (Oxford University Press, 1939) contains an unsolved challenge cipher: 395 digits arranged as 196 pairs, 18 distinct pairs. We work from a frozen transcription (variant B), laid out as printed in 14 rows of 14 pairs. Pair #98 (row 7, column 14) is the lone `04`.

## 2. Prior work and attribution

The column-14 observation is not ours. Nick Pelling documented it on 27 January 2014 ("Why I think the d'Agapeyeff cipher is diagonally transposed," Cipher Mysteries): "many of its oddities are to be found in the final right hand column," flagging the `04` and the concentration of `92` symbols occurring only in that column. Pelling's post — a blog post, not a paper — proposed a diagonal-transposition theory and included letter-frequency counts, but no significance test of the column concentration. Our split-half test does not support the diagonal-transposition hypothesis; we attribute the theory to Pelling and the test to ourselves, without claiming he was wrong — he sketched an idea, we measured one specific prediction of it.

A second independent effort is active: Tim Marland's 2026 research program lists "Column-14-stripped" analysis among its phases. We publish first and note it here.

On the frequently repeated claim that D'Agapeyeff "forgot" his own method: we could locate no primary source. The trail goes cold at David Shulman, "The D'Agapeyeff Cryptogram: A Challenge," *The Cryptogram*, April/May 1952 (print-only, not digitized). Every modern retelling hedges or cites nothing. We treat this as unverified lore; it carries no argument in this note.

## 3. Results

### 3.1 The body is flat (confirmation)

The 182-pair body (columns 1–13) uses 13 symbols with near-perfect evenness. Against 240 shuffled-English controls, the real body ranked 0th in lumpiness (p<0.004): "plain English with columns shuffled" is excluded as the body construction. Unigram chi-square against uniform-13 is 8.71 (df=12), inside the i.i.d. null 95% band [4.71, 22.14] — ordinary random-draw evenness, not deliberate flattening.

### 3.2 The body has no bigram structure (new)

Mutual information between adjacent pairs, conditional entropy, length-2 and length-3 repeat rates, and the 13×13 bigram chi-square against independence: all inside null 95% bands (500 shuffled + 500 i.i.d. nulls, fresh seeds, code and seeds hashed before the run). 0 of 5 structure indicators. The discriminator was validated to have power: on a synthetic homophonic control it flagged structure (MI 0.468 vs null [0.190, 0.301]); on i.i.d. controls it held at null 49/50. Conclusion: the body is consistent with i.i.d. filler. The homophonic-English hypothesis is not supported.

Note on labeling: the unigram flatness (§3.1) predates this test and is confirmatory; the bigram-level null is the new information.

### 3.3 The column-14 anomaly is real and quantified (confirmation + quantification)

All 8 appearances of the 5 rarest pairs fall in column 14 (p≈9e-10). Column 14 uses a different symbol set from the body (including the 9x pairs 92×3, 93×2, 94). The concentration survives a split-half test (5/5 in both halves, Holm-significant). Confirmed across all four frozen transcription variants.

### 3.4 Semantic readings of column 14: negative (new, under cap rule)

Four reading types were pre-registered with exact formats, a 10,000-permutation null, and a Bonferroni-corrected bar (p<0.0125), hashed before measurement:

| Test | Format | Real score | p | Hit? |
|---|---|---|---|---|
| R1 embedded date | valid YYYYMMDD, 1850–1939, contiguous | 0 | 1.0 | No |
| R2 coordinate | lat/lon DDDMMSS, valid ranges | 0 | 1.0 | No |
| R3 row checksum | Σ(row pairs) mod 100 == col-14 pair | 1/14 | 0.275 | No |
| R4 positional trend | |Spearman rho| vs row index | 0.14 | 0.629 | No |

Per the pre-registered cap rule: **column 14 is structurally distinct, semantically unresolved.** No further candidates will be tested under this rule.

*Methods honesty note:* R1 and R2 were weak tests by construction (binary scores; a real score of 0 yields p=1.0 mechanically). Their "confirmed" predictions are low-information. R3, R4, and the §3.2 discriminator carried genuine falsification risk. The prediction sweep is documented as a methods appendix (Appendix A), not as the finding.

### 3.5 Dead hypotheses

- Monoalphabetic substitution + width-14 columnar transposition: dead at n=182 under pre-registration (scorer test failed all three bars; the §3.1 bag result independently undercuts its premise).
- Split-at-`04` separator: null (halves homogeneous).
- Column-4 structure: weak (3% of 5,000 shuffles reach it); not built on.

## 4. What this is not

Not a solution. Not a decryption. No solver was run on the real cipher in this work, and none is proposed. The full solve remains a low-probability event; this note deliberately prices it at zero and publishes anyway.

## 5. Reproduction

The harness (`harness/run_selftest.py`) validates the full apparatus in one command: frozen-data integrity, the scorer suite including a regression test for the historical zip-count scoring bug (an accuracy formula that counted zipped pairs without checking equality, scoring every column order 1.00 — it voided an earlier round of results and must never reappear undetected), the discriminator power check, and column-14 separation. 12/12 green at publication. All analysis code is hashed in the pre-registration documents; seeds were drawn from `os.urandom` after each code freeze.

## References

- D'Agapeyeff, A. *Codes and Ciphers.* Oxford University Press, 1939.
- Pelling, N. "Why I think the d'Agapeyeff cipher is diagonally transposed..." Cipher Mysteries, 27 Jan 2014. https://ciphermysteries.com/2014/01/27/think-dagapeyeff-cipher-diagonally-transposed
- Shulman, D. (as AB STRUSE). "The D'Agapeyeff Cryptogram: A Challenge." *The Cryptogram*, Apr/May 1952, pp. 39–40, 46.
- Marland, T. D'Agapeyeff research program, 2026. https://www.dagapeyeffresearch.com/

## Appendix A: pre-registered predictions and audit

(Bigam test: `build/PRE_REG_BIGRAM.md`, code `bigram_test.py` bf9f8b9d, seeds af0b4544. Column-14 readings: `build/PRE_REG_COL14_READINGS.md`, code `score_readings.py` aced6a91, seeds 0744eac5.)

Predictions P-R1–P-R4 (all "no hit") and P-CAP ("structurally distinct, semantically unresolved") were confirmed. Audit: R1/R2 near-certain (weak tests, labeled as such in §3.4); R3/R4 genuinely falsifiable; bigram unigram-level confirmatory, bigram-level new. No prediction is presented as evidence beyond its actual risk. Prior knowledge was labeled already-known vs new before each run; no edits were made after any hash.
