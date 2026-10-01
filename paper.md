# The D'Agapeyeff Column-14 Anomaly: Statistical Confirmation and Negative Semantic Results

**A characterization and replication-plus-quantification note — not a solution attempt.**

Date: 2026-10-01
Authors: Chief & Mentor (independent replication), with thanks to Nick Pelling for the original observation.

## Abstract

The D'Agapeyeff cipher (1939, 196 digit-pairs) contains a genuine anomaly: when laid out as a 14×14 grid, the final column concentrates the rarest symbols far beyond chance (p≈9e-10). This observation was first published by numberworld (2013) and Nick Pelling (January 2014) as informal posts; MsgTrail (2026) independently quantified it. We replicate the quantification under pre-registered methods (10,000-permutation null, hashed code and seeds, confirmation across four frozen data variants) and report a negative result on four pre-registered semantic readings of column 14 (embedded date, geographic coordinate, row checksum, positional trend). The cipher's main body (182 pairs, 13 symbols) is flat — flatter than all 240 shuffled-English controls — and shows no bigram-level structure (mutual information, conditional entropy, repeat rates, and bigram chi-square all at null). Per a pre-registered cap rule, column 14 is declared **structurally distinct, semantically unresolved**. Our contribution is the pre-registered replication, the null framework, the negative semantic battery, and the published test harness — not the observation (numberworld/Pelling) nor the first quantification (MsgTrail). No solution is claimed. All code, seeds, and the self-test harness (including a regression test for a historical scoring bug) are published alongside this note for reproduction.

## 1. The object

Alexander D'Agapeyeff's *Codes and Ciphers* (Oxford University Press, 1939) contains an unsolved challenge cipher: 395 digits arranged as 196 pairs, 18 distinct pairs. We work from a frozen transcription (variant B), laid out as printed in 14 rows of 14 pairs. Pair #98 (row 7, column 14) is the lone `04`.

## 2. Prior work and attribution

The column-14 observation is not ours. The earliest known spotting is a 2013 numberworld post; Nick Pelling documented it on 27 January 2014 ("Why I think the d'Agapeyeff cipher is diagonally transposed," Cipher Mysteries): "many of its oddities are to be found in the final right hand column," flagging the `04` and the concentration of `92` symbols occurring only in that column. Pelling's post — a blog post, not a paper — proposed a diagonal-transposition theory and included letter-frequency counts, but no significance test of the column concentration. MsgTrail (2026) independently quantified the concentration (p≈8.99e-10) and argued the column reads as 'empty'. Our split-half test does not support the diagonal-transposition hypothesis; we attribute the theory to Pelling and the test to ourselves, without claiming he was wrong — he sketched an idea, we measured one specific prediction of it. (Prior-art details per an independent literature survey by our collaborator Mentor; the numberworld 2013 post was not directly re-verified for this note.)

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

*Methods honesty note:* R1 and R2 were weak tests by construction (binary scores; a real score of 0 yields p=1.0 mechanically), and an independent audit relabelled all four predictions as retrodiction — locked after the body's flatness was known, so they confirmed method, not model. The confirmed finding is the clean negative result under a pre-registered cap, not the sweep.

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
- numberworld. Column-14 pattern noted, 2013. (Per independent literature survey; not directly re-verified for this note.)
- Pelling, N. "Why I think the d'Agapeyeff cipher is diagonally transposed..." Cipher Mysteries, 27 Jan 2014. https://ciphermysteries.com/2014/01/27/think-dagapeyeff-cipher-diagonally-transposed
- MsgTrail. Independent quantification of the column-14 concentration (p≈8.99e-10), 2026. (Per independent literature survey.)
- Shulman, D. (as AB STRUSE). "The D'Agapeyeff Cryptogram: A Challenge." *The Cryptogram*, Apr/May 1952, pp. 39–40, 46.
- Marland, T. D'Agapeyeff research program, 2026. https://www.dagapeyeffresearch.com/

## Appendix A: pre-registered tests and audit

(Bigam test: `build/PRE_REG_BIGRAM.md`, code `bigram_test.py` bf9f8b9d, seeds af0b4544. Column-14 readings: `build/PRE_REG_COL14_READINGS.md`, code `score_readings.py` aced6a91, seeds 0744eac5.)

All four column-14 reading predictions (P-R1–P-R4, "no hit") and the cap prediction P-CAP were confirmed. Audit, stated honestly: an independent review (Mentor) relabelled the predictions as retrodiction — they were locked after the body's flatness was already established, so their only falsification risk ran against already-excluded hypotheses; genuine novel predictions confirmed: 0. The R1/R2 reading tests were additionally weak by construction (binary scores). What remains valid and publishable is the *method*: pre-registered formats, hashed code, sealed seeds, permutation null, Bonferroni bar, cap rule — a clean negative result, honestly labeled. Prior knowledge was marked already-known vs new before each run; no edits were made after any hash. A parallel independent battery (144 key derivations + 54 checksum tests, Holm-corrected; 16 readings × 6 criteria vs 10,000 shuffles) reached the same cap verdict.
