"""Independent finite-game audit of exact randomized planar retention.

The reference game enumerates all original feasible retained portfolios and all
future demand sets, identifying only sets with identical coverage requirements.
Its optimum is a numerical scipy LP; the produced sampler is checked exactly
with Fraction. The solver itself uses neither scipy nor this reference game.
"""
from fractions import Fraction
from itertools import combinations
from pathlib import Path
import json
import random

import numpy as np
from scipy.optimize import linprog

from solve_randomized_retention import solve


def data(candidates, demands):
    signatures = [sum(1 << j for j, d in enumerate(demands)
                      if d[0] <= r[0] and d[1] <= r[1]) for r in candidates]
    supports = [sum(1 << i for i, signature in enumerate(signatures)
                    if signature >> j & 1) for j in range(len(demands))]
    assert all(supports)
    return signatures, supports


def normalize_future(mask, supports):
    """Keep one demand per inclusion-minimal candidate-support set."""
    indices = [j for j in range(len(supports)) if mask >> j & 1]
    return sum(1 << j for j in indices
               if not any(k != j and supports[k] & supports[j] == supports[k]
                          and (supports[k] != supports[j] or k < j)
                          for k in indices))


def future_states(supports):
    states = {0}
    for j in range(len(supports)):
        states |= {normalize_future(mask | (1 << j), supports) for mask in states}
    # Independently check the incremental enumeration against every raw future
    # in the small cases. Normalization preserves every portfolio's feasibility.
    if len(supports) <= 9:
        assert states == {normalize_future(mask, supports)
                          for mask in range(1 << len(supports))}
    return sorted(states)


def reference(candidates, demands):
    signatures, supports = data(candidates, demands)
    states = future_states(supports)
    index = {mask: j for j, mask in enumerate(states)}
    n = len(candidates)
    infinity = n + 1
    rows = [[0 if mask == 0 else infinity for mask in states]]
    unions = [0]
    reduced = [[index[mask & ~s] for mask in states] for s in signatures]
    for allowed in range(1, 1 << n):
        low = allowed & -allowed
        candidate = low.bit_length() - 1
        previous = allowed ^ low
        row = rows[previous]
        rows.append([min(row[j], 1 + row[reduced[candidate][j]])
                     for j in range(len(states))])
        unions.append(unions[previous] | signatures[candidate])
    full = (1 << len(demands)) - 1
    feasible = [mask for mask, cov in enumerate(unions) if cov == full]
    q = min(mask.bit_count() for mask in feasible)
    sigs = set(signatures) - {0}
    g = sum(not any(s != t and s & t == s for t in sigs) for s in sigs)
    return signatures, states, rows, feasible, q, g


def audit_case(candidates, demands, budgets=None, expected=None):
    signatures, states, rows, feasible, q, g = reference(candidates, demands)
    budgets = list(range(q, g + 1)) if budgets is None else budgets
    summary = []
    n = len(candidates)
    fullmask = (1 << n) - 1
    full_demands = (1 << len(demands)) - 1
    nonempty = [j for j, mask in enumerate(states) if mask]
    for budget in budgets:
        result = solve(candidates, demands, budget)
        assert result['q'] == q and result['g'] == g
        choices = [mask for mask in feasible if mask.bit_count() <= budget]
        payoff = np.array([[rows[mask][j] / rows[fullmask][j] for mask in choices]
                           for j in nonempty], dtype=float)
        lp = linprog(np.r_[np.zeros(len(choices)), 1.0],
                     A_ub=np.c_[payoff, -np.ones(len(nonempty))],
                     b_ub=np.zeros(len(nonempty)),
                     A_eq=np.array([[1.0] * len(choices) + [0.0]]),
                     b_eq=np.array([1.0]),
                     bounds=[(0, None)] * len(choices) + [(1, None)],
                     method='highs')
        assert lp.success, lp.message
        error = abs(lp.fun - float(result['ratio']))
        assert error < 1e-8, (candidates, demands, budget, result, lp.fun)
        if expected is not None:
            assert result['ratio'] == expected(budget)

        # Original candidate indices, including dominated candidates, are kept
        # in the reference; the solver may canonicalize to maximal signatures.
        mixture = {}
        observed = [Fraction(0)] * g
        for selected, probability in result['mixture'].items():
            assert probability > 0 and len(selected) <= budget
            mask = sum(1 << result['representatives'][i] for i in selected)
            cov = 0
            for i in range(n):
                if mask >> i & 1:
                    cov |= signatures[i]
            assert cov == full_demands
            mixture[mask] = mixture.get(mask, Fraction(0)) + probability
            for i in selected:
                observed[i] += probability
        assert sum(mixture.values()) == 1
        assert observed == result['marginals']
        assert min(observed) == result['lambda']
        exact_worst = max(sum(p * rows[mask][j] for mask, p in mixture.items())
                          / rows[fullmask][j] for j in nonempty)
        assert exact_worst == result['ratio']
        if budget < g:
            assert all(max(Fraction(rows[mask][j], rows[fullmask][j])
                           for j in nonempty) == 2 for mask in mixture)
        summary.append({'budget': budget, 'ratio': str(result['ratio']),
                        'original_portfolios': len(choices),
                        'future_payoff_classes': len(nonempty),
                        'lp_error': error})
    return {'candidates': n, 'demands': len(demands), 'q': q, 'g': g,
            'budgets': summary,
            'dominated_candidates': any(i != j and r != s and r[0] <= s[0] and r[1] <= s[1]
                                        for i, r in enumerate(candidates)
                                        for j, s in enumerate(candidates)),
            'duplicate_signatures': len(set(signatures)) < len(signatures)}


def random_cases():
    rng = random.Random(9172026)
    cases = []
    # Arbitrary geometry, including comparable candidates and empty signatures.
    grid = [(x, y) for x in range(1, 8) for y in range(1, 8)]
    for _ in range(35):
        candidates = rng.sample(grid, rng.randint(3, 8))
        possible = [d for d in grid if any(d[0] <= r[0] and d[1] <= r[1] for r in candidates)]
        demands = rng.sample(possible, min(len(possible), rng.randint(3, 8)))
        cases.append((candidates, demands))
    # Richer incomparable frontiers with random interval demands; optional
    # dominated extra candidates force an audit of canonicalization.
    for _ in range(65):
        g = rng.randint(3, 7)
        candidates = [(2*j, 2*(g+1-j)) for j in range(1, g+1)]
        intervals = [(i, j) for i in range(g) for j in range(i, g)]
        picked = rng.sample(intervals, rng.randint(3, min(8, len(intervals))))
        demands = [(candidates[i][0], candidates[j][1]) for i, j in picked]
        if rng.random() < 0.7:
            r = rng.choice(candidates)
            extra = (r[0]-1, r[1]-1)
            candidates.append(extra)
        cases.append((candidates, demands))
    return cases


def main():
    groups = {'random': [], 'exhaustive_small_interval': [], 'universal_sharp': [], 'demo': []}
    for candidates, demands in random_cases():
        groups['random'].append(audit_case(candidates, demands))
    # Every nonempty interval family on each ordered frontier of size 1..3.
    for g in range(1, 4):
        candidates = [(j, g+1-j) for j in range(1, g+1)]
        intervals = [(i, j) for i in range(g) for j in range(i, g)]
        for family in range(1, 1 << len(intervals)):
            demands = [(candidates[i][0], candidates[j][1])
                       for k, (i, j) in enumerate(intervals) if family >> k & 1]
            groups['exhaustive_small_interval'].append(audit_case(candidates, demands))
    for g in range(3, 9):
        for q in range(2, g):
            m = g-q+2
            candidates = [(j, g+1-j) for j in range(1, g+1)]
            demands = sorted({(1, g+1-i) for i in range(1, m+1)}
                             | {(i, g+1-m) for i in range(1, m+1)}
                             | {candidates[j-1] for j in range(m+1, g+1)})
            result = audit_case(candidates, demands,
                                expected=lambda B, g=g, q=q: 1+Fraction(g-B, g-q))
            assert result['g'] == g and result['q'] == q
            groups['universal_sharp'].append(result)
    candidates = [(i, 7-i) for i in range(1, 7)]
    demands = [(i, 6-i) for i in range(1, 6)] + [candidates[0], candidates[-1]]
    demo = audit_case(candidates, demands)
    assert [b['ratio'] for b in demo['budgets']] == ['3/2', '5/4', '1']
    groups['demo'].append(demo)
    all_cases = [case for cases in groups.values() for case in cases]
    all_budgets = [b for case in all_cases for b in case['budgets']]
    result = {'seed': 9172026,
              'summary': {'instances': len(all_cases), 'finite_game_LPs': len(all_budgets),
                          'exact_sampler_audits': len(all_budgets),
                          'max_LP_absolute_error': max(b['lp_error'] for b in all_budgets),
                          'dominated_candidate_instances': sum(c['dominated_candidates'] for c in all_cases),
                          'duplicate_signature_instances': sum(c['duplicate_signatures'] for c in all_cases),
                          'original_portfolios_compared': sum(b['original_portfolios'] for b in all_budgets),
                          'future_payoff_constraints_compared': sum(b['future_payoff_classes'] for b in all_budgets)},
              'groups': {name: {'instances': len(cases),
                               'LPs': sum(len(c['budgets']) for c in cases),
                               'details': cases} for name, cases in groups.items()}}
    Path(__file__).with_name('randomized_v4_results.json').write_text(
        json.dumps(result, indent=2)+'\n', encoding='utf-8')
    print(json.dumps(result['summary'], indent=2))
    print(json.dumps({k: {'instances': v['instances'], 'LPs': v['LPs']}
                      for k, v in result['groups'].items()}, indent=2))


if __name__ == '__main__':
    main()
