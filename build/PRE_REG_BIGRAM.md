# Bigram / Conditional-Entropy Discriminator — Pre-registration
**Date:** 2026-10-01 ~02:05 CT
**Status:** PRE-REGISTERED — code frozen, seeds to be drawn after.
**Author:** Chief (builder). Authorized by Billy 2026-10-01 ~02:01 CT.
**Scope:** Diagnostic only. Does not decrypt, does not run gate.py, does not touch Track A solver.

## Question
Is the 182-pair body (frozen variant B, printed column 14 removed) i.i.d. filler
or homophonic English? Unigrams cannot separate these; bigrams can.

## Data
- Input: `B_no000.txt` (196 pairs, frozen variant B).
- Body: pairs at 1-indexed positions not divisible by 14 (182 pairs, 13 symbols).
- Column 14 (14 pairs) is NEVER pooled with the body in any statistic.

## Statistics (all pre-registered)
- S0. Chi-square of unigram counts vs uniform-13 (df=12). Classify: flatter-than-chance
  (below 95% band of i.i.d. null) / at-chance / lumpier-than-chance.
- S1. Mutual information I(X_i ; X_{i+1}) between adjacent pairs.
- S2. Conditional entropy H(X_{i+1}|X_i) vs unigram entropy H(X).
- S3. Repeat rate of length-2 and length-3 substrings.
- S4. Chi-square of 13x13 bigram table against independence.

## Nulls
- Shuffled null: 500 random permutations of the body (destroys order, keeps unigrams).
- i.i.d. null: 500 uniform-13 draws, n=182.
- Seeds: drawn from os.urandom AFTER code freeze, written to sealed file BEFORE run.

## Decision logic (locked before running)
- ≥4 of 5 structure indicators above/below the shuffled-null 95% band (MI, rep2, rep3,
  bigram-chi2 above; h_cond below) → STRUCTURED: homophonic English, live construction.
- 0 of 5 → AT_NULL: i.i.d. filler, payload elsewhere (column 14 / 04 split).
- 1–3 of 5 → AMBIGUOUS: triggers partition test (separate pre-registration).

## Code
- bigram_test.py SHA-256: bf9f8b9d577192796e0230aff783444749470e4ae82754a227b04e4a657375b8
- Any code change after seed draw invalidates the run.

## Seeds
- SEEDS-BIGRAM-TEST.txt SHA-256: af0b45440a08b5b7f830345ac5f6e0064e73177431964e8e04e9731126fdef4a
- Drawn from os.urandom AFTER code freeze (2026-10-01 ~02:07 CT). Sealed before run.
