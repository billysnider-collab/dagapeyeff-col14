#!/usr/bin/env python3
"""
Independent scorer for D'Agapeyeff Phase 5 prep — written from scratch.
One shared module for all accuracy metrics. No dependency on Phase 4 solver.py.

Metrics:
  column_order_accuracy(order, true_order) -> float
  adjacency_accuracy(order, true_order) -> float
  symbol_accuracy(decoded, true_symbols) -> float
  exact_recovery(order, true_order, decoded, true_symbols) -> float (1.0 or 0.0)
  english_score(symbols, log_bigram) -> float (mean log-prob per bigram)
"""

def column_order_accuracy(order, true_order):
    """Fraction of positions i where order[i] == true_order[i].
    REGRESSION GUARD: must compare elements, not just count pairs.
    The Phase 4 bug was: sum(1 for a,b in zip(order, inv))/len — always 1.0.
    """
    if not order or not true_order:
        return 0.0
    n = min(len(order), len(true_order))
    if n == 0:
        return 0.0
    matches = sum(1 for a, b in zip(order[:n], true_order[:n]) if a == b)
    return matches / n


def adjacency_accuracy(order, true_order):
    """Fraction of adjacent pairs (order[i], order[i+1]) that appear as
    adjacent in true_order (in the same order). Measures if the relative
    ordering is correct even if absolute positions shift."""
    if len(order) < 2 or len(true_order) < 2:
        return 0.0
    true_adj = set()
    for i in range(len(true_order) - 1):
        true_adj.add((true_order[i], true_order[i+1]))
    n = len(order) - 1
    hits = sum(1 for i in range(n) if (order[i], order[i+1]) in true_adj)
    return hits / n


def symbol_accuracy(decoded, true_symbols):
    """Fraction of positions where decoded[i] == true_symbols[i]."""
    if not decoded or not true_symbols:
        return 0.0
    n = min(len(decoded), len(true_symbols))
    if n == 0:
        return 0.0
    return sum(1 for a, b in zip(decoded[:n], true_symbols[:n]) if a == b) / n


def exact_recovery(order, true_order, decoded, true_symbols):
    """1.0 iff order exactly equals true_order AND decoded exactly equals
    true_symbols. Otherwise 0.0."""
    if list(order) == list(true_order) and list(decoded) == list(true_symbols):
        return 1.0
    return 0.0


def english_score(symbols, log_bigram, oov=-20.0):
    """Mean bigram log-probability per bigram. log_bigram: dict[(a,b)] -> logp.
    Returns oov-heavy negative values for non-language-like sequences."""
    if len(symbols) < 2:
        return oov
    total = 0.0
    n = 0
    for i in range(len(symbols) - 1):
        total += log_bigram.get((symbols[i], symbols[i+1]), oov)
        n += 1
    return total / n if n else oov
