"""Exact checks for nonintegral cube sections and sharp rank gaps.

Only Python standard library; rational/int arithmetic throughout.
This verifies finite cases, and does not purport to prove the continuum theorem.
"""
from fractions import Fraction as F
from itertools import combinations, combinations_with_replacement
from math import comb
import json
from pathlib import Path


def vertex_graph(n, m, r):
    vertices = []
    for A in combinations(range(n), m):
        for j in range(n):
            if j not in A:
                x = tuple(F(1) if i in A else r if i == j else F(0)
                          for i in range(n))
                vertices.append(x)
    index = {v: i for i, v in enumerate(vertices)}
    qmax = m + r*r
    edges = []
    # Generate by swapping the sole fractional coordinate with a 0 or 1.
    # Edge weights are independently computed from midpoint squared norms.
    for vi, v in enumerate(vertices):
        j = v.index(r)
        for k in range(n):
            if k == j:
                continue
            w = list(v)
            w[j], w[k] = w[k], w[j]
            wi = index[tuple(w)]
            if wi > vi:
                midpoint = [(x+y)/2 for x, y in zip(v, w)]
                weight = qmax - sum(x*x for x in midpoint)
                edges.append((vi, wi, weight))
    return vertices, edges


def graph_components(vcount, edges, E):
    adjacency = [[] for _ in range(vcount)]
    for i, j, weight in edges:
        if weight <= E:
            adjacency[i].append(j)
            adjacency[j].append(i)
    unseen = set(range(vcount))
    count = 0
    while unseen:
        todo = [unseen.pop()]
        count += 1
        while todo:
            for j in adjacency[todo.pop()]:
                if j in unseen:
                    unseen.remove(j)
                    todo.append(j)
    return count


def prediction(n, m, r, E):
    a, b = r*r/2, (1-r)**2/2
    if E < a and E < b:
        return comb(n, m)*(n-m)
    if E >= a and E < b:
        return comb(n, m)
    if E < a and E >= b:
        return comb(n, m+1)
    return 1


def check_graphs():
    cases = vertices_checked = edges_checked = 0
    examples = []
    for n in range(1, 11):
        for m in range(n):
            for r in [F(1,10), F(1,4), F(1,2), F(3,4), F(9,10)]:
                vertices, edges = vertex_graph(n, m, r)
                vertices_checked += len(vertices)
                edges_checked += len(edges)
                a, b = r*r/2, (1-r)**2/2
                Emax = m+r*r-(m+r)**2/n
                landmarks = sorted(set([F(0), a, b, Emax]))
                probes = set(landmarks)
                probes.update((x+y)/2 for x,y in zip(landmarks,landmarks[1:]))
                for E in sorted(probes):
                    if 0 <= E <= Emax:
                        actual = graph_components(len(vertices), edges, E)
                        expected = prediction(n, m, r, E)
                        assert actual == expected, (n,m,r,E,actual,expected)
                        cases += 1
                        if n == 4 and m == 1 and r == F(1,4):
                            examples.append(dict(E=str(E), components=actual))
    return dict(level_graph_cases=cases, vertex_records=vertices_checked,
                edge_records=edges_checked, example_n4_S5over4=examples)


def check_rank_gaps():
    # Permutation invariance permits testing only sorted grid vectors.
    denominator = 10
    vectors = upper_tests = lower_tests = 0
    for n in range(2, 11):
        for ascending in combinations_with_replacement(range(denominator+1), n):
            numer = sum(ascending)
            m, rem = divmod(numer, denominator)
            if not rem:
                continue
            a = list(reversed(ascending))
            E_num = m*denominator**2 + rem**2 - sum(x*x for x in a)
            assert E_num >= 0
            if m >= 1:
                gap_num = a[m-1] - a[m]
                assert gap_num**2 >= (denominator-rem)**2 - 2*E_num, a
                upper_tests += 1
            if m+1 < n:
                gap_num = a[m] - a[m+1]
                assert gap_num**2 >= rem**2 - 2*E_num, a
                lower_tests += 1
            vectors += 1
    return dict(sorted_grid_vectors=vectors, upper_rank_inequalities=upper_tests,
                lower_rank_inequalities=lower_tests, grid_denominator=denominator)


def check_sharpness():
    count = 0
    for n in range(2, 11):
        for m in range(n):
            for r in [F(1,10), F(1,4), F(1,2), F(3,4), F(9,10)]:
                S, qmax = m+r, m+r*r
                for mode in ['upper', 'lower']:
                    if mode == 'upper' and m == 0:
                        continue
                    if mode == 'lower' and m+1 >= n:
                        continue
                    t = 1-r if mode == 'upper' else r
                    k = m if mode == 'upper' else m+1
                    for h in range(11):
                        d = t*F(h,10)
                        pair_sum = 1+r if mode == 'upper' else r
                        x = [F(1)]*(k-1) + [(pair_sum+d)/2,(pair_sum-d)/2]
                        x += [F(0)]*(n-len(x))
                        E = qmax-sum(v*v for v in x)
                        assert len(x) == n and sum(x) == S
                        assert all(0 <= v <= 1 for v in x)
                        assert x == sorted(x, reverse=True)
                        assert x[k-1]-x[k] == d
                        assert 2*E == t*t-d*d
                        count += 1
                    # From the tied extremizer to the uniform vector,
                    # the gap remains zero and E covers [threshold,Emax].
                    y = [F(1)]*(k-1) + [pair_sum/2,pair_sum/2]
                    y += [F(0)]*(n-len(y))
                    threshold = t*t/2
                    Emax = qmax-S*S/n
                    for h in range(11):
                        lam = F(h,10)
                        x = [(1-lam)*v+lam*S/n for v in y]
                        E = qmax-sum(v*v for v in x)
                        assert x[k-1] == x[k]
                        assert E == Emax-(1-lam)**2*(Emax-threshold)
                        count += 1
    return dict(exact_extremizer_checks=count)


if __name__ == '__main__':
    result = dict(status='all_passed', arithmetic='exact integers and fractions',
                  graphs=check_graphs(), margins=check_rank_gaps(),
                  sharpness=check_sharpness())
    path = Path(__file__).with_name('verification_results.json')
    path.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False, indent=2))
