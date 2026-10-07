from itertools import combinations
from math import lcm, comb
from collections import deque
from random import Random
import argparse
import json
from pathlib import Path

def partitions(n, minimum=1):
    if n == 0:
        yield ()
    for first in range(minimum, n + 1):
        for rest in partitions(n - first, first):
            yield (first,) + rest

def perm_of_partition(parts):
    result = []
    offset = 0
    for length in parts:
        result.extend(offset + ((i + 1) % length) for i in range(length))
        offset += length
    return result

def image(mask, relation):
    result = 0
    for i, targets in enumerate(relation):
        if mask & (1 << i):
            result |= targets
    return result

def unary_exhaustive(n):
    maxima_exact_size = [-1] * n
    examples = [None] * n
    for parts in partitions(n):
        f = perm_of_partition(parts)
        relation = [1 << q for q in f]
        period = lcm(*parts)
        image_table = [image(S, relation) for S in range(1 << n)]
        for C in range(1, (1 << n) - 1):
            size = C.bit_count()
            for z in range(n):
                if C & (1 << z):
                    continue
                trajectory = []
                S, q = C, z
                for t in range(period):
                    trajectory.append((S, q))
                    S, q = image_table[S], f[q]
                for P in range(1 << n):
                    for t, (S, q) in enumerate(trajectory):
                        if S & ~P == 0 and not (P & (1 << q)):
                            if t > maxima_exact_size[size]:
                                maxima_exact_size[size] = t
                                examples[size] = (parts, C, z, P)
                            break
    result = []
    for k in range(1, n):
        observed = max(maxima_exact_size[1:k + 1])
        expected = max(lcm(*part) for total in range(1, n + 1)
                       for part in partitions(total) if len(part) <= k + 1) - 1
        assert observed == expected, (n, k, observed, expected)
        result.append(observed)
    return result

def bfs_full(n, relations, C, D, P):
    queue = deque([(C, D, 0)])
    seen = {(C, D)}
    while queue:
        S, T, depth = queue.popleft()
        if S & ~P == 0 and T & ~P:
            return depth
        for rel in relations:
            state = (image(S, rel), image(T, rel))
            if state not in seen:
                seen.add(state)
                queue.append((*state, depth + 1))
    return None

def bfs_one_witness(n, relations, C, D, P):
    starts = [(C, z) for z in range(n) if (D & ~C) & (1 << z)]
    queue = deque((S, z, 0) for S, z in starts)
    seen = set(starts)
    while queue:
        S, z, depth = queue.popleft()
        if S & ~P == 0 and not P & (1 << z):
            return depth
        for rel in relations:
            T = image(S, rel)
            for q in range(n):
                if rel[z] & (1 << q) and not T & (1 << q):
                    state = (T, q)
                    if state not in seen:
                        seen.add(state)
                        queue.append((*state, depth + 1))
    return None

def random_relational_checks():
    rng = Random(9172026)
    count = 0
    for n in range(2, 7):
        for _ in range(200):
            relations = [[rng.randrange(1 << n) for q in range(n)] for a in range(2)]
            C = rng.randrange((1 << n) - 1)
            absent = [q for q in range(n) if not C & (1 << q)]
            D = C | (1 << rng.choice(absent)) | rng.randrange(1 << n)
            P = rng.randrange(1 << n)
            full = bfs_full(n, relations, C, D, P)
            reduced = bfs_one_witness(n, relations, C, D, P)
            assert full == reduced, (n, relations, C, D, P, full, reduced)
            if reduced is not None:
                assert reduced <= n * (1 << (n - 1)) - 1
            count += 1
    return count

def counter_example(k):
    # State 2*i+b stores bit i with value b. Trap=2*k, extra=2*k+1.
    n = 2 * k + 2
    trap, extra = 2 * k, 2 * k + 1
    relations = []
    for pivot in range(k):
        f = list(range(n))
        for j in range(pivot):
            f[2*j], f[2*j+1] = trap, 2*j
        f[2*pivot], f[2*pivot+1] = 2*pivot+1, trap
        relations.append([1 << q for q in f])
    C = sum(1 << (2*i) for i in range(k))
    D = C | (1 << extra)
    P = sum(1 << (2*i+1) for i in range(k))
    shortest = bfs_full(n, relations, C, D, P)
    assert shortest == (1 << k) - 1, (k, shortest)
    return shortest

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--max-n', type=int, default=6,
                        help='Use 10 to recompute all recorded n=2..10 numerical cases; historical batch metadata is not regenerated.')
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    records = []
    for n in range(2, args.max_n + 1):
        observed = unary_exhaustive(n)
        records.append({'n': n, 'max_delay_by_k_1_to_n_minus_1': observed,
                        'permutation_conjugacy_classes': len(list(partitions(n))),
                        'checked_C_z_P_cases': n * ((1 << (n-1)) - 1) * (1 << n) * len(list(partitions(n)))})
    result = {
        'status': 'all_checks_passed',
        'unary_exhaustive': records,
        'random_relational_pair_reduction': {'seed': 9172026, 'checked_cases': random_relational_checks()},
        'binary_counter': [{'k': k, 'n': 2*k+2, 'shortest': counter_example(k)} for k in range(1, 9)],
        'scope': 'Finite exhaustive/random computation; not proof-assistant verification.'
    }
    rendered = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        args.output.write_text(rendered + '\n')
    print(rendered)
