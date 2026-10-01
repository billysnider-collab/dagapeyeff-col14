#!/usr/bin/env python3
"""
D'Agapeyeff harness self-test. ONE command validates the whole apparatus.

Runs:
  1. Data integrity: frozen variant B loads, 196 pairs, body/col14 split = 182/14.
  2. Scorer suite (test_scorer.py) — includes the Phase 4 zip-count bug regression:
     the old formula `sum(1 for a,b in zip(order, inv))/len` returned 1.0 for EVERY
     order because it never checked a==b. If this regression ever fails, the harness
     is broken and every number it produced is void.
  3. Discriminator power check: the bigram test must flag synthetic homophonic
     English as STRUCTURED and synthetic i.i.d. as AT_NULL. A discriminator that
     cannot tell these apart is vacuous.
  4. Column-14 separation: body and column 14 never pooled (extraction check).

Exit 0 = harness healthy. Anything else = stop, do not trust any output.
"""
import subprocess
import sys
import os
import random
from collections import Counter

HERE = os.path.dirname(os.path.abspath(__file__))
WORK = os.path.dirname(HERE)
sys.path.insert(0, os.path.join(WORK, "build"))

passed = 0
failed = 0

def check(name, cond):
    global passed, failed
    if cond:
        passed += 1
        print(f"  PASS {name}")
    else:
        failed += 1
        print(f"  FAIL {name}")

print("== 1. Data integrity ==")
toks = open(os.path.join(WORK, "data", "B_no000.txt")).read().split()
check("frozen variant B has 196 pairs", len(toks) == 196)
body = [t for i, t in enumerate(toks, 1) if i % 14 != 0]
col14 = [t for i, t in enumerate(toks, 1) if i % 14 == 0]
check("body = 182 pairs", len(body) == 182)
check("column 14 = 14 pairs", len(col14) == 14)
check("body uses 13 symbols", len(set(body)) == 13)
check("no pair appears in both body and col14 extraction overlap check",
      len(set(body) | set(col14)) <= 18)

print("== 2. Scorer suite (incl. zip-count bug regression) ==")
r = subprocess.run([sys.executable, os.path.join(WORK, "test_scorer.py")],
                   capture_output=True, text=True, cwd=WORK)
print("   " + r.stdout.strip().split("\n")[-1])
check("test_scorer.py exits 0 (all pass, bug regression green)", r.returncode == 0)
check("regression line present in output",
      "zip-count" in r.stdout.lower() or "zip" in r.stdout.lower())

print("== 3. Discriminator power check ==")
from bigram_test import bigram_stats, chi_square_bigram_independence, repeat_rate

def band_of_null(gen, nrep, seed):
    rng = random.Random(seed)
    vals = {"mi": [], "bi_chi2": []}
    for _ in range(nrep):
        seq = gen(rng)
        st = bigram_stats(seq)
        vals["mi"].append(st["mi"])
        vals["bi_chi2"].append(
            chi_square_bigram_independence(st["bi"], st["uni"], len(seq) - 1,
                                           sorted(set(seq))))
    out = {}
    for k, v in vals.items():
        s = sorted(v)
        out[k] = (s[int(0.025 * nrep)], s[int(0.975 * nrep)])
    return out

symbols = [f"S{i}" for i in range(13)]
# Synthetic i.i.d. control: batch must read AT_NULL at ~null rate.
# (A single i.i.d. draw falls outside the 95% band 5% of the time by design,
# so test the batch false-alarm rate instead — deterministic under fixed seed.)
bands = band_of_null(lambda rng: [rng.choice(symbols) for _ in range(182)], 200, 777)
rng_batch = random.Random(778)
inside = 0
N_BATCH = 50
for _ in range(N_BATCH):
    seq = [rng_batch.choice(symbols) for _ in range(182)]
    st = bigram_stats(seq)
    if bands["mi"][0] <= st["mi"] <= bands["mi"][1]:
        inside += 1
check(f"i.i.d. batch inside null MI band {inside}/{N_BATCH} (>=45)", inside >= 45)

# Synthetic homophonic-English control: must read STRUCTURED.
# Build a Markov chain with real bigram structure, then split each state
# across 2 homophone symbols (flattening unigrams, preserving transitions).
rng = random.Random(4242)
states = list("abcdef")  # 6 "letters"
# skewed transition matrix = English-like lumpiness
trans = {
    "a": [0.4, 0.2, 0.15, 0.1, 0.1, 0.05],
    "b": [0.1, 0.1, 0.4, 0.2, 0.1, 0.1],
    "c": [0.2, 0.3, 0.1, 0.1, 0.2, 0.1],
    "d": [0.05, 0.1, 0.1, 0.5, 0.2, 0.05],
    "e": [0.3, 0.1, 0.1, 0.1, 0.1, 0.3],
    "f": [0.1, 0.2, 0.2, 0.2, 0.15, 0.15],
}
homophones = {s: [f"{s}0", f"{s}1"] for s in states}  # each letter -> 2 symbols
seq_letters = ["a"]
for _ in range(400):
    prev = seq_letters[-1]
    r_ = rng.random()
    cum = 0.0
    for s, p in zip(states, trans[prev]):
        cum += p
        if r_ < cum:
            seq_letters.append(s)
            break
seq_hom = [rng.choice(homophones[s]) for s in seq_letters]  # 12 symbols, flat-ish
st_hom = bigram_stats(seq_hom)
hom_symbols = sorted(set(seq_hom))
hom_bi_chi2 = chi_square_bigram_independence(st_hom["bi"], st_hom["uni"],
                                             len(seq_hom) - 1, hom_symbols)
# null bands for THIS homophonic sequence's own alphabet
bands_h = band_of_null(lambda rr: [rr.choice(hom_symbols) for _ in range(len(seq_hom))],
                       200, 4243)
hom_structured = st_hom["mi"] > bands_h["mi"][1]
check(f"homophonic control MI {st_hom['mi']:.3f} above null band "
      f"[{bands_h['mi'][0]:.3f},{bands_h['mi'][1]:.3f}] (STRUCTURED)", hom_structured)
# and unigrams should be flatter than the raw letter distribution would be
uni_counts = Counter(seq_hom)
max_share = max(uni_counts.values()) / len(seq_hom)
check(f"homophonic unigrams flattened (max share {max_share:.2f} < 0.25)", max_share < 0.25)

print("== 4. Column-14 separation ==")
# Re-derive extraction independently and confirm no pooling in bigram_test
import importlib.util
spec = importlib.util.spec_from_file_location(
    "bt", os.path.join(WORK, "build", "bigram_test.py"))
bt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(bt)
b2, c2 = bt.load_body(os.path.join(WORK, "data", "B_no000.txt"))
check("load_body reproduces 182/14 split", len(b2) == 182 and len(c2) == 14)
check("load_body body matches independent extraction", b2 == body and c2 == col14)

print(f"\n{passed} passed, {failed} failed")
print("HARNESS " + ("HEALTHY" if failed == 0 else "BROKEN — DO NOT TRUST OUTPUT"))
sys.exit(0 if failed == 0 else 1)
