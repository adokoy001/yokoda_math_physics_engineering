#!/usr/bin/env python3
"""Independent finite verification of the v2 retention bounds.

Unit-price cover problems are solved by enumerating all candidate subsets.
For each retained portfolio, all demand subsets are then solved via a
superset-min transform. No claimed inequality is used by the optimizer.
Standard library only. Default output is stdout; no files are changed.
Run: python verify_v2.py --output fresh_results.json
An existing output file is never overwritten.
"""
from __future__ import annotations
import itertools
import argparse
import json
import random
import time
from pathlib import Path

SEED = 20260917
RANDOM_INSTANCES = 300
COUNTS: dict[str, int] = {}


def inc(name: str, number: int = 1) -> None:
    COUNTS[name] = COUNTS.get(name, 0) + number


def require(value: bool, label: str, **context) -> None:
    if not value:
        raise AssertionError((label, context))


def covers_data(signatures, m):
    n = len(signatures)
    unions = [0] * (1 << n)
    sizes = [0] * (1 << n)
    for selected in range(1, 1 << n):
        low = selected & -selected
        previous = selected ^ low
        unions[selected] = unions[previous] | signatures[low.bit_length() - 1]
        sizes[selected] = sizes[previous] + 1
    return unions, sizes


def all_portfolio_optima(signatures, m):
    """Return exact optima[retained_mask][demand_mask]."""
    n = len(signatures)
    unions, sizes = covers_data(signatures, m)
    unreachable = n + 1
    rows = []
    for retained in range(1 << n):
        exact = [unreachable] * (1 << m)
        selected = retained
        while True:
            covered = unions[selected]
            exact[covered] = min(exact[covered], sizes[selected])
            if not selected:
                break
            selected = (selected - 1) & retained
        # Any superset of the requested demand set also covers that request.
        for j in range(m):
            bit = 1 << j
            for e in range(1 << m):
                if not e & bit:
                    exact[e] = min(exact[e], exact[e | bit])
        rows.append(exact)
    return rows, unions, sizes


def incidence_signatures(candidates, demands):
    return [sum(1 << j for j, d in enumerate(demands)
                if all(x <= y for x, y in zip(d, r))) for r in candidates]


def exact_problem(signatures, m, demand_mask, retained=None):
    """Enumerate every candidate subset; no demand-subset table required."""
    n = len(signatures)
    if retained is None:
        retained = (1 << n) - 1
    unions, sizes = covers_data(signatures, m)
    minimum = n + 1
    solutions = []
    selected = retained
    while True:
        if unions[selected] & demand_mask == demand_mask:
            size = sizes[selected]
            if size < minimum:
                minimum, solutions = size, [selected]
            elif size == minimum:
                solutions.append(selected)
        if not selected:
            break
        selected = (selected - 1) & retained
    return minimum, solutions


def exhaustive_incidence():
    n, m = 3, 4
    full_d = (1 << m) - 1
    for signatures in itertools.product(range(1 << m), repeat=n):
        inc('incidence_systems_enumerated')
        if signatures[0] | signatures[1] | signatures[2] != full_d:
            continue
        inc('incidence_feasible_systems')
        opt, unions, sizes = all_portfolio_optima(signatures, m)
        full_r = (1 << n) - 1
        q = opt[full_r][full_d]
        minima = [t for t in range(1 << n)
                  if unions[t] == full_d and sizes[t] == q]
        unique = len(minima) == 1
        if unique:
            inc('incidence_unique_optimum_systems')
        for t in minima:
            inc('incidence_initial_minimum_portfolios')
            for e in range(1, 1 << m):
                h = m - e.bit_count()
                k, future = opt[full_r][e], opt[t][e]
                require(future <= (h + 1) * k, 'general h+1',
                        signatures=signatures, retained=t, e=e, h=h)
                inc('incidence_general_h_plus_1_checks')
                # The h bound applies for h>=1; h=0 has ratio exactly one.
                if unique:
                    require(future <= max(1, h) * k, 'unique h',
                            signatures=signatures, retained=t, e=e, h=h)
                    inc('incidence_unique_h_checks')
    return {'n_candidates': n, 'n_demands': m,
            'includes_empty_and_duplicate_signatures': True}


def random_planar():
    rng = random.Random(SEED)
    grid = list(itertools.product(range(1, 7), repeat=2))
    sample_records = []
    for trial in range(RANDOM_INSTANCES):
        n = rng.randint(2, 7)
        candidates = sorted(rng.sample(grid, n))
        pool = [d for d in grid if any(all(x <= y for x, y in zip(d, r))
                                      for r in candidates)]
        m = rng.randint(2, min(7, len(pool)))
        demands = sorted(rng.sample(pool, m))
        signatures = incidence_signatures(candidates, demands)
        opt, unions, sizes = all_portfolio_optima(signatures, m)
        full_r, full_d = (1 << n) - 1, (1 << m) - 1
        q = opt[full_r][full_d]
        minima = [t for t in range(1 << n)
                  if unions[t] == full_d and sizes[t] == q]
        unique = len(minima) == 1
        inc('planar_random_instances')
        if unique:
            inc('planar_unique_optimum_instances')
        # A strict sum-increasing score ensures each selected dominator is maximal.
        replacement = []
        for old in candidates:
            admissible = [j for j, new in enumerate(candidates)
                          if all(x <= y for x, y in zip(old, new))]
            replacement.append(max(admissible,
                                   key=lambda j: (sum(candidates[j]), candidates[j])))
        pareto = {i for i, r in enumerate(candidates)
                  if not any(i != j and all(x <= y for x, y in zip(r, s))
                             for j, s in enumerate(candidates))}
        for t in range(1, 1 << n):
            if unions[t] != full_d:
                continue
            inc('planar_feasible_portfolios')
            initial_min = sizes[t] == q
            if initial_min:
                inc('planar_initial_minimum_portfolios')
            s = sizes[t] - q
            normalized = 0
            for i in range(n):
                if t >> i & 1:
                    j = replacement[i]
                    require(j in pareto, 'normalization lands on Pareto frontier')
                    normalized |= 1 << j
            require(sizes[normalized] <= sizes[t], 'normalization cardinality')
            require(unions[normalized] == full_d, 'normalization feasibility')
            observed_num, observed_den = 0, 1
            for e in range(1, 1 << m):
                k, future = opt[full_r][e], opt[t][e]
                require(future <= min(sizes[t], s + 3) * k, 'planar slack s+3',
                        trial=trial, candidates=candidates, demands=demands,
                        retained=t, e=e, slack=s)
                inc('planar_slack_checks')
                if initial_min:
                    require(future <= 3 * k, 'planar minimum factor3')
                    inc('planar_optimal_factor3_checks')
                    if unique:
                        require(future <= 2 * k, 'planar unique factor2')
                        inc('planar_unique_factor2_checks')
                    h = m - e.bit_count()
                    require(future <= min(3, h + 1) * k, 'planar nonunique table')
                    inc('planar_table_nonunique_checks')
                    if unique:
                        require(future <= min(2, max(1, h)) * k, 'planar unique table')
                        inc('planar_table_unique_checks')
                require(opt[normalized][e] <= future,
                        'normalization all-future nonincrease', trial=trial,
                        retained=t, normalized=normalized, e=e)
                inc('normalization_all_future_checks')
                if future * observed_den > observed_num * k:
                    observed_num, observed_den = future, k
            local = max(opt[t][signature] for signature in signatures)
            require(observed_num == local * observed_den, 'A0 exact loss identity')
            inc('planar_exact_loss_identity_checks')
        if trial < 3:
            sample_records.append({'candidates': candidates, 'demands': demands,
                                   'initial_optimum': q,
                                   'number_initial_optima': len(minima)})
    return {'seed': SEED, 'grid': 'positive integer [1,6]^2',
            'candidate_count': [2, 7], 'demand_count': [2, 7],
            'sample_instances': sample_records}


def pad_2d(candidates, demands, future, h, base_h):
    scale = h + 1
    sc = lambda points: [tuple(scale * x for x in p) for p in points]
    candidates, demands, future = sc(candidates), sc(demands), sc(future)
    demands += [(1, j) for j in range(1, h - base_h + 1)]
    return candidates, demands, future


def table_instance(dim, unique, h):
    if dim == 1:
        demands = [(i,) for i in range(1, h + 2)]
        candidates = [(h + 2,)] if unique else [(h + 2,), (h + 3,)]
        return candidates, demands, [(1,)], 1, 1
    if dim == 2:
        if unique and h == 1:
            return [(3, 3)], [(1, 1), (2, 2)], [(1, 1)], 1, 1
        if unique or h == 1:
            candidates = [(1, 3), (2, 2), (3, 1)]
            future = [(1, 2), (2, 1)]
            demands = future + [(1, 3)] + ([(3, 1)] if unique else [])
            base_h = 2 if unique else 1
            candidates, demands, future = pad_2d(candidates, demands, future, h, base_h)
            return candidates, demands, future, 0b101, 2
        candidates = [(3, 3), (1, 4), (2, 2), (4, 1)]
        future = [(1, 3), (2, 2), (3, 1)]
        demands = future + [(1, 4), (4, 1)]
        candidates, demands, future = pad_2d(candidates, demands, future, h, 2)
        return candidates, demands, future, 0b1110, 3
    if unique and h == 1:
        candidates, demands, future, t, ratio = [(3, 3, 3)], [(1, 1, 1), (2, 2, 2)], [(1, 1, 1)], 1, 1
    else:
        m = h if unique else h + 1
        p = (m, m, 2)
        qs = [(i, m + 1 - i, 3) for i in range(1, m + 1)]
        future = [(i, m + 1 - i, 1) for i in range(1, m + 1)]
        candidates = [p] + qs
        demands = future + (qs if unique else qs[:h])
        t, ratio = ((1 << (m + 1)) - 2), m
    if dim > 3:
        append = lambda points: [p + (1,) * (dim - 3) for p in points]
        candidates, demands, future = append(candidates), append(demands), append(future)
    return candidates, demands, future, t, ratio


def check_sharp_instance(candidates, demands, future, retained):
    require(len(set(candidates)) == len(candidates), 'distinct candidates')
    require(len(set(demands)) == len(demands), 'distinct demands')
    require(set(future) <= set(demands), 'future demand inclusion')
    signatures = incidence_signatures(candidates, demands)
    full_d = (1 << len(demands)) - 1
    e = sum(1 << j for j, d in enumerate(demands) if d in set(future))
    initial_opt, minima = exact_problem(signatures, len(demands), full_d)
    retained_initial, _ = exact_problem(signatures, len(demands), full_d, retained)
    original_future, _ = exact_problem(signatures, len(demands), e)
    retained_future, _ = exact_problem(signatures, len(demands), e, retained)
    inc('sharp_problem_exact_optimizations', 4)
    require(retained_initial <= len(candidates), 'initial feasibility')
    return initial_opt, minima, original_future, retained_future


def sharp_table():
    records = []
    for dim in [1, 2, 3, 4]:
        for unique in [False, True]:
            for h in range(1, 9):
                candidates, demands, future, t, expected = table_instance(dim, unique, h)
                q, minima, k, value = check_sharp_instance(candidates, demands, future, t)
                require(len(demands) - len(future) == h, 'exact deletion count')
                require(t in minima, 'retained portfolio initial minimum')
                require((len(minima) == 1) == unique, 'intended uniqueness status',
                        dimension=dim, unique=unique, h=h, n_minima=len(minima))
                require(k == 1 and value == expected, 'sharp table attainment',
                        dimension=dim, unique=unique, h=h)
                expected_table = 1 if dim == 1 else (
                    min(2, h) if unique else min(3, h + 1)) if dim == 2 else (
                    h if unique else h + 1)
                require(value == expected_table, 'reported table formula')
                inc('sharp_table_instances')
                records.append({'dimension': dim, 'unique': unique, 'h': h,
                                'initial_optimum': q, 'initial_optima': len(minima),
                                'future_original_optimum': k,
                                'future_retained_optimum': value,
                                'n_candidates': len(candidates), 'n_demands': len(demands)})
    return records


def sharp_slack():
    records = []
    for s in range(9):
        k = s + 1
        p = (k + 2, k + 2)
        left, right = (1, k + 3), (k + 3, 1)
        qs = [(i + 1, k + 2 - i) for i in range(1, k + 1)]
        candidates = [p, left, right] + qs
        future = qs + [(1, k + 2), (k + 2, 1)]
        demands = future + [left, right]
        t = (1 << len(candidates)) - 2
        q, minima, original, retained = check_sharp_instance(candidates, demands, future, t)
        require(q == 3, 'slack construction initial optimum')
        require(t.bit_count() - q == s, 'slack exact value')
        require(original == 1 and retained == s + 3, 'sharp slack attainment')
        inc('sharp_slack_instances')
        records.append({'s': s, 'initial_optimum': q,
                        'retained_cardinality': t.bit_count(),
                        'future_original_optimum': original,
                        'future_retained_optimum': retained})
    return records


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path,
                        help='Write to a new file; refuse an existing path. Default: stdout only.')
    args = parser.parse_args()
    if args.output and args.output.exists():
        parser.error(f'Output already exists: {args.output}')
    started = time.monotonic()
    result = {'status': 'running', 'method': 'exact finite enumeration; not a formal proof',
              'seed': SEED, 'counts': COUNTS}
    result['incidence_exhaustive'] = exhaustive_incidence()
    result['planar_random'] = random_planar()
    result['sharp_table'] = sharp_table()
    result['sharp_slack'] = sharp_slack()
    result['status'] = 'all_checks_passed'
    result['elapsed_seconds'] = round(time.monotonic() - started, 3)
    rendered = json.dumps(result, ensure_ascii=False, indent=2) + '\n'
    if args.output:
        with args.output.open('x', encoding='utf-8') as output:
            output.write(rendered)
        print(json.dumps({'status': result['status'], 'counts': COUNTS,
                          'elapsed_seconds': result['elapsed_seconds'], 'output': str(args.output)},
                         ensure_ascii=False, indent=2))
    else:
        print(rendered, end='')


if __name__ == '__main__':
    main()
