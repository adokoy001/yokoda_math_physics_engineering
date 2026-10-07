"""Independent finite audit of the randomized interval-support theorem."""
from itertools import combinations
from fractions import Fraction
from math import inf
import json
import numpy as np
from scipy.optimize import linprog


def subsets(n):
    return range(1 << n)


def pop(s):
    return s.bit_count()


def covers(t, intervals):
    return all(t & i for i in intervals)


def packing_values(intervals):
    vals = {(0, 0)}
    def rec(start, used, size):
        vals.add((size, pop(used)))
        for j in range(start, len(intervals)):
            if not used & intervals[j]:
                rec(j + 1, used | intervals[j], size + 1)
    rec(0, 0, 0)
    return vals


def greedy_mass(g, intervals, lam):
    xs = [lam] * g
    for iv in sorted(intervals, key=int.bit_length):
        deficit = max(Fraction(0), 1-sum(xs[i] for i in range(g) if iv >> i & 1))
        for i in range(g-1, -1, -1):
            if iv >> i & 1:
                added = min(deficit, 1-xs[i])
                xs[i] += added
                deficit -= added
        assert deficit == 0
    return xs


def costs(signatures, retained):
    m = max(signatures).bit_length()
    out = [inf] * (1 << m)
    for sub in subsets(len(signatures)):
        if sub & ~retained:
            continue
        union = 0
        for i, sig in enumerate(signatures):
            if sub >> i & 1:
                union |= sig
        e = union
        while True:
            out[e] = min(out[e], pop(sub))
            if not e:
                break
            e = (e - 1) & union
    return out


counts = dict(interval_families=0, budget_instances=0, canonical_instances=0,
              future_expectation_checks=0, sampler_supports=0,
              greedy_optimality_checks=0)
for g in range(1, 5):
    all_intervals = [sum(1 << i for i in range(a, b + 1))
                     for a in range(g) for b in range(a, g)]
    for fm in range(1, 1 << len(all_intervals)):
        intervals = [v for j, v in enumerate(all_intervals) if fm >> j & 1]
        counts['interval_families'] += 1
        packs = packing_values(intervals)
        q = max(k for k, length in packs)
        for lam0 in [Fraction(0), Fraction(1,7), Fraction(1,2), Fraction(6,7), Fraction(1)]:
            gx = greedy_mass(g, intervals, lam0)
            f = max(k+lam0*(g-length) for k, length in packs)
            assert sum(gx) == f, (g, intervals, lam0, gx, f)
            counts['greedy_optimality_checks'] += 1
        signatures = [sum(1 << j for j, v in enumerate(intervals) if v >> i & 1)
                      for i in range(g)]
        canonical = all(signatures) and all(
            signatures[i] & ~signatures[j]
            for i in range(g) for j in range(g) if i != j)
        all_t = [t for t in subsets(g) if covers(t, intervals)]
        for budget in range(q, g + 1):
            counts['budget_instances'] += 1
            allowed = [t for t in all_t if pop(t) <= budget]
            # Marginal LP in x_1,...,x_g,lambda.
            A, b = [], []
            for iv in intervals:
                A.append([-int(iv >> i & 1) for i in range(g)] + [0])
                b.append(-1)
            for i in range(g):
                A.append([-int(i == j) for j in range(g)] + [1])
                b.append(0)
            A.append([1] * g + [0]); b.append(budget)
            sol = linprog([0] * g + [-1], A_ub=A, b_ub=b,
                          bounds=[(0, 1)] * (g + 1), method='highs')
            assert sol.success
            lam = Fraction(float(sol.x[-1])).limit_denominator(100000)
            xs = [Fraction(float(x)).limit_denominator(100000) for x in sol.x[:-1]]
            formula = min([Fraction(1)] + [Fraction(budget-k, g-length)
                                          for k, length in packs if length < g])
            assert lam == formula, (g, intervals, budget, lam, formula)
            gx = greedy_mass(g, intervals, lam)
            assert sum(gx) == max(k+lam*(g-length) for k, length in packs) <= budget
            counts['greedy_optimality_checks'] += 1
            # Independent LP over all feasible supports, to test the marginal polytope.
            dA = [[-int(t >> i & 1) for t in allowed] + [1] for i in range(g)]
            ds = linprog([0] * len(allowed) + [-1], A_ub=dA, b_ub=[0] * g,
                         A_eq=[[1] * len(allowed) + [0]], b_eq=[1],
                         bounds=[(0, 1)] * (len(allowed)+1), method='highs')
            assert ds.success and abs(ds.x[-1] - float(lam)) < 1e-7
            # Exact rational systematic sampler: only fractional prefix endpoints matter.
            pref = [Fraction(0)]
            for x in xs: pref.append(pref[-1]+x)
            cuts = sorted({Fraction(0), Fraction(1)} | {s % 1 for s in pref})
            dist = {}
            for lo, hi in zip(cuts, cuts[1:]):
                theta = (lo+hi)/2
                t = 0
                for i in range(g):
                    if any(pref[i] < theta+z <= pref[i+1] for z in range(g+1)):
                        t |= 1 << i
                assert t in allowed, (g, intervals, xs, t)
                dist[t] = dist.get(t, Fraction(0)) + hi-lo
                counts['sampler_supports'] += 1
            assert sum(dist.values()) == 1
            assert all(sum(p for t, p in dist.items() if t >> i & 1) == xs[i]
                       for i in range(g))
            if canonical:
                counts['canonical_instances'] += 1
                rcost = costs(signatures, (1 << g)-1)
                tcost = {t: costs(signatures, t) for t in dist}
                maxloss = Fraction(0)
                for e in range(1, 1 << len(intervals)):
                    loss = sum(p*tcost[t][e] for t, p in dist.items()) / rcost[e]
                    maxloss = max(maxloss, loss)
                    counts['future_expectation_checks'] += 1
                assert maxloss == 2-lam, (g, intervals, budget, maxloss, lam)

counts['status'] = 'all passed'
print(json.dumps(counts, indent=2))
with open('randomized_audit_v4_results.json', 'w') as f:
    json.dump(counts, f, indent=2)
