"""Exact standard-library verification of monotone-query reconstruction.

Run: python verify_monotone_reconstruction.py
No floating-point comparisons, no external dependencies.
"""
from fractions import Fraction as F
from itertools import product, accumulate
from random import Random
import json


def shortest_paths(nvertices, edges, source=0):
    """Bellman-Ford: edges (i,j,c) encode S[j]-S[i] <= c."""
    d = [None] * nvertices
    d[source] = 0
    for _ in range(nvertices):
        changed = False
        for i, j, c in edges:
            if d[i] is not None and (d[j] is None or d[j] > d[i] + c):
                d[j] = d[i] + c
                changed = True
        if not changed:
            return d
    raise ValueError("Inconsistent interval summaries: negative cycle")


def reconstruct(n, interval_bounds):
    """Bounds are (i,j,lo,hi), for sum(x[i:j]) in [lo,hi].

    Include finite bounds for every x_i and an exact total bound.
    Indexing is Python's zero-based, half-open convention.
    All numbers may be int or fractions.Fraction.
    """
    edges = []
    for i, j, lo, hi in interval_bounds:
        edges += [(i, j, hi), (j, i, -lo)]
    U = shortest_paths(n + 1, edges)
    reverse = [(j, i, c) for i, j, c in edges]
    reverse_d = shortest_paths(n + 1, reverse)
    if any(v is None for v in U + reverse_d):
        raise ValueError("Every prefix needs finite upper and lower bounds")
    L = [-v for v in reverse_d]
    midpoint = [F(lo + hi, 2) for lo, hi in zip(L, U)]
    xstar = [midpoint[i + 1] - midpoint[i] for i in range(n)]
    return L, U, xstar


def query_interval(w, L, U):
    """Exact answer interval for any real-valued monotone w.

    Assumes fixed total: L[-1] == U[-1].
    """
    if not all(w[i] <= w[i + 1] for i in range(len(w) - 1)) and not all(
        w[i] >= w[i + 1] for i in range(len(w) - 1)
    ):
        raise ValueError("The theorem requires monotone weights")
    assert L[-1] == U[-1]
    a = w[-1] * L[-1] - sum((w[i] - w[i - 1]) * L[i] for i in range(1, len(w)))
    b = w[-1] * U[-1] - sum((w[i] - w[i - 1]) * U[i] for i in range(1, len(w)))
    return min(a, b), max(a, b)


def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def feasible(x, bounds):
    return all(lo <= sum(x[i:j]) <= hi for i, j, lo, hi in bounds)


def main():
    rng = Random(20260908)
    tested_queries = 0
    feasible_grid_vectors = 0
    cases = 600
    for _ in range(cases):
        n = rng.randrange(2, 8)
        witness = tuple(rng.randrange(3) for _ in range(n))
        total = sum(witness)
        bounds = [(i, i + 1, 0, 2) for i in range(n)]
        bounds.append((0, n, total, total))
        for _ in range(2 * n):
            i = rng.randrange(n)
            j = rng.randrange(i + 1, n + 1)
            s = sum(witness[i:j])
            bounds.append((i, j, max(0, s - rng.randrange(4)), min(2 * (j - i), s + rng.randrange(4))))
        L, U, xstar = reconstruct(n, bounds)
        assert feasible(xstar, bounds)
        xmin = tuple(L[i + 1] - L[i] for i in range(n))
        xmax = tuple(U[i + 1] - U[i] for i in range(n))
        assert feasible(xmin, bounds) and feasible(xmax, bounds)
        possible = [x for x in product(range(3), repeat=n) if feasible(x, bounds)]
        assert xmin in possible and xmax in possible
        feasible_grid_vectors += len(possible)
        prefixes = [tuple(accumulate((0,) + x)) for x in possible]
        assert L == [min(s[i] for s in prefixes) for i in range(n + 1)]
        assert U == [max(s[i] for s in prefixes) for i in range(n + 1)]
        for _ in range(20):
            w = sorted((rng.randrange(-9, 10) for _ in range(n)), reverse=rng.choice([True, False]))
            lo, hi = query_interval(w, L, U)
            values = [dot(w, x) for x in possible]
            assert (lo, hi) == (min(values), max(values))
            assert dot(w, xstar) == F(lo + hi, 2)
            radius = F(sum(abs(w[i] - w[i - 1]) * (U[i] - L[i]) for i in range(1, n)), 2)
            assert radius == F(hi - lo, 2)
            tested_queries += 1

    # Four slots, range [0,1], total 1, half-life-one-slot weights.
    bounds = [(i, i + 1, 0, 1) for i in range(4)] + [(0, 4, 1, 1)]
    L, U, xstar = reconstruct(4, bounds)
    w = [F(z, 15) for z in (1, 2, 4, 8)]
    lo, hi = query_interval(w, L, U)
    answer = dot(w, xstar)
    uniform = F(1, 4)
    optimum_error = F(hi - lo, 2)
    uniform_error = max(uniform - lo, hi - uniform)
    assert xstar == [F(1, 2), 0, 0, F(1, 2)]
    assert answer == F(3, 10)
    assert optimum_error == F(7, 30)
    assert uniform_error == F(17, 60)

    # Nonmonotone weights: same center has twice the best possible error.
    bounds3 = [(i, i + 1, 0, 1) for i in range(3)] + [(0, 3, 1, 1)]
    _, _, center3 = reconstruct(3, bounds3)
    assert center3 == [F(1, 2), 0, F(1, 2)]
    assert dot([0, 1, 0], center3) == 0  # true query range [0,1], optimum midpoint 1/2.

    # Inconsistency detection.
    try:
        reconstruct(1, [(0, 1, 0, 1), (0, 1, 2, 2)])
    except ValueError:
        pass
    else:
        raise AssertionError("A negative cycle went undetected")

    result = {
        "seed": 20260908,
        "constraint_systems": cases,
        "monotone_weight_queries": tested_queries,
        "feasible_grid_vectors": feasible_grid_vectors,
        "arithmetic": "exact integers and Fraction",
        "all_assertions_passed": True,
        "example": {"xstar": list(map(str, xstar)), "query_interval": [str(lo), str(hi)],
                    "minimax_answer": str(answer), "uniform_fill_answer": str(uniform),
                    "minimax_error": str(optimum_error), "uniform_fill_error": str(uniform_error)},
        "scope": "Finite grid verification and counterexamples support but do not replace the written real-valued proof."
    }
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
