"""Exact rational audit of rank gaps and the slab-polytope edge graph.

This is finite verification, not a replacement for the general proofs.
Run: python3 round2_robust/check_robust.py
"""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from math import comb
from pathlib import Path
import json


def defect(x):
    return sum((t * (1 - t) for t in x), F(0))


def vectors(n, s, eta):
    out = set()
    for ones in combinations(range(n), s):
        z = tuple(F(i in ones) for i in range(n))
        out.add(z)
        if eta:
            for j in range(n):
                v = list(z)
                v[j] = 1 - eta if z[j] else eta
                out.add(tuple(v))
    return sorted(out)


def edge_max(v, w):
    d = [b - a for a, b in zip(v, w)]
    h = sum((a * a for a in d), F(0))
    ell = sum((a * (1 - 2 * b) for a, b in zip(d, v)), F(0))
    t = min(F(1), max(F(0), ell / (2 * h)))
    return defect(v) + t * ell - t * t * h


def graph_edges(vs, s, eta):
    """Generate all cube and slab-face edges by active-constraint rank.

    The pairwise test is independent of the formulas for edge heights.
    Both slab planes cannot be active when eta > 0.
    """
    n = len(vs[0])
    sums = [sum(v) for v in vs]
    edges = []
    for i, v in enumerate(vs):
        for j in range(i):
            w = vs[j]
            fixed = sum(a == b and a in (0, 1) for a, b in zip(v, w))
            if not eta:
                adjacent = fixed == n - 2
            else:
                plane = int(sums[i] == sums[j] and sums[i] in (s - eta, s + eta))
                adjacent = fixed + plane == n - 1
            if adjacent:
                edges.append((j, i, edge_max(w, v)))
    return edges


def component_count(vs, edges, delta):
    active = [defect(v) <= delta for v in vs]
    par = list(range(len(vs)))

    def root(i):
        while par[i] != i:
            par[i] = par[par[i]]
            i = par[i]
        return i

    for i, j, height in edges:
        if height <= delta:
            assert active[i] and active[j]
            par[root(i)] = root(j)
    return len({root(i) for i, is_active in enumerate(active) if is_active})


def main():
    counts = dict(sorted_vectors=0, rank_splits=0, band_gap_checks=0,
                  equality_witnesses=0, graph_cases=0, graph_threshold_checks=0,
                  independently_enumerated_edges=0, constructive_paths=0,
                  nearest_rounding_checks=0)
    etas = [F(j, 8) for j in range(5)]
    grid = [F(j, 8) for j in range(9)]
    for n in range(2, 9):
        for raw in combinations_with_replacement(grid, n):
            x = tuple(reversed(raw))
            d = defect(x)
            total = sum(x)
            counts['sorted_vectors'] += 1
            for s in range(1, n):
                u, v = x[s - 1:s + 1]
                sigma = sum((1 - t for t in x[:s]), F(0))
                rho = sum(x[s:], F(0))
                a, b = sigma - (1 - u), rho - v
                t_slack = sum(((t - u) * (1 - t) for t in x[:s]), F(0))
                t_slack += sum(((v - t) * t for t in x[s:]), F(0))
                e, g = total - s, u - v
                residual = 2 * d + e * e + g * g - 1
                rhs = 2 * t_slack + 2 * (1 - v) * a + 2 * u * b + (b - a) ** 2
                assert min(a, b, t_slack, g) >= 0
                assert residual == rhs and residual >= 2 * g * (a + b)
                if g > 0:
                    assert (residual == 0) == (a == b == 0)
                counts['rank_splits'] += 1
                for eta in etas:
                    if abs(e) > eta:
                        continue
                    d0, dc = eta * (1 - eta), (1 - eta * eta) / 2
                    assert d >= abs(e) * (1 - abs(e))
                    z = (F(1),) * s + (F(0),) * (n - s)
                    if u <= F(1, 2):
                        anchor = (F(1),) * (s - 1) + (1 - eta,) + (F(0),) * (n - s)
                    elif v >= F(1, 2):
                        anchor = (F(1),) * s + (eta,) + (F(0),) * (n - s - 1)
                    else:
                        anchor = z
                    directional_gain = sum(((2 * a - 1) * (b - a) for a, b in zip(x, anchor)), F(0))
                    assert directional_gain >= 0 and defect(anchor) <= d
                    if x != anchor:
                        assert edge_max(x, anchor) == d
                    if anchor != z:
                        assert edge_max(anchor, z) == defect(anchor)
                    counts['constructive_paths'] += 1
                    if d < F(1, 2) - eta * eta:
                        assert F(1, 2) not in x
                        assert sum(t > F(1, 2) for t in x) == s
                        counts['nearest_rounding_checks'] += 1
                    if d <= d0:
                        # Equivalent to g >= (1 + sqrt(1 - 4*d))/2.
                        assert g >= F(1, 2) and (2 * g - 1) ** 2 >= 1 - 4 * d
                    elif d <= dc:
                        assert g * g >= 1 - 2 * d - eta * eta
                    if d < dc:
                        assert g > 0
                    counts['band_gap_checks'] += 1

    for n in range(2, 9):
        for s in range(1, n):
            for eta in etas:
                for j in range(33):
                    a = F(j, 64)
                    if a <= eta:
                        x = (F(1),) * (s - 1) + (1 - a,) + (F(0),) * (n - s)
                        d = a * (1 - a)
                        assert defect(x) == d and abs(sum(x) - s) <= eta
                        assert x[s - 1] - x[s] == 1 - a
                        counts['equality_witnesses'] += 1
                for j in range(65):
                    g = F(j, 64)
                    if g <= 1 - eta:
                        u, v = (1 - eta + g) / 2, (1 - eta - g) / 2
                        x = (F(1),) * (s - 1) + (u, v) + (F(0),) * (n - s - 1)
                        d = (1 - eta * eta - g * g) / 2
                        assert defect(x) == d and sum(x) == s - eta
                        assert x[s - 1] - x[s] == g
                        assert eta * (1 - eta) <= d <= (1 - eta * eta) / 2
                        counts['equality_witnesses'] += 1

    for n in range(2, 7):
        for s in range(1, n):
            for eta in etas:
                vs = vectors(n, s, eta)
                edges = graph_edges(vs, s, eta)
                d0, ds, dc = eta * (1 - eta), eta - eta * eta / 2, (1 - eta * eta) / 2
                allowed = {d0, ds, dc} if eta else {F(1, 2)}
                assert all(height in allowed for _, _, height in edges)
                breakpoints = sorted({F(0), d0, ds, dc, F(n, 4)})
                budgets = sorted(set(breakpoints + [(a + b) / 2 for a, b in zip(breakpoints, breakpoints[1:])]))
                for delta in budgets:
                    expected = comb(n, s) if delta < dc else 1
                    assert component_count(vs, edges, delta) == expected
                    counts['graph_threshold_checks'] += 1
                counts['graph_cases'] += 1
                counts['independently_enumerated_edges'] += len(edges)

    # The eta <= 1/2 assumption matters: already six components arise here.
    vs = vectors(2, 1, F(9, 10))
    edges = graph_edges(vs, 1, F(9, 10))
    outside_range_components = component_count(vs, edges, F(9, 100))
    assert outside_range_components == 6
    result = {'status': 'PASS', 'arithmetic': 'fractions.Fraction, exact',
              'counts': counts,
              'eta_outside_theorem_counterexample': {
                  'n': 2, 's': 1, 'eta': '9/10', 'delta': '9/100',
                  'graph_component_count': outside_range_components},
              'scope': 'Finite identities, sharp witnesses, constructive paths, and polytope edge graphs; general results rely on the accompanying mathematical proofs.'}
    path = Path(__file__).with_name('verification_results.json')
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
