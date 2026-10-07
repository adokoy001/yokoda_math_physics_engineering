"""Finite verification of the 2D future-recompression theorem.

Standard library only. Exhaustive interval incidence families on <=5 points,
plus independent numeric domination examples in dimension 2 and 3.
These checks supplement, and do not replace, the general proof.
"""
import json
from itertools import combinations
from fractions import Fraction


def exhaustive_intervals(max_n=5):
    rows = []
    for n in range(1, max_n + 1):
        intervals = [sum(1 << i for i in range(a, b + 1))
                     for a in range(n) for b in range(a, n)]
        coverage = [sum(1 << j for j, interval in enumerate(intervals)
                        if points & interval) for points in range(1 << n)]
        families = 0
        feasible_retained = 0
        max_ratio = 0.0
        for family in range(1, 1 << len(intervals)):
            families += 1
            # Compute the exact optimum inside EVERY allowed candidate subset.
            best = [points.bit_count() if coverage[points] & family == family
                    else n + 1 for points in range(1 << n)]
            for bit in range(n):
                for points in range(1 << n):
                    if points & (1 << bit):
                        best[points] = min(best[points], best[points ^ (1 << bit)])
            unrestricted = best[-1]
            for retained in range(1 << n):
                if coverage[retained] & family != family:
                    continue
                feasible_retained += 1
                assert unrestricted <= best[retained] <= 2 * unrestricted
                max_ratio = max(max_ratio, best[retained] / unrestricted)
        rows.append(dict(points=n, interval_types=len(intervals),
                         nonempty_families=families,
                         feasible_family_retained_pairs=feasible_retained,
                         worst_ratio=max_ratio))
    return rows


def dominates(r, d):
    return all(a >= b for a, b in zip(r, d))


def general_replacement_identity():
    # ALL incidence matrices: 3 candidate representatives, 3 demands.
    from itertools import product
    cases = 0
    future_subsets = 0
    for stars in product(range(8), repeat=3):
        covers = []
        for selected in range(8):
            cover = 0
            for i in range(3):
                if selected & (1 << i):
                    cover |= stars[i]
            covers.append(cover)
        if covers[7] != 7:
            continue
        def opt(available, demands):
            return min(selected.bit_count() for selected in range(8)
                       if selected & ~available == 0
                       and covers[selected] & demands == demands)
        maximal = {s for s in stars if not any(s != t and s & ~t == 0 for t in stars)}
        for retained in range(1, 8):
            if covers[retained] != 7:
                continue
            costs = [opt(retained, demands) for demands in range(8)]
            local = max(costs[star] for star in stars)
            global_loss = max(Fraction(costs[demands], opt(7, demands))
                              for demands in range(1, 8))
            assert global_loss == local
            future_safe = all(any(stars[j] & s == s for j in range(3)
                                 if retained & (1 << j)) for s in stars)
            assert future_safe == (local == 1)
            if future_safe:
                assert retained.bit_count() >= len(maximal)
            cases += 1
            future_subsets += 7
    return dict(incidence_matrices_examined=512,
                feasible_retained_cases=cases, future_subsets_checked=future_subsets)


def optimal_subsets(candidates, demands):
    for size in range(len(candidates) + 1):
        feasible = [list(ids) for ids in combinations(range(len(candidates)), size)
                    if all(any(dominates(candidates[i], d) for i in ids)
                           for d in demands)]
        if feasible:
            return size, feasible
    raise ValueError('uncovered demand')


def explicit_examples():
    r2 = [(1, 3), (2, 2), (3, 1)]
    future2 = [(1, 2), (2, 1)]
    initial2 = [r2[0], r2[2]] + future2
    assert optimal_subsets(r2, initial2) == (2, [[0, 2]])
    assert optimal_subsets(r2, future2)[0] == 1
    assert optimal_subsets([r2[0], r2[2]], future2)[0] == 2
    rows = []
    for m in range(2, 10):
        p = (m, m, 2)
        q = [(i, m + 1 - i, 3) for i in range(1, m + 1)]
        future = [(i, m + 1 - i, 1) for i in range(1, m + 1)]
        candidates = [p] + q
        assert all(not dominates(a, b) for i, a in enumerate(candidates)
                   for j, b in enumerate(candidates) if i != j)
        size, ids = optimal_subsets(candidates, q + future)
        assert (size, ids) == (m, [list(range(1, m + 1))])
        assert optimal_subsets(candidates, future)[0] == 1
        assert optimal_subsets(q, future)[0] == m
        # Realize demand narrowing by a positive-cost branch prefix.
        prefix = (1, 1, 1)
        shifted = [tuple(x + y for x, y in zip(r, prefix)) for r in candidates]
        for d in q + future:
            translated_d = tuple(x + y for x, y in zip(d, prefix))
            assert [dominates(r, d) for r in candidates] == [
                dominates(r, translated_d) for r in shifted]
        rows.append(dict(m=m, initial_unique_minimum=m,
                         future_with_all_candidates=1, future_after_pruning=m))
    return dict(two_dimensional=dict(initial_unique_minimum=2,
                future_with_all_candidates=1, future_after_pruning=2),
                three_dimensional=rows)


if __name__ == '__main__':
    print(json.dumps(dict(exhaustive=exhaustive_intervals(),
                         examples=explicit_examples(),
                         general_identity=general_replacement_identity()), indent=2))
