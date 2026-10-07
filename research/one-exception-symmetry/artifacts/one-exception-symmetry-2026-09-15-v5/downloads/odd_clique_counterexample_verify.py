"""Refutations of conjecture K; normal-play Arc Kayles, standard library only.
Run: python odd_clique_counterexample_verify.py
Two independent state representations: remaining vertices and remaining edges.
"""
from functools import lru_cache
from itertools import combinations
from pathlib import Path
import json


def mex(values):
    result = 0
    while result in values:
        result += 1
    return result


def verify(m, attachments):
    n = 2 * m + 5
    pairs = [(2*i, 2*i+1) for i in range(m)]
    clique = list(combinations(range(2*m, n), 2))
    edges = tuple(sorted(pairs + clique + attachments))
    assert len(set(edges)) == len(edges)
    core = set(pairs)
    tau = lambda v: v ^ 1
    assert all(tuple(sorted((tau(a), tau(b)))) in core for a, b in core)
    assert all(a < 2*m <= b < n for a, b in attachments)
    moves = tuple((1 << a) | (1 << b) for a, b in edges)

    @lru_cache(None)
    def by_vertices(mask):
        return mex({by_vertices(mask ^ move) for move in moves
                    if mask & move == move})

    @lru_cache(None)
    def by_edges(remaining):
        # The state is an immutable edge set; isolated vertices have no moves.
        options = set()
        for a, b in remaining:
            child = tuple((u, v) for u, v in remaining
                          if a not in (u, v) and b not in (u, v))
            options.add(by_edges(child))
        return mex(options)

    full = (1 << n) - 1
    first_moves = []
    for edge, move in zip(edges, moves):
        a, b = edge
        child = tuple((u, v) for u, v in edges
                      if a not in (u, v) and b not in (u, v))
        value = by_vertices(full ^ move)
        assert value == by_edges(child)
        kind = 'pair' if edge in pairs else 'clique' if edge in clique else 'attachment'
        first_moves.append({'edge': list(edge), 'kind': kind, 'grundy': value})
    vertex_value, edge_value = by_vertices(full), by_edges(edges)
    predicted = (m + 2) % 2
    assert vertex_value == edge_value != predicted
    return {'m': m, 'k': 2, 'vertices': n, 'pairs': pairs,
            'clique_vertices': list(range(2*m, n)), 'attachments': attachments,
            'edges': edges, 'prediction_of_retracted_K': predicted,
            'grundy_by_vertices': vertex_value, 'grundy_by_edges': edge_value,
            'first_move_value_set': sorted({row['grundy'] for row in first_moves}),
            'first_moves': first_moves}


if __name__ == '__main__':
    examples = [verify(3, [(0, 6), (0, 9), (2, 7), (4, 8)]),
                verify(4, [(0, 8), (2, 9), (4, 10), (6, 11)])]
    report = {'status': 'conjecture_K_refuted', 'examples': examples,
              'scope': 'two explicit counterexamples; no minimality claim'}
    text = json.dumps(report, ensure_ascii=False, indent=2) + '\n'
    Path(__file__).with_name('odd_clique_counterexample_results.json').write_text(text)
    print(text, end='')
