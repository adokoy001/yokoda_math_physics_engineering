#!/usr/bin/env python3
"""Exact bounded gate-DAG synthesis, with free constants, inputs, and fanout.
Truth-table bit x is f(x), where x ranges from 0 through 2**n-1.
Every BFS state is the sorted tuple of its non-base wire functions.
No repeated wire function is needed by a minimum-size circuit.
"""
import argparse, itertools, json, pathlib, time

def enumerate_costs(n, max_size, layer_budget=50):
    rows = 1 << n
    mask = (1 << rows) - 1
    inputs = [sum(((x >> j) & 1) << x for x in range(rows)) for j in range(n)]
    base = tuple(sorted(set([0, mask] + inputs)))
    costs = {f: 0 for f in base}
    # Keep one optimal circuit witness per output function.
    circuits = {f: [] for f in base}
    states = {(): []}
    stats = [{'size': 0, 'states': 1, 'functions': len(costs), 'seconds': 0}]
    complete = 0
    for size in range(1, max_size + 1):
        start = time.monotonic()
        next_states = {}
        additions = {}
        aborted = False
        for t, (state, circuit) in enumerate(states.items()):
            if t % 256 == 0 and time.monotonic() - start > layer_budget:
                aborted = True
                break
            wires = base + state
            have = set(wires)
            possible = {}
            for a in wires:
                v = mask ^ a
                if v not in have:
                    possible.setdefault(v, ['NOT', a])
            for ia, a in enumerate(wires):
                for b in wires[ia + 1:]:
                    v = a & b
                    if v not in have:
                        possible.setdefault(v, ['AND', a, b])
                    v = a | b
                    if v not in have:
                        possible.setdefault(v, ['OR', a, b])
            for v, gate in possible.items():
                next_state = tuple(sorted(state + (v,)))
                if next_state not in next_states:
                    next_circuit = circuit + [{'output': v, 'gate': gate}]
                    next_states[next_state] = next_circuit
                    if v not in costs:
                        additions.setdefault(v, next_circuit)
        elapsed = time.monotonic() - start
        if aborted:
            stats.append({'size': size, 'complete': False, 'partial_states': len(next_states), 'seconds': elapsed})
            print(f'n={n} size={size} ABORTED; previous layer remains exact', flush=True)
            break
        for f, circuit in additions.items():
            costs[f] = size
            circuits[f] = circuit
        stats.append({'size': size, 'states': len(next_states), 'functions': len(costs), 'seconds': elapsed})
        print(f'n={n} size={size} states={len(next_states)} functions={len(costs)} seconds={elapsed:.3f}', flush=True)
        complete = size
        states = next_states
        if len(costs) == 1 << rows:
            break
    return base, costs, circuits, stats, complete

def analyze(n, base, costs, circuits, stats, complete):
    rows = 1 << n
    out = {'n': n, 'complete_through_size': complete, 'all_functions_found': len(costs) == 1 << rows,
           'truth_table_convention': 'bit x is f(x); integer inputs x in increasing binary order; x_0 is least significant coordinate',
           'basis': 'fan-in 2 AND/OR, fan-in 1 NOT; free constants, inputs, fanout; output any wire',
           'base_wires': list(base), 'layer_statistics': stats,
           'minimum_sizes': {str(f): size for f, size in sorted(costs.items())},
           'witnesses': {str(f): c for f,c in sorted(circuits.items())},
           'threshold_summary': [], 'live_prefix_rows': [], 'forced_prefix_rows': [], 'violations': [], 'tight_examples': []}
    for s in range(complete + 1):
        fs = [f for f,c in costs.items() if c <= s]
        counts = {'s': s, 'functions': len(fs), 'live_prefixes': 0, 'both_next_bits': 0, 'forced_0': 0, 'forced_1': 0,
                  'bound_tests': 0, 'bound_violations': 0, 'tight_forced_0': 0, 'tight_forced_1': 0}
        for i in range(1, rows):
            groups = {}
            prefixmask = (1 << i) - 1
            for f in fs:
                u = f & prefixmask
                g = groups.setdefault(u, {'bits': set(), 'tau': costs[f], 'witness': f})
                g['bits'].add((f >> i) & 1)
                if costs[f] < g['tau']:
                    g['tau'] = costs[f]
                    g['witness'] = f
            for u,g in groups.items():
                counts['live_prefixes'] += 1
                live_row = {'s': s, 'i': i, 'prefix': ''.join(str((u >> j) & 1) for j in range(i)),
                            'prefix_integer': u, 'next_bits': sorted(g['bits']), 'tau': g['tau'],
                            'slack': s - g['tau'], 'w': i.bit_count(), 'minimum_prefix_witness': g['witness']}
                out['live_prefix_rows'].append(live_row)
                if len(g['bits']) == 2:
                    counts['both_next_bits'] += 1
                    continue
                forced = next(iter(g['bits']))
                counts[f'forced_{forced}'] += 1
                counts['bound_tests'] += 1
                tau = g['tau']
                w = i.bit_count()
                slack = s - tau
                # force0 implies slack < w; force1 implies slack < w+1.
                repair_cost = w + forced
                row = {'s': s, 'i': i, 'prefix': ''.join(str((u >> j) & 1) for j in range(i)),
                       'prefix_integer': u, 'next_forced': forced, 'tau': tau, 'slack': slack, 'w': w,
                       'required_strict_bound': f'slack < {repair_cost}', 'minimum_prefix_witness': g['witness']}
                out['forced_prefix_rows'].append(row)
                if slack >= repair_cost:
                    counts['bound_violations'] += 1
                    out['violations'].append(row)
                if slack == repair_cost - 1:
                    counts[f'tight_forced_{forced}'] += 1
                    out['tight_examples'].append(row)
        out['threshold_summary'].append(counts)
    return out

def main():
    p = argparse.ArgumentParser()
    p.add_argument('--n', type=int, required=True)
    p.add_argument('--size', type=int, required=True)
    p.add_argument('--budget', type=float, default=50)
    p.add_argument('--out', type=pathlib.Path, required=True)
    args = p.parse_args()
    data = analyze(args.n, *enumerate_costs(args.n, args.size, args.budget))
    args.out.write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps({'n': args.n, 'summary': data['threshold_summary'], 'violation_count': len(data['violations']), 'tight_count': len(data['tight_examples'])}, ensure_ascii=False), flush=True)

if __name__ == '__main__':
    main()
