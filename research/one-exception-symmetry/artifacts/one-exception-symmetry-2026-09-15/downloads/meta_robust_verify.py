"""Check the robust partial-Grundy characterization on all labeled DAGs up to 4 vertices.
The order is fixed; every edge goes from a larger index to a smaller index.
Only standard Python is required. Additional followers are private Nim heaps.
"""
from itertools import product
from pathlib import Path
import json
import random


def grundy(edges, extra):
    values = []
    for i, followers in enumerate(edges):
        # Each k in extra[i] is the value of a private Nim heap option *k.
        options = {values[j] for j in followers} | set(extra[i])
        value = 0
        while value in options:
            value += 1
        values.append(value)
    return values


def first_violation(edges, labels):
    for s, c in labels.items():
        inner = {labels[t] for t in edges[s] if t in labels}
        if c in inner:
            return ('same_label', s, None)
        for k in range(c):
            if k not in inner:
                return ('missing_lower', s, k)
        for u in edges[s]:
            if u not in labels and not any(t in labels and labels[t] == c for t in edges[u]):
                return ('missing_return', s, u)
    return None


def main():
    rng = random.Random(20260915)
    report = {'seed': 20260915, 'label_range': [0, 1, 2], 'max_vertices': 4,
              'labelled_order': 'edge i -> j allowed exactly when i > j',
              'templates': 0, 'valid_certificates': 0, 'random_completions_checked': 0,
              'invalid_certificates': 0, 'constructed_counterexamples': 0,
              'violation_types': {}, 'by_vertices': []}
    for n in range(1, 5):
        potential = [(i, j) for i in range(n) for j in range(i)]
        count = 0
        for edge_mask in range(1 << len(potential)):
            edges = [[] for _ in range(n)]
            for bit, (i, j) in enumerate(potential):
                if edge_mask >> bit & 1:
                    edges[i].append(j)
            for s_mask in range(1, 1 << n):
                anchors = [i for i in range(n) if s_mask >> i & 1]
                unknown = [i for i in range(n) if not (s_mask >> i & 1)]
                for c in product(range(3), repeat=len(anchors)):
                    labels = dict(zip(anchors, c))
                    report['templates'] += 1
                    count += 1
                    violation = first_violation(edges, labels)
                    if violation is None:
                        report['valid_certificates'] += 1
                        for _ in range(5):
                            extra = [set() for _ in range(n)]
                            for u in unknown:
                                extra[u] = {k for k in range(7) if rng.getrandbits(1)}
                            got = grundy(edges, extra)
                            assert all(got[s] == value for s, value in labels.items())
                            report['random_completions_checked'] += 1
                    else:
                        report['invalid_certificates'] += 1
                        kind, s, witness = violation
                        report['violation_types'][kind] = report['violation_types'].get(kind, 0) + 1
                        extra = [set() for _ in range(n)]
                        if kind == 'missing_lower':
                            # Every unknown now has an option *k, so none has value k.
                            for u in unknown:
                                extra[u] = {witness}
                        elif kind == 'missing_return':
                            # Other unknowns cannot equal k; u is forced to k if all
                            # anchor labels survive. Otherwise robustness already fails.
                            k = labels[s]
                            for u in unknown:
                                extra[u] = set(range(k)) if u == witness else {k}
                        assert all(k <= max(c) for opts in extra for k in opts)
                        got = grundy(edges, extra)
                        assert any(got[s] != value for s, value in labels.items()), (edges, labels, violation, extra, got)
                        report['constructed_counterexamples'] += 1
        report['by_vertices'].append({'vertices': n, 'templates': count})
    report['violations_of_theorem'] = 0
    report['counterexample_heap_bound'] = 'every added Nim option *k has k <= max prescribed label'
    dest = Path(__file__).with_name('meta_robust_results.json')
    dest.write_text(json.dumps(report, ensure_ascii=False, indent=2) + '\n')
    print(json.dumps(report, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
