#!/usr/bin/env python3
"""Tests for scorer.py — positive control, negative control, regression."""
import random, sys, os
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from scorer import (column_order_accuracy, adjacency_accuracy, symbol_accuracy,
                    exact_recovery, english_score)

passed = 0
failed = 0
def check(name, cond):
    global passed, failed
    if cond: passed += 1; print(f"  PASS {name}")
    else: failed += 1; print(f"  FAIL {name}")

print("== Positive controls ==")
# true key -> 1.0
check("col_order true key = 1.0",
      column_order_accuracy([3,1,4,0,2], [3,1,4,0,2]) == 1.0)
# known partial: 3/5 correct
check("col_order partial = 0.6",
      abs(column_order_accuracy([3,1,0,4,2], [3,1,4,0,2]) - 0.6) < 1e-9)
# adjacency: [0,1,2,3] vs [0,1,2,3] -> all 3 adjacencies match
check("adjacency true = 1.0",
      adjacency_accuracy([0,1,2,3], [0,1,2,3]) == 1.0)
# adjacency: [0,2,1,3] vs [0,1,2,3]: pairs (0,2),(2,1),(1,3); true has (0,1),(1,2),(2,3) -> 0 match
check("adjacency shuffled = 0.0",
      adjacency_accuracy([0,2,1,3], [0,1,2,3]) == 0.0)
# symbol accuracy
check("symbol 3/4 = 0.75",
      abs(symbol_accuracy(['a','b','x','d'], ['a','b','c','d']) - 0.75) < 1e-9)
# exact recovery
check("exact_recovery true = 1.0",
      exact_recovery([1,2],[1,2],['a'],['a']) == 1.0)
check("exact_recovery wrong order = 0.0",
      exact_recovery([2,1],[1,2],['a'],['a']) == 0.0)
check("exact_recovery wrong symbols = 0.0",
      exact_recovery([1,2],[1,2],['b'],['a']) == 0.0)

print("== Regression: Phase 4 zip-count bug ==")
# The bug: sum(1 for a,b in zip(order, inv))/len always returned 1.0
# because it never tested a==b. Our scorer MUST distinguish.
order_wrong = [1,2,3,4,5,6,7,8,9,10,11,12,13,0]
order_true  = [0,1,2,3,4,5,6,7,8,9,10,11,12,13]
buggy = sum(1 for a,b in zip(order_wrong, order_true))/len(order_true)  # old buggy formula
fixed = column_order_accuracy(order_wrong, order_true)
check(f"buggy formula gives 1.0 on wrong order (demonstrates bug): {buggy}",
      buggy == 1.0)
check(f"fixed scorer gives 0.0 on wrong order: {fixed}",
      fixed == 0.0)
check("fixed scorer distinguishes (not always 1.0)", buggy != fixed)

print("== Negative controls ==")
# random orders should average ~1/width positional accuracy
rng = random.Random(12345)
width = 14
trials = 10000
true = list(range(width))
accs = []
for _ in range(trials):
    perm = true[:]; rng.shuffle(perm)
    accs.append(column_order_accuracy(perm, true))
mean_acc = sum(accs)/len(accs)
expected = 1.0/width
check(f"random order mean accuracy {mean_acc:.4f} ~= 1/{width}={expected:.4f} (tol 0.01)",
      abs(mean_acc - expected) < 0.01)
# pure noise symbol accuracy: random symbols vs true should be ~1/alphabet
alpha = 18
saccs = []
syms = [f"s{i}" for i in range(alpha)]
for _ in range(5000):
    dec = [rng.choice(syms) for _ in range(100)]
    tru = [rng.choice(syms) for _ in range(100)]
    saccs.append(symbol_accuracy(dec, tru))
mean_sacc = sum(saccs)/len(saccs)
check(f"random symbol accuracy {mean_sacc:.4f} ~= 1/{alpha}={1/alpha:.4f} (tol 0.02)",
      abs(mean_sacc - 1/alpha) < 0.02)

print("== English score sanity ==")
# fake bigram LM where ('a','b') is likely
lb = {('a','b'): -0.5, ('b','a'): -2.0}
s_good = english_score(['a','b','a','b'], lb)
s_bad = english_score(['x','y','z'], lb)
check(f"english_score prefers real bigrams ({s_good:.2f} > {s_bad:.2f})", s_good > s_bad)

print(f"\n{passed} passed, {failed} failed")
sys.exit(0 if failed == 0 else 1)
