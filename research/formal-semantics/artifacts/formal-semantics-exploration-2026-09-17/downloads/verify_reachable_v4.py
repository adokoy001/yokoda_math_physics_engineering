"""Finite audit of the binary-cost reachable-loss reduction.

Checks actual reachable state/cost pairs and complete finite suffix cost sets,
not only the designated-state inequalities in the written proof.
"""
from itertools import product, combinations
from functools import lru_cache
import json


def add(a, b):
    return a[0] + b[0], a[1] + b[1]


def leq(a, b):
    return a[0] <= b[0] and a[1] <= b[1]


def audit(weights, target):
    n, total = len(weights), sum(weights)
    m = total + 1
    shift = n + target + m, n + total - target + m
    budgets = tuple(add(shift, b) for b in ((1, 3), (2, 2), (3, 1)))
    fork, terminal = n + 1, n + 2
    edges = {q: [] for q in range(terminal + 1)}
    for i, w in enumerate(weights):
        edges[i] = [(i + 1, (w + 1, 1)), (i + 1, (1, w + 1))]
    edges[n] = [(fork, (m, m))]
    edges[fork] = [(terminal, (1, 2)), (terminal, (2, 1))]
    edges[0] += [(terminal, budgets[0]), (terminal, budgets[2])]

    @lru_cache(None)
    def suffix_costs(q):
        costs = {(0, 0)}
        for nxt, cost in edges[q]:
            costs.update(add(cost, v) for v in suffix_costs(nxt))
        return frozenset(costs)

    def covered(q, c, chosen):
        return frozenset(v for v in suffix_costs(q)
                         if any(leq(add(c, v), budgets[j]) for j in chosen))

    def optimum(q, c, support):
        universe = covered(q, c, range(3))
        for k in range(len(support) + 1):
            for chosen in combinations(support, k):
                if covered(q, c, chosen) == universe:
                    return k
        raise AssertionError("Initial equivalence was not inherited")

    universe0 = covered(0, (0, 0), range(3))
    initial_minima = [chosen for chosen in combinations(range(3), 2)
                      if covered(0, (0, 0), chosen) == universe0]
    assert initial_minima == [(0, 2)], (weights, target, initial_minima)
    assert optimum(0, (0, 0), (0, 1, 2)) == 2

    reachable = [set() for _ in edges]
    reachable[0].add((0, 0))
    for q in range(terminal + 1):
        for c in reachable[q]:
            for nxt, cost in edges[q]:
                new = add(c, cost)
                if any(leq(new, b) for b in budgets):
                    reachable[nxt].add(new)

    any_loss = False
    fork_losses = set()
    checked_states = 0
    for q in range(terminal + 1):
        for c in reachable[q]:
            checked_states += 1
            before = optimum(q, c, (0, 1, 2))
            after = optimum(q, c, (0, 2))
            assert 1 <= before <= after <= 2
            if after > before:
                any_loss = True
                if q == fork:
                    fork_losses.add(c)

            # Independently check inclusion-exclusion counting for every subset.
            def count_box(bound):
                return sum(leq(v, bound) for v in suffix_costs(q))

            for mask in range(8):
                chosen = [i for i in range(3) if mask >> i & 1]
                count = 0
                for size in range(1, len(chosen) + 1):
                    for sub in combinations(chosen, size):
                        bound = (min(budgets[j][0] for j in sub) - c[0],
                                 min(budgets[j][1] for j in sub) - c[1])
                        count += (-1) ** (size + 1) * count_box(bound)
                assert count == len(covered(q, c, chosen))

    sums = {0}
    for w in weights:
        sums |= {s + w for s in sums}
    expected = target in sums
    assert any_loss == expected, (weights, target, any_loss, expected)
    assert bool(fork_losses) == expected
    assert not fork_losses or fork_losses == {shift}
    return checked_states


if __name__ == "__main__":
    cases, states = 0, 0
    for n in range(1, 5):
        for weights in product(range(1, 4), repeat=n):
            for target in range(sum(weights) + 1):
                states += audit(weights, target)
                cases += 1
    result = {
        "status": "passed",
        "subset_sum_instances": cases,
        "reachable_state_cost_pairs": states,
        "range": "n=1..4; every wi=1..3; every B=0..sum(w)",
        "checks": ["initial unique exact minimum T={left,right}",
                   "all reachable-prefix loss iff subset sum is solvable",
                   "designated-state loss iff exact target accumulated cost",
                   "all 8 subsets: box inclusion-exclusion counts equal direct coverage"],
        "limits": "finite checks complement, not replace, the symbolic proofs"
    }
    with open("reachable_v4_results.json", "w") as f:
        json.dump(result, f, indent=2)
    print(json.dumps(result, indent=2))
