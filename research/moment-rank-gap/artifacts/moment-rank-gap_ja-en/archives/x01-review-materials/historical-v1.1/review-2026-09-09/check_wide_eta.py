#!/usr/bin/env python3
"""Exact finite audit of wide-band component counts; not a general proof.

Vertices are obtained from active cube/band constraints. Edges are detected
from the rank of common active constraints, independently of the proposed
edge-type classification. Fraction arithmetic is used throughout.
"""
from fractions import Fraction as F
from itertools import product
from math import comb
from pathlib import Path
import json


def main():
    checks = 0
    graph_results = []
    for n in range(2, 7):
        for s in range(1, n):
            for eta in [F(3, 5), F(7, 10), F(3, 4), F(9, 10)]:
                low, high = s - eta, s + eta
                verts = set()
                for v in product([F(0), F(1)], repeat=n):
                    if low <= sum(v) <= high:
                        verts.add(v)
                for free in range(n):
                    for fixed in product([F(0), F(1)], repeat=n - 1):
                        for bound in (low, high):
                            f = bound - sum(fixed)
                            if 0 <= f <= 1:
                                verts.add(fixed[:free] + (f,) + fixed[free:])
                vs = sorted(verts)
                ds = [sum(t * (1 - t) for t in v) for v in vs]
                edges = []
                for i, a in enumerate(vs):
                    for j in range(i + 1, len(vs)):
                        b = vs[j]
                        common_box = sum(x == y and x in (0, 1)
                                         for x, y in zip(a, b))
                        common_cut = (sum(a) == sum(b)
                                      and sum(a) in (low, high))
                        # Coordinate normals are independent; a common sum
                        # normal adds one rank because the vertices differ.
                        if common_box + int(common_cut) == n - 1:
                            w = [y - x for x, y in zip(a, b)]
                            q = sum(t * t for t in w)
                            linear = sum(t * (1 - 2 * x)
                                         for t, x in zip(w, a))
                            t = max(F(0), min(F(1), linear / (2 * q)))
                            maximum = ds[i] + linear * t - q * t * t
                            edges.append((i, j, maximum))
                k, c, h, d = (eta * (1 - eta), (1 - eta * eta) / 2,
                              F(1, 4), eta - eta * eta / 2)
                edge_values = {w for i, j, w in edges}
                expected_values = {h, c} if n == 2 else {h, c, d}
                assert edge_values == expected_values, (n, s, eta, edge_values)
                levels = sorted({F(0), k, c, h, d, F(n, 4) + 1})
                levels = sorted(set(levels + [(a + b) / 2
                                               for a, b in zip(levels, levels[1:])]))
                N = comb(n, s)
                A = (n + 1) * N
                B = N + comb(n, s - 1) + comb(n, s + 1)
                assert len(vs) == A, (n, s, eta, len(vs), A)
                counts = []
                for delta in levels:
                    parents = list(range(len(vs)))

                    def root(i):
                        while i != parents[i]:
                            parents[i] = parents[parents[i]]
                            i = parents[i]
                        return i

                    for i, j, w in edges:
                        if w <= delta:
                            parents[root(i)] = root(j)
                    actual = len({root(i) for i, v in enumerate(vs)
                                  if ds[i] <= delta})
                    if delta < k:
                        expected = N
                    elif delta < min(c, h):
                        expected = A
                    elif delta >= max(c, h):
                        expected = 1
                    elif c < h:
                        expected = B
                    else:
                        expected = N
                    assert actual == expected, (n, s, eta, delta, actual, expected)
                    checks += 1
                    counts.append({"delta": str(delta), "actual": actual,
                                   "expected": expected})
                graph_results.append({
                    "n": n, "s": s, "eta": str(eta), "vertices": len(vs),
                    "edges": len(edges),
                    "thresholds": {"k": str(k), "c": str(c),
                                   "h": str(h), "d": str(d)},
                    "checks": counts,
                })
    result = {
        "status": "PASS", "date": "2026 09 09",
        "scope": "Exact finite rational polytope/graph audit, not a general proof or Lean formalization.",
        "arithmetic": "Python fractions.Fraction",
        "edge_detection": "Rank n-1 of common active cube/band constraints",
        "rational_geometries_checked": len(graph_results),
        "threshold_and_interval_counts_checked": checks,
        "largest_graph_vertices": max(g["vertices"] for g in graph_results),
        "irrational_transition_eta": "1/sqrt(2) handled symbolically in the proof, not sampled here",
        "graphs": graph_results,
    }
    out = Path(__file__).with_name("wide_eta_check.json")
    out.write_text(json.dumps(result, indent=2, ensure_ascii=False) + "\n",
                   encoding="utf-8")
    print(json.dumps({k: v for k, v in result.items() if k != "graphs"},
                     ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
