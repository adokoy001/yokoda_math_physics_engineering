#!/usr/bin/env python3
"""Independent redundant gate-program enumeration and witness verification."""
import itertools, json, pathlib
ROOT = pathlib.Path(__file__).resolve().parent

def brute_programs(n, max_size):
    row_count = 1 << n
    mask = (1 << row_count) - 1
    base = [0, mask] + [sum(((x >> j) & 1) << x for x in range(row_count)) for j in range(n)]
    minimum = {f: 0 for f in base}
    program_counts = [0] * (max_size + 1)
    def walk(wires, depth):
        program_counts[depth] += 1
        if depth == max_size:
            return
        # Unlike the BFS, retain repeated functions and redundant gates,
        # including repeated-input AND/OR. Thus this independently covers
        # every syntactic gate program, modulo commutative argument order.
        gates = [mask ^ a for a in wires]
        for ia,a in enumerate(wires):
            for b in wires[ia:]:
                gates.extend([a & b, a | b])
        for v in gates:
            minimum[v] = min(minimum.get(v, depth + 1), depth + 1)
            walk(wires + [v], depth + 1)
    walk(base, 0)
    return minimum, program_counts

results = []
for n in [2,3,4]:
    d = json.loads((ROOT / f'tiny_wc_synthesis_n{n}.json').read_text())
    mask = (1 << (1 << n)) - 1
    costs = {int(k):v for k,v in d['minimum_sizes'].items()}
    for name,circuit in d['witnesses'].items():
        f = int(name)
        assert len(circuit) == costs[f]
        available = set(d['base_wires'])
        for step in circuit:
            op, *args = step['gate']
            assert all(x in available for x in args)
            if op == 'NOT':
                v = mask ^ args[0]
            elif op == 'AND':
                v = args[0] & args[1]
            else:
                assert op == 'OR'
                v = args[0] | args[1]
            assert v == step['output']
            available.add(v)
        assert f in available
    for summary in d['threshold_summary']:
        assert summary['live_prefixes'] == sum(summary[k] for k in ['both_next_bits','forced_0','forced_1'])
        # Binary trie with both root edges present (free constants).
        assert summary['both_next_bits'] == summary['functions'] - 2
    result = {'n': n, 'witnesses_verified': len(costs), 'prefix_trie_invariants_verified': True}
    if n <= 3:
        direct, counts = brute_programs(n, 3)
        assert direct == {f:c for f,c in costs.items() if c <= 3}
        result['independent_redundant_program_counts_by_size'] = counts
        result['independent_minimum_sizes_through_3_match'] = True
    results.append(result)
(ROOT / 'tiny_wc_verification.json').write_text(json.dumps(results, indent=2) + '\n')
print(json.dumps(results, indent=2))
