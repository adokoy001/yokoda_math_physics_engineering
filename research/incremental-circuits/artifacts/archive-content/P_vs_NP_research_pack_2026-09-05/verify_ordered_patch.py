#!/usr/bin/env python3
"""Exhaustive, bit-parallel verification of contiguous-interval patch circuits.

Basis: fan-in 2 AND/OR, unary NOT, free fanout, no constant inputs.
The original circuit's output is an opaque port; every x and both possible
values of this port are checked. This covers every possible original C.
"""
from __future__ import annotations

import argparse
import json
import random
import time
from pathlib import Path


def base_rows(n: int):
    """Rows are (x,c) in lex order, with c varying fastest."""
    rows = 1 << (n + 1)
    full = (1 << rows) - 1
    values = []
    for j in range(n):
        values.append(sum(1 << (2*x+c) for x in range(1 << n)
                          for c in (0, 1) if (x >> (n-1-j)) & 1))
    values.append(sum(1 << (2*x+1) for x in range(1 << n)))
    return values, full


class Circuit:
    def __init__(self, n, values=None, gates=None, full=None):
        self.n = n
        if values is None:
            self.values, self.full = base_rows(n)
            self.gates = []
        else:
            self.values, self.gates, self.full = values, gates, full

    def clone(self):
        return Circuit(self.n, self.values.copy(), self.gates.copy(), self.full)

    def gate(self, kind, *args):
        if kind == 'NOT':
            assert len(args) == 1
            val = self.values[args[0]] ^ self.full
        elif kind == 'AND':
            assert len(args) == 2
            val = self.values[args[0]] & self.values[args[1]]
        elif kind == 'OR':
            assert len(args) == 2
            val = self.values[args[0]] | self.values[args[1]]
        else:
            raise ValueError(kind)
        out = len(self.values)
        self.gates.append((kind, *args))
        self.values.append(val)
        return out

    def or_tree(self, wires):
        # A left-associated fan-in 2 tree. No empty OR / constant is used.
        assert wires
        out = wires[0]
        for wire in wires[1:]:
            out = self.gate('OR', out, wire)
        return out


def trie_skeleton(n, a, k):
    assert n >= 1 and 1 <= k <= (1 << n) and 0 <= a <= (1 << n)-k
    c = Circuit(n)
    negative = [c.gate('NOT', j) for j in range(n)]
    leaves = []
    depth_counts = [0] * (n+1)
    unary = 0
    branches = 0
    b = a+k

    def walk(depth, left, span, parent):
        nonlocal unary, branches
        if depth == n:
            leaves.append(parent)
            return
        half = span >> 1
        children = []
        for bit in (0, 1):
            child_left = left + bit*half
            if child_left < b and child_left+half > a:
                children.append((bit, child_left))
        unary += len(children) == 1
        branches += len(children) == 2
        for bit, child_left in children:
            literal = depth if bit else negative[depth]
            wire = literal if depth == 0 else c.gate('AND', parent, literal)
            depth_counts[depth+1] += 1
            walk(depth+1, child_left, half, wire)

    walk(0, 0, 1 << n, None)
    assert len(leaves) == k
    assert branches == k-1
    assert unary <= 2*n-1
    exact_T = sum(depth_counts[2:])
    assert exact_T <= 2*k+2*n-4
    assert len(c.gates) == n+exact_T
    for depth in range(1, n+1):
        expected = ((a+k-1) >> (n-depth)) - (a >> (n-depth)) + 1
        assert depth_counts[depth] == expected
    return c, leaves, exact_T


def patch(skeleton, leaves, alpha):
    c = skeleton.clone()
    zero = [w for j, w in enumerate(leaves) if not ((alpha >> j) & 1)]
    one = [w for j, w in enumerate(leaves) if (alpha >> j) & 1]
    original = c.n
    if not zero:
        out = c.gate('OR', original, c.or_tree(one))
    elif not one:
        out = c.gate('AND', original, c.gate('NOT', c.or_tree(zero)))
    else:
        d0 = c.or_tree(zero)
        d1 = c.or_tree(one)
        out = c.gate('OR', c.gate('AND', original, c.gate('NOT', d0)), d1)
    return c, out


def zero_suffix_completion(skeleton, leaves, alpha):
    c = skeleton.clone()
    one = [w for j, w in enumerate(leaves) if (alpha >> j) & 1]
    if one:
        out = c.or_tree(one)
    else:
        # Ignore the already built skeleton in the all-zero case: two gates.
        c = Circuit(c.n)
        out = c.gate('AND', 0, c.gate('NOT', 0))
    return c, out


def expected_patch(n, a, k, alpha):
    original = sum(1 << (2*x+1) for x in range(1 << n))
    interval = ((1 << (2*k))-1) << (2*a)
    labels = sum(3 << (2*(a+j)) for j in range(k) if (alpha >> j) & 1)
    return (original & ~interval) | labels


def check_one(n, a, k, alpha, skeleton, leaves, T, stats):
    c, out = patch(skeleton, leaves, alpha)
    expected = expected_patch(n, a, k, alpha)
    assert c.values[out] == expected, (n, a, k, alpha, 'truth')
    gates = len(c.gates)
    exact = n+T+k+(alpha != (1 << k)-1)
    assert gates == exact, (n, a, k, alpha, gates, exact)
    assert gates <= n+T+k+1
    assert gates <= 3*k+3*n-3
    if k == 1:
        assert gates <= 2*n+1
    stats['patch_circuits'] += 1
    stats['evaluated_rows'] += 1 << (n+1)
    stats['max_additional_gates'] = max(stats['max_additional_gates'], gates)
    if a == 0:
        completion, completion_out = zero_suffix_completion(skeleton, leaves, alpha)
        labels = sum(3 << (2*j) for j in range(k) if (alpha >> j) & 1)
        assert completion.values[completion_out] == labels
        assert len(completion.gates) <= 3*k+3*n-3
        # The completion has no dependence on the original-circuit output port.
        assert all(n not in gate[1:] for gate in completion.gates)
        stats['prefix_completion_circuits'] += 1


def run(exhaustive_n=4, seed=20260905):
    started = time.monotonic()
    result = {'basis': 'fan-in 2 AND/OR; unary NOT charged; free fanout; no constants',
              'model': 'original C represented by a free opaque output port; all x,c tested',
              'seed': seed, 'exhaustive': [], 'sampled': []}
    for n in range(1, exhaustive_n+1):
        stats = {'n': n, 'intervals': 0, 'patch_circuits': 0, 'evaluated_rows': 0,
                 'prefix_completion_circuits': 0, 'max_additional_gates': 0}
        N = 1 << n
        for k in range(1, N+1):
            for a in range(N-k+1):
                skeleton, leaves, T = trie_skeleton(n, a, k)
                stats['intervals'] += 1
                for alpha in range(1 << k):
                    check_one(n, a, k, alpha, skeleton, leaves, T, stats)
        result['exhaustive'].append(stats)
    rng = random.Random(seed)
    for n in (5, 6, 8, 10):
        stats = {'n': n, 'intervals': 0, 'patch_circuits': 0, 'evaluated_rows': 0,
                 'prefix_completion_circuits': 0, 'max_additional_gates': 0}
        N = 1 << n
        cases = [(0, 1), (N-1, 1), (0, N), (1, N-2), (N//2-1, 2)]
        cases += [(0, min(N, 1 << j)) for j in range(n+1)]
        for _ in range(100):
            k = rng.randint(1, min(N, 256))
            cases.append((rng.randint(0, N-k), k))
        for a, k in cases:
            skeleton, leaves, T = trie_skeleton(n, a, k)
            stats['intervals'] += 1
            alphas = {0, (1 << k)-1, rng.getrandbits(k), rng.getrandbits(k)}
            for alpha in alphas:
                check_one(n, a, k, alpha, skeleton, leaves, T, stats)
        result['sampled'].append(stats)
    result['status'] = 'PASS'
    result['elapsed_seconds'] = round(time.monotonic()-started, 3)
    result['scope_note'] = ('Finite checks supplement the proof; they are not asymptotic '
                            'lower bounds, novelty evidence, or a P versus NP result.')
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--exhaustive-n', type=int, default=4)
    parser.add_argument('--output', type=Path,
                        default=Path(__file__).with_name('ordered_patch_experiment.json'))
    args = parser.parse_args()
    result = run(args.exhaustive_n)
    args.output.write_text(json.dumps(result, ensure_ascii=False, indent=2)+'\n')
    print(json.dumps(result, ensure_ascii=False))
