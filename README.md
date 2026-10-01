# The D'Agapeyeff Column-14 Anomaly: Statistical Confirmation and Negative Semantic Results

A characterization and replication-plus-quantification note on the unsolved 1939 D'Agapeyeff cipher. **Not a solution attempt.**

- **Paper:** [`paper.md`](paper.md) — read this first.
- **Harness:** `python3 harness/run_selftest.py` — one command validates everything (12 checks green at publication).

## What this is

The 196-pair cipher, laid out 14×14, has a genuine anomaly in its final column: the rarest symbols concentrate there far beyond chance (p≈9e-10). That observation was first published by Nick Pelling in January 2014; this repo independently confirms it with quantified statistics and a pre-registered null, and reports a negative result on four semantic readings of the column (date, coordinate, checksum, positional trend — none cleared the bar).

The cipher's main body is flat and structureless: not shuffled English, no bigram-level signal, consistent with filler.

## Reproduce

```
python3 harness/run_selftest.py
```

Checks: frozen-data integrity, scorer suite (including a regression test for a historical scoring bug that once voided a full round of results), discriminator power validation, column-14 separation. All analysis code and seeds are hashed in `build/` pre-registration documents.

## Attribution

Column-14 observation: Nick Pelling, Cipher Mysteries, 27 Jan 2014. Statistics, null framework, and negative semantic result: this work. "D'Agapeyeff forgot his method" is unverified lore (no primary source located) and carries no argument here.

## License

Code: MIT. Text: CC-BY-4.0. Cite Pelling 2014 for the observation.
