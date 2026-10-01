# Column-14 Reading Tests — Predictions (Pre-registered)
**Date:** 2026-10-01 ~02:25 CT
**Status:** PRE-REGISTERED — hash before measuring. No edits after hash.
**Author:** Chief. Authorized under Charter (Billy, 2026-10-01).

## Already-known (labeled, NOT predictions)
- A1: column 14 = [84,62,93,92,85,64,04,94,71,93,74,92,83,92] (14 pairs).
- A2: rare pairs concentrate in column 14 (8/8 of the 5 rarest, p≈9e-10).
- A3: column-14 symbol set differs from body.
- A4: digit string = 8462939285640494719374928392 (28 digits).

## Reading types (mechanical scoring, no human judgment post-hash)
- **R1 date:** 28-digit string contains a contiguous 8-digit block forming a valid
  date YYYYMMDD with 1850≤YYYY≤1939. Score ∈ {0,1}.
- **R2 coordinate:** digits[0:7] parse as latitude DDDMMSS (DDD≤90, MM≤59, SS≤59)
  AND digits[7:14] parse as longitude DDDMMSS (DDD≤180, MM≤59, SS≤59).
  Score ∈ {0,1}.
- **R3 row checksum:** for each of 14 rows, (sum of the 13 body-pair integer values
  in that row) mod 100 == column-14 pair integer value. Score ∈ {0..14}.
- **R4 positional trend:** Spearman |rho| between column-14 pair integer values
  and row indices 1..14. Score ∈ [0,1].

## Null
- 10,000 permutations of the column-14 multiset (same 14 pairs, shuffled order),
  fresh seed from os.urandom AFTER code freeze, sealed before run.
- p = fraction of null draws with score ≥ real score.
- Per-test bar: p < 0.0125 (0.05 Bonferroni over 4 reading types).

## Predictions (all NEW — these exact tests never run before)
- P-R1: R1 will NOT clear the bar (p ≥ 0.0125). Miss = p < 0.0125.
- P-R2: R2 will NOT clear the bar (p ≥ 0.0125). Miss = p < 0.0125.
- P-R3: R3 will NOT clear the bar (p ≥ 0.0125). Miss = p < 0.0125.
- P-R4: R4 will NOT clear the bar (p ≥ 0.0125). Miss = p < 0.0125.
- P-CAP: cap outcome — "structurally distinct, semantically unresolved."
  Miss = any reading clears its bar.

## Code
- score_readings.py SHA-256: aced6a91306b56e6547c264549ded7620b00246359db8f7005353dd756da1d12
- Compiled clean. Any change after seed draw invalidates the run.

## Seeds
- SEEDS-COL14-READINGS.txt SHA-256: 0744eac58d1e37a4cd32d95781e0d503f662767d4dbacf22dc445f688397cd87
- Drawn from os.urandom AFTER code freeze (2026-10-01 ~02:28 CT). Sealed before run.
