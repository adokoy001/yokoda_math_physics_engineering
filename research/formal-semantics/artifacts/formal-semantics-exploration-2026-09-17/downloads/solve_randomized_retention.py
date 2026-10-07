"""Exact planar randomized retention: integer interval DP and rational rounding.

The solver uses only Python's standard library. Run this file to write the
six-candidate demonstration. verify_randomized_v4.py independently compares it
with explicit finite games, using scipy for the numerical LP comparison.
"""
from fractions import Fraction
from bisect import bisect_left
from pathlib import Path
import json


def canonical_intervals(candidates, demands):
    """Return maximal-signature representatives and their demand intervals."""
    assert candidates and demands
    by_signature = {}
    for index, candidate in enumerate(candidates):
        signature = sum(1 << j for j, d in enumerate(demands)
                        if all(a <= b for a, b in zip(d, candidate)))
        if signature:
            by_signature.setdefault(signature, index)
    full = (1 << len(demands)) - 1
    union = 0
    for signature in by_signature:
        union |= signature
    assert union == full, 'The original candidates must cover all demands.'
    maximal = [s for s in by_signature
               if not any(s != t and s & t == s for t in by_signature)]
    reps = sorted((by_signature[s] for s in maximal), key=lambda i: candidates[i])
    assert all(candidates[reps[j]][0] < candidates[reps[j+1]][0]
               and candidates[reps[j]][1] > candidates[reps[j+1]][1]
               for j in range(len(reps)-1)), 'This solver is for two resources.'
    intervals = []
    for d in demands:
        indices = [j for j, index in enumerate(reps)
                   if all(a <= b for a, b in zip(d, candidates[index]))]
        assert indices == list(range(indices[0], indices[-1]+1))
        intervals.append((indices[0], indices[-1]))
    return reps, sorted(set(intervals))


def packing_lengths(g, intervals):
    """ell[k] = minimum total length of k disjoint demand intervals."""
    ordered = sorted(set(intervals), key=lambda v: (v[1], v[0]))
    rights = [r for l, r in ordered]
    infinity = g + 1
    rows = [[0] + [infinity] * g]
    for j, (left, right) in enumerate(ordered):
        previous = bisect_left(rights, left, 0, j)
        row = rows[-1].copy()
        for k in range(1, g+1):
            if rows[previous][k-1] < infinity:
                row[k] = min(row[k], right-left+1+rows[previous][k-1])
        rows.append(row)
    return [v for v in rows[-1] if v < infinity]


def systematic_distribution(x):
    """Finite rational mixture equivalent to a uniform systematic shift."""
    prefix = [Fraction(0)]
    for value in x:
        assert 0 <= value <= 1
        prefix.append(prefix[-1] + value)
    cuts = sorted({Fraction(0), Fraction(1)} |
                  {s - s.numerator // s.denominator for s in prefix})
    distribution = {}
    for lower, upper in zip(cuts, cuts[1:]):
        theta = (lower + upper) / 2
        selected = []
        for i, (left, right) in enumerate(zip(prefix, prefix[1:])):
            a, b = left-theta, right-theta
            if b.numerator//b.denominator > a.numerator//a.denominator:
                selected.append(i)
        selected = tuple(selected)
        distribution[selected] = distribution.get(selected, Fraction(0)) + upper-lower
    assert sum(distribution.values()) == 1
    return distribution


def solve_intervals(g, intervals, budget):
    assert isinstance(budget, int) and 0 <= budget <= g
    assert all(0 <= l <= r < g for l, r in intervals)
    ell = packing_lengths(g, intervals)
    q = len(ell)-1
    if budget < q:
        raise ValueError('Storage is below the minimum current cover size.')
    candidates = [(Fraction(1), None)]
    candidates += [(Fraction(budget-k, g-length), k)
                   for k, length in enumerate(ell) if length < g]
    lam, bottleneck_k = min(candidates, key=lambda item: item[0])
    x = [lam] * g
    # Greedy minimum-mass interval cover with lower bounds x_i >= lam.
    for left, right in sorted(set(intervals), key=lambda v: (v[1], v[0])):
        deficit = 1-sum(x[left:right+1])
        for i in range(right, left-1, -1):
            if deficit <= 0:
                break
            add = min(deficit, 1-x[i])
            x[i] += add
            deficit -= add
        assert deficit <= 0
    assert sum(x) <= budget
    mixture = systematic_distribution(x)
    observed = [Fraction(0)] * g
    for selected, probability in mixture.items():
        assert len(selected) <= budget
        assert all(any(left <= i <= right for i in selected) for left, right in intervals)
        for i in selected:
            observed[i] += probability
    assert observed == x
    return {'q': q, 'g': g, 'budget': budget, 'ell': ell, 'lambda': lam,
            'ratio': 2-lam, 'marginals': x, 'mixture': mixture,
            'bottleneck_k': bottleneck_k}


def solve(candidates, demands, budget):
    assert all(len(r) == 2 for r in candidates)
    reps, intervals = canonical_intervals(candidates, demands)
    result = solve_intervals(len(reps), intervals, budget)
    result.update({'representatives': reps, 'intervals': intervals})
    return result


def serializable(result):
    return {**{key: value for key, value in result.items()
               if key not in ('lambda', 'ratio', 'marginals', 'mixture')},
            'lambda': str(result['lambda']), 'ratio': str(result['ratio']),
            'marginals': [str(v) for v in result['marginals']],
            'mixture': [{'indices': list(s), 'probability': str(p)}
                        for s, p in result['mixture'].items()]}


if __name__ == '__main__':
    R = [(i, 7-i) for i in range(1, 7)]
    D = [(i, 6-i) for i in range(1, 6)] + [R[0], R[-1]]
    output = {'candidates': R, 'demands': D,
              'solutions': [serializable(solve(R, D, B)) for B in range(4, 7)]}
    path = Path(__file__).with_name('randomized_demo_v4.json')
    path.write_text(json.dumps(output, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(output, ensure_ascii=False))
