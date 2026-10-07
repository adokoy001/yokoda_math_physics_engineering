"""Exact finite checks supporting, not replacing, the written proofs.

Only Python's standard library is required. Outputs results beside this script.
"""
from fractions import Fraction as F
from itertools import combinations, permutations
from pathlib import Path
import json


def saturation_enumeration(n):
    faces = list(combinations(range(n), 3))
    idx = {t: i for i, t in enumerate(faces)}
    tetra = [sum(1 << idx[t] for t in combinations(v, 3))
             for v in combinations(range(n), 4)]
    witnesses = [[m & ~(1 << i) for m in tetra if m & (1 << i)]
                 for i in range(len(faces))]
    q = (n - 1) * (n - 2) // 2
    total = saturated = zero_three = 0
    designs = []
    for selection in combinations(range(len(faces)), q):
        total += 1
        mask = sum(1 << i for i in selection)
        if all((mask & t).bit_count() in (0, 3) for t in tetra):
            zero_three += 1
        if any(mask & t == t for t in tetra):
            continue
        if not all(mask & (1 << i) or any(mask & w == w for w in ws)
                   for i, ws in enumerate(witnesses)):
            continue
        saturated += 1
        common = set(range(n))
        for i in selection:
            common.intersection_update(faces[i])
        assert len(common) == 1
        designs.append(sorted(common)[0])
    assert sorted(designs) == list(range(n))
    return dict(n=n, q=q, total_designs=total,
                saturated_designs=saturated,
                zero_or_three_designs=zero_three,
                centers=sorted(designs))


def invert(matrix):
    n = len(matrix)
    a = [[F(x) for x in row] + [F(i == j) for j in range(n)]
         for i, row in enumerate(matrix)]
    for c in range(n):
        r = next((r for r in range(c, n) if a[r][c]), None)
        if r is None:
            return None
        a[c], a[r] = a[r], a[c]
        pivot = a[c][c]
        a[c] = [x / pivot for x in a[c]]
        for r in range(n):
            if r != c:
                multiple = a[r][c]
                a[r] = [x - multiple * y for x, y in zip(a[r], a[c])]
    return [row[n:] for row in a]


def audit_constant(n, selection):
    edges = list(combinations(range(1, n), 2))
    idx = {e: i for i, e in enumerate(edges)}

    def row(c):
        ans = [0] * len(edges)
        for a, b in zip(c, c[1:] + c[:1]):
            if a and b:
                ans[idx[tuple(sorted((a, b)))]] += 1 if a < b else -1
        return ans

    inverse = invert([row(t) for t in selection])
    assert inverse is not None
    worst, triangle_worst, cycles, maximizers = F(0), F(0), 0, []
    for size in range(3, n + 1):
        for subset in combinations(range(n), size):
            for tail in permutations(subset[1:]):
                c = (subset[0],) + tail
                if c[1] >= c[-1]:
                    continue
                cycles += 1
                coeffs = [sum(x * y[j] for x, y in zip(row(c), inverse))
                          for j in range(len(inverse))]
                value = sum(map(abs, coeffs)) / size
                if size == 3:
                    triangle_worst = max(triangle_worst, value)
                if value > worst:
                    worst, maximizers = value, []
                if value == worst:
                    maximizers.append(c)
    return dict(n=n, triangles=selection, cycles=cycles,
                constant=str(worst), triangle_lower_bound=str(triangle_worst),
                worst_cycle=maximizers[0], maximizing_cycles=len(maximizers),
                inverse_denominators=sorted({x.denominator for r in inverse for x in r}))


def main():
    # The ten faces form the classical six-vertex triangulation of RP^2.
    rp2 = [tuple(int(c) - 1 for c in s)
           for s in ('123', '124', '135', '146', '156',
                     '236', '245', '256', '345', '346')]
    report = dict(saturation=[saturation_enumeration(n) for n in (4, 5, 6)],
                  projective_plane=audit_constant(6, rp2))
    target = Path(__file__).with_name('graph_round2_results.json')
    target.write_text(json.dumps(report, indent=2) + '\n')
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    main()
