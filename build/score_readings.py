#!/usr/bin/env python3
"""
Column-14 reading tests. Mechanical scoring, pre-registered null.
Pre-reg: PRE_REG_COL14_READINGS.md. Hash this file, seal seeds, then run.

Reading types:
  R1 date:       28-digit string contains valid YYYYMMDD, 1850-1939, contiguous.
  R2 coordinate: digits[0:7] = lat DDDMMSS valid, digits[7:14] = lon DDDMMSS valid.
  R3 checksum:   per row, sum(13 body pairs) % 100 == col14 pair. Count matches.
  R4 positional: Spearman |rho| between col14 pair values and row indices 1..14.

Null: 10,000 permutations of the col14 multiset. p = frac(null >= real).
Bar: p < 0.0125 per test (Bonferroni 0.05/4).
"""
import json
import math
import os
import random
import sys

def load(path):
    toks = open(path).read().split()
    assert len(toks) == 196
    body_rows = []
    col14 = []
    for r in range(14):
        row = toks[r * 14:(r + 1) * 14]
        body_rows.append([int(x) for x in row[:13]])
        col14.append(int(row[13]))
    return body_rows, col14

def days_in_month(y, m):
    if m == 2:
        leap = (y % 4 == 0 and y % 100 != 0) or (y % 400 == 0)
        return 29 if leap else 28
    return [0, 31, 0, 31, 30, 31, 30, 31, 31, 30, 31, 30, 31][m]

def score_r1(col14):
    s = "".join(f"{v:02d}" for v in col14)
    for i in range(len(s) - 7):
        blk = s[i:i + 8]
        y, m, d = int(blk[0:4]), int(blk[4:6]), int(blk[6:8])
        if 1850 <= y <= 1939 and 1 <= m <= 12 and 1 <= d <= days_in_month(y, m):
            return 1
    return 0

def score_r2(col14):
    s = "".join(f"{v:02d}" for v in col14)
    lat, lon = s[0:7], s[7:14]
    lat_ok = int(lat[0:3]) <= 90 and int(lat[3:5]) <= 59 and int(lat[5:7]) <= 59
    lon_ok = int(lon[0:3]) <= 180 and int(lon[3:5]) <= 59 and int(lon[5:7]) <= 59
    return 1 if (lat_ok and lon_ok) else 0

def score_r3(body_rows, col14):
    return sum(1 for row, c in zip(body_rows, col14)
               if sum(row) % 100 == c)

def spearman(xs, ys):
    n = len(xs)
    rx = _ranks(xs)
    ry = _ranks(ys)
    mx, my = sum(rx) / n, sum(ry) / n
    num = sum((a - mx) * (b - my) for a, b in zip(rx, ry))
    den = math.sqrt(sum((a - mx) ** 2 for a in rx) * sum((b - my) ** 2 for b in ry))
    return abs(num / den) if den > 0 else 0.0

def _ranks(xs):
    order = sorted(range(len(xs)), key=lambda i: xs[i])
    ranks = [0.0] * len(xs)
    i = 0
    while i < len(order):
        j = i
        while j + 1 < len(order) and xs[order[j + 1]] == xs[order[i]]:
            j += 1
        avg = (i + j) / 2.0 + 1
        for k in range(i, j + 1):
            ranks[order[k]] = avg
        i = j + 1
    return ranks

def score_r4(col14):
    return spearman(col14, list(range(1, 15)))

def all_scores(body_rows, col14):
    return {
        "R1_date": score_r1(col14),
        "R2_coord": score_r2(col14),
        "R3_checksum": score_r3(body_rows, col14),
        "R4_positional": score_r4(col14),
    }

def main():
    data_path = sys.argv[1] if len(sys.argv) > 1 else "B_no000.txt"
    seed_file = sys.argv[2] if len(sys.argv) > 2 else None
    body_rows, col14 = load(data_path)
    real = all_scores(body_rows, col14)

    if seed_file and os.path.exists(seed_file):
        seed = int(open(seed_file).read().strip())
        seed_source = f"file:{seed_file}"
    else:
        seed = int.from_bytes(os.urandom(8), "big")
        seed_source = "os.urandom(fresh)"
        if seed_file:
            open(seed_file, "w").write(str(seed))

    N_NULL = 10000
    rng = random.Random(seed)
    null_ge = {k: 0 for k in real}
    for _ in range(N_NULL):
        perm = col14[:]
        rng.shuffle(perm)
        s = all_scores(body_rows, perm)
        for k in real:
            if s[k] >= real[k]:
                null_ge[k] += 1
    pvals = {k: null_ge[k] / N_NULL for k in real}

    BAR = 0.0125
    hits = {k: (pvals[k] < BAR and real[k] > 0) for k in real}
    # For binary scores, a real score of 0 can never be a hit (p=1.0 by construction
    # since all nulls score >= 0); the real[k] > 0 guard makes this explicit.

    out = {
        "col14": col14,
        "real_scores": real,
        "n_null": N_NULL,
        "p_values": pvals,
        "bar": BAR,
        "hits": hits,
        "cap": ("STRUCTURALLY DISTINCT, SEMANTICALLY UNRESOLVED"
                if not any(hits.values())
                else f"HIT: {[k for k, h in hits.items() if h]}"),
        "seed": seed,
        "seed_source": seed_source,
        "predictions": {
            "P-R1": ("HIT" if hits["R1_date"] else "NO HIT"),
            "P-R2": ("HIT" if hits["R2_coord"] else "NO HIT"),
            "P-R3": ("HIT" if hits["R3_checksum"] else "NO HIT"),
            "P-R4": ("HIT" if hits["R4_positional"] else "NO HIT"),
        },
    }
    # Prediction check: pre-registered prior was NO HIT on all four.
    out["prediction_verdict"] = {
        k: ("CONFIRMED" if v == "NO HIT" else "MISS — investigate")
        for k, v in out["predictions"].items()
    }
    print(json.dumps(out, indent=2))

if __name__ == "__main__":
    main()
