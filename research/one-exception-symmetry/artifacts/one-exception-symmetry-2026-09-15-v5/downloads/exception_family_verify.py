"""Checks for the fifth edition: pendant tufts on 2xn ladders and odd-clique exception sets.
Python standard library only. Run: python exception_family_verify.py
Every value is computed by plain mex recursion over vertex subsets; no formula is built in.
"""
from functools import lru_cache
from itertools import combinations, combinations_with_replacement, product
from pathlib import Path
import json
import random

SEED = 20260915


def sg(n, edges):
    moves = tuple({(1 << u) | (1 << v) for u, v in edges})

    @lru_cache(None)
    def g(mask):
        seen = {g(mask ^ e) for e in moves if mask & e == e}
        k = 0
        while k in seen:
            k += 1
        return k
    return g((1 << n) - 1)


def ladder(n):
    """2xn grid; column i is the pair (2i, 2i+1)."""
    return ([(2 * i, 2 * i + 1) for i in range(n)]
            + [(2 * i, 2 * i + 2) for i in range(n - 1)]
            + [(2 * i + 1, 2 * i + 3) for i in range(n - 1)])


def core(m, bits):
    """Pairs (2i, 2i+1) with pair edges; each bit adds one swap-invariant orbit of two edges."""
    edges = [(2 * i, 2 * i + 1) for i in range(m)]
    k = 0
    for i, j in combinations(range(m), 2):
        for flip in (0, 1):
            if bits >> k & 1:
                edges += [(2 * i, 2 * j + flip), (2 * i + 1, 2 * j + 1 - flip)]
            k += 1
    return edges


def exception_set(m, x_edges, c, bits, adj):
    """m symmetric pairs plus an exception set X of c vertices (labels 2m..2m+c-1).
    x_edges is the graph on X; adj chooses every X-to-pair edge independently (no symmetry)."""
    edges = core(m, bits) + [(2 * m + a, 2 * m + b) for a, b in x_edges]
    edges += [(2 * m + z, v) for z in range(c) for v in range(2 * m) if adj >> (z * 2 * m + v) & 1]
    return sg(2 * m + c, edges)


def histogram(values):
    out = {}
    for v in values:
        out[str(v)] = out.get(str(v), 0) + 1
    return dict(sorted(out.items()))


def main():
    rng = random.Random(SEED)
    report = {'seed': SEED, 'ladder_tufts': {}, 'odd_clique_exceptions': {},
              'controls': {}, 'strictly_matched_fixed_clique': {}, 'paw': {}}

    # 1. Tufts on 2xn ladders. A tuft is a star whose centre is a grid vertex.
    one, two, three, multi = [], [], [], []
    for n in range(1, 9):
        base = sg(2 * n, ladder(n))
        assert base == n % 2
        bad1 = sum(sg(2 * n + 1, ladder(n) + [(v, 2 * n)]) != base for v in range(2 * n))
        pairs = list(combinations_with_replacement(range(2 * n), 2))
        bad2 = [p for p in pairs
                if sg(2 * n + 2, ladder(n) + [(p[0], 2 * n), (p[1], 2 * n + 1)]) != base]
        one.append({'n': n, 'placements': 2 * n, 'changed': bad1})
        two.append({'n': n, 'placements': len(pairs), 'changed': len(bad2), 'examples': bad2[:3]})
        assert bad1 == 0
        assert (len(bad2) == 0) == (n >= 2)
    for n in range(2, 7):
        base = n % 2
        checked = bad = 0
        for v, w in combinations_with_replacement(range(2 * n), 2):
            for a, b in product(range(1, 4), repeat=2):
                if 2 * n + a + b > 18:
                    continue
                edges = ladder(n) + [(v, 2 * n + i) for i in range(a)] + [(w, 2 * n + a + j) for j in range(b)]
                checked += 1
                bad += sg(2 * n + a + b, edges) != base
        multi.append({'n': n, 'leaf_counts': '1..3 per tuft', 'placements': checked, 'changed': bad})
        assert bad == 0
        triples = list(combinations_with_replacement(range(2 * n), 3))
        bad3 = [t for t in triples
                if sg(2 * n + 3, ladder(n) + [(x, 2 * n + i) for i, x in enumerate(t)]) != base]
        three.append({'n': n, 'placements': len(triples), 'changed': len(bad3), 'examples': bad3[:3]})
        assert bad3
    report['ladder_tufts'] = {'one_leaf': one, 'two_single_leaves': two,
                              'two_tufts_multi_leaf': multi, 'three_single_leaves': three}

    # 2. Exception set inducing K3 or K5, with arbitrary edges to the pairs.
    K3 = list(combinations(range(3), 2))
    K5 = list(combinations(range(5), 2))
    k3 = []
    for m in (0, 1, 2):
        vals = [exception_set(m, K3, 3, bits, adj)
                for bits in range(1 << (m * (m - 1))) for adj in range(1 << (6 * m))]
        assert set(vals) == {(m + 1) % 2}
        k3.append({'m': m, 'mode': 'exhaustive', 'cases': len(vals), 'values': histogram(vals)})
    vals = [exception_set(3, K3, 3, rng.getrandbits(6), rng.getrandbits(18)) for _ in range(400)]
    assert set(vals) == {0}
    k3.append({'m': 3, 'mode': 'random', 'cases': 400, 'values': histogram(vals)})
    k5 = []
    vals = [exception_set(1, K5, 5, 0, adj) for adj in range(1 << 10)]
    assert set(vals) == {1}
    k5.append({'m': 1, 'mode': 'exhaustive', 'cases': len(vals), 'values': histogram(vals)})
    for m, count in ((2, 400), (3, 100)):
        vals = [exception_set(m, K5, 5, rng.getrandbits(m * (m - 1)), rng.getrandbits(10 * m))
                for _ in range(count)]
        assert set(vals) == {(m + 2) % 2}
        k5.append({'m': m, 'mode': 'random', 'cases': count, 'values': histogram(vals)})
    report['odd_clique_exceptions'] = {'K3_predicted': '(m+1) mod 2', 'K3': k3,
                                       'K5_predicted': '(m+2) mod 2', 'K5': k5}

    # 3. Other exception graphs on 3 or 5 vertices do not keep a single value.
    controls = {'P3': (3, [(0, 1), (1, 2)]), 'K2+K1': (3, [(0, 1)]), '3K1': (3, []),
                'C5': (5, [(i, (i + 1) % 5) for i in range(5)]),
                'K5-e': (5, [e for e in K5 if e != (0, 1)]),
                'bowtie': (5, [(0, 1), (0, 2), (1, 2), (2, 3), (2, 4), (3, 4)])}
    for name, (c, xe) in controls.items():
        vals = [exception_set(2, xe, c, rng.getrandbits(2), rng.getrandbits(4 * c)) for _ in range(300)]
        controls_hist = histogram(vals)
        assert len(controls_hist) > 1
        report['controls'][name] = {'m': 2, 'cases': 300, 'values': controls_hist}

    # 4. Strictly matched involutions: fixed-point clique C, every z in C symmetric to each pair.
    for c in range(6):
        rows = []
        for m in range(0, 5 if c <= 3 else 4):
            vals = []
            for _ in range(200):
                edges = core(m, rng.getrandbits(max(1, m * (m - 1))))
                edges += [(2 * m + a, 2 * m + b) for a, b in combinations(range(c), 2)]
                for z in range(c):
                    for i in range(m):
                        if rng.random() < .5:
                            edges += [(2 * m + z, 2 * i), (2 * m + z, 2 * i + 1)]
                vals.append(sg(2 * m + c, edges))
            rows.append({'m': m, 'cases': 200, 'values': histogram(vals),
                         'floor_half_order_mod2': (2 * m + c) // 2 % 2})
            if c % 2 == 1 or c == 0:
                assert set(vals) == {(2 * m + c) // 2 % 2}
        report['strictly_matched_fixed_clique'][str(c)] = rows

    # 5. Symmetric two-point clique already fails: the paw with a pendant at the triangle apex.
    paw = [(0, 1), (2, 0), (2, 1), (2, 3)]  # pair {0,1}; C = {2,3}
    report['paw'] = {'edges': paw, 'pair': [0, 1], 'fixed_clique': [2, 3],
                     'grundy': sg(4, paw), 'floor_half_order_mod2': 0}
    assert report['paw']['grundy'] == 2

    dest = Path(__file__).with_name('exception_family_results.json')
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
