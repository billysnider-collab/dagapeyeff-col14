#!/usr/bin/env python3
"""
Bigram / conditional-entropy discriminator: i.i.d. filler vs homophonic English.
Phase 5 diagnostic, authorized by Billy 2026-10-01 ~02:01 CT.

Body: 182 pairs (frozen variant B with every 14th pair / printed column 14 removed).
Column 14 is NEVER pooled with the body.

Statistics:
  S0. Chi-square of unigram counts vs uniform-13 (Billy's refinement):
      flatter-than-chance / at-chance / lumpier-than-chance.
  S1. Mutual information I(X_i ; X_{i+1}) between adjacent pairs.
  S2. Conditional entropy H(X_{i+1} | X_i) vs unigram entropy H(X).
  S3. Repeat rate of length-2 and length-3 substrings vs shuffled null.
  S4. Chi-square of 13x13 bigram table against independence.

Nulls (fresh seeds, drawn AFTER code freeze):
  - Shuffled null: random permutations of the body (destroys order, keeps unigrams).
  - i.i.d. null: uniform-13 draws, n=182.

Decision logic (pre-registered):
  - If S1..S4 all at null (within 95% bands of BOTH nulls): body consistent with
    i.i.d. filler. Leans "filler, payload elsewhere."
  - If S1..S4 show structure (above 95% band of shuffled null): body consistent
    with homophonic English. Live construction.
  - Mixed: report as ambiguous -> triggers partition test (separate prereg).

This is a DIAGNOSTIC. It does not decrypt, does not run gate.py, does not touch
Track A solver. Blocked items remain blocked.
"""
import hashlib
import json
import math
import os
import random
import sys
from collections import Counter

# ---------------------------------------------------------------- data
def load_body(path):
    toks = open(path).read().split()
    assert len(toks) == 196, f"expected 196 pairs, got {len(toks)}"
    # Remove every 14th pair (1-indexed): printed column 14
    body = [t for i, t in enumerate(toks, start=1) if i % 14 != 0]
    col14 = [t for i, t in enumerate(toks, start=1) if i % 14 == 0]
    assert len(body) == 182 and len(col14) == 14
    return body, col14

# ---------------------------------------------------------------- stats
def unigram_entropy(counts, n):
    h = 0.0
    for c in counts.values():
        p = c / n
        h -= p * math.log2(p)
    return h

def bigram_stats(seq):
    """Return dict with MI, cond entropy, unigram entropy, bigram table."""
    n = len(seq)
    uni = Counter(seq)
    bi = Counter(zip(seq[:-1], seq[1:]))
    nb = n - 1
    h_x = unigram_entropy(uni, n)
    # H(X_{i+1} | X_i) = H(X_i, X_{i+1}) - H(X_i)
    h_joint = 0.0
    for c in bi.values():
        p = c / nb
        h_joint -= p * math.log2(p)
    # H(X_i) over the n-1 adjacent-left positions; approximate with unigram
    h_cond = h_joint - h_x
    mi = h_x - h_cond  # I(X_i;X_{i+1}) = H(X_{i+1}) - H(X_{i+1}|X_i)
    return {
        "mi": mi,
        "h_cond": h_cond,
        "h_uni": h_x,
        "uni": uni,
        "bi": bi,
        "n": n,
    }

def chi_square_uniform(uni, n, k=13):
    exp = n / k
    return sum((uni.get(s, 0) - exp) ** 2 / exp for s in set(uni) | {f"SYM{i}" for i in range(k)})

def chi_square_uniform_exact(symbols, uni, n):
    exp = n / len(symbols)
    return sum((uni.get(s, 0) - exp) ** 2 / exp for s in symbols)

def chi_square_bigram_independence(bi, uni, nb, symbols):
    chi2 = 0.0
    for a in symbols:
        for b in symbols:
            obs = bi.get((a, b), 0)
            exp = uni[a] * uni[b] / nb
            if exp > 0:
                chi2 += (obs - exp) ** 2 / exp
    return chi2

def repeat_rate(seq, k):
    n = len(seq)
    grams = [tuple(seq[i:i+k]) for i in range(n - k + 1)]
    c = Counter(grams)
    total = len(grams)
    # fraction of positions that belong to a repeated gram
    repeated = sum(v for v in c.values() if v > 1)
    return repeated / total

# ---------------------------------------------------------------- nulls
def run_nulls(body, symbols, n_shuf, n_iid, seed):
    rng = random.Random(seed)
    results = {"shuffled": [], "iid": []}
    n = len(body)
    for _ in range(n_shuf):
        perm = body[:]
        rng.shuffle(perm)
        st = bigram_stats(perm)
        results["shuffled"].append({
            "mi": st["mi"],
            "h_cond": st["h_cond"],
            "rep2": repeat_rate(perm, 2),
            "rep3": repeat_rate(perm, 3),
            "bi_chi2": chi_square_bigram_independence(st["bi"], st["uni"], n - 1, symbols),
        })
    for _ in range(n_iid):
        seq = [rng.choice(symbols) for _ in range(n)]
        st = bigram_stats(seq)
        results["iid"].append({
            "mi": st["mi"],
            "h_cond": st["h_cond"],
            "rep2": repeat_rate(seq, 2),
            "rep3": repeat_rate(seq, 3),
            "bi_chi2": chi_square_bigram_independence(st["bi"], st["uni"], n - 1, symbols),
            "uni_chi2": chi_square_uniform_exact(symbols, st["uni"], n),
        })
    return results

def band(vals):
    s = sorted(vals)
    n = len(s)
    return (s[int(0.025 * n)], s[int(0.975 * n)], sum(s) / n)

# ---------------------------------------------------------------- main
def main():
    data_path = sys.argv[1] if len(sys.argv) > 1 else "B_no000.txt"
    seed_file = sys.argv[2] if len(sys.argv) > 2 else None

    body, col14 = load_body(data_path)
    symbols = sorted(set(body))
    assert len(symbols) == 13, f"expected 13 symbols, got {len(symbols)}: {symbols}"
    # Confirm column 14 not pooled: body must not contain col14-only symbols leaking?
    # (informational only)
    n = len(body)

    st = bigram_stats(body)
    uni_chi2 = chi_square_uniform_exact(symbols, st["uni"], n)
    bi_chi2 = chi_square_bigram_independence(st["bi"], st["uni"], n - 1, symbols)
    rep2 = repeat_rate(body, 2)
    rep3 = repeat_rate(body, 3)

    # Load or draw seed
    if seed_file and os.path.exists(seed_file):
        seed = int(open(seed_file).read().strip())
        seed_source = f"file:{seed_file}"
    else:
        seed = int.from_bytes(os.urandom(8), "big")
        seed_source = "os.urandom(fresh)"
        if seed_file:
            open(seed_file, "w").write(str(seed))

    N_SHUF, N_IID = 500, 500
    nulls = run_nulls(body, symbols, N_SHUF, N_IID, seed)

    out = {
        "body_n": n,
        "n_symbols": len(symbols),
        "symbols": symbols,
        "seed": seed,
        "seed_source": seed_source,
        "n_shuffled_null": N_SHUF,
        "n_iid_null": N_IID,
        "observed": {
            "uni_chi2_vs_uniform13": uni_chi2,
            "uni_chi2_df": 12,
            "mi_adjacent": st["mi"],
            "h_cond": st["h_cond"],
            "h_uni": st["h_uni"],
            "h_gap": st["h_uni"] - st["h_cond"],
            "repeat_rate_2": rep2,
            "repeat_rate_3": rep3,
            "bigram_chi2_vs_independence": bi_chi2,
        },
        "null_bands_95pct": {},
        "verdict": None,
    }
    for key in ["mi", "h_cond", "rep2", "rep3", "bi_chi2"]:
        for null in ["shuffled", "iid"]:
            vals = [r[key] for r in nulls[null]]
            lo, hi, mean = band(vals)
            out["null_bands_95pct"][f"{null}_{key}"] = {"lo": lo, "hi": hi, "mean": mean}
    # uni_chi2 band from iid null only (shuffled preserves unigrams exactly)
    vals = [r["uni_chi2"] for r in nulls["iid"]]
    lo, hi, mean = band(vals)
    out["null_bands_95pct"]["iid_uni_chi2"] = {"lo": lo, "hi": hi, "mean": mean}

    # Pre-registered decision logic
    obs = out["observed"]
    b = out["null_bands_95pct"]
    struct_count = 0
    for key, obs_key in [("mi", "mi_adjacent"), ("rep2", "repeat_rate_2"),
                         ("rep3", "repeat_rate_3"), ("bi_chi2", "bigram_chi2_vs_independence")]:
        hi_shuf = b[f"shuffled_{key}"]["hi"]
        if obs[obs_key] > hi_shuf:
            struct_count += 1
    # h_cond: structure means LOWER than null
    if obs["h_cond"] < b["shuffled_h_cond"]["lo"]:
        struct_count += 1

    if struct_count >= 4:
        verdict = "STRUCTURED: consistent with homophonic English. Live construction."
    elif struct_count == 0:
        verdict = "AT_NULL: consistent with i.i.d. filler. Leans filler, payload elsewhere."
    else:
        verdict = f"AMBIGUOUS ({struct_count}/5 above null): triggers partition test."

    # Billy's refinement: flatter / at / lumpier than chance
    lo_iid = b["iid_uni_chi2"]["lo"]
    hi_iid = b["iid_uni_chi2"]["hi"]
    if uni_chi2 < lo_iid:
        flat = "FLATTER_THAN_CHANCE: deliberate flattening (homophonic or engineered filler)."
    elif uni_chi2 > hi_iid:
        flat = "LUMPIER_THAN_CHANCE: unexpected given prior evenness result."
    else:
        flat = "AT_CHANCE: consistent with random draw over 13 symbols."
    out["flatness"] = flat
    out["verdict"] = verdict

    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
