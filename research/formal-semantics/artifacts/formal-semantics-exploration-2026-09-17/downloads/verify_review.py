"""Audit fixed update alphabets and the two assertion-context conventions.

Python 3 standard library only. Existing research files are not modified.
Run: python verify_review.py
Writes review_results.json next to this script and prints the same JSON.
"""

from collections import deque
from itertools import combinations, product
from math import comb, inf
from pathlib import Path
import json


def families(items, max_size=None):
    limit = len(items) if max_size is None else max_size
    for size in range(limit + 1):
        yield from combinations(items, size)


def nested_contexts(n):
    for C in range(1, 1 << n):
        for D in range(C + 1, 1 << n):
            if C & D == C:
                yield C, D


def full_pair_distance(C, D, P, updates, require_nonempty=False):
    """Independent BFS on the actual two contexts, including empty word."""
    todo = deque([(C, D, 0)])
    seen = {(C, D)}
    while todo:
        S, T, distance = todo.popleft()
        if S & ~P == 0 and T & ~P:
            return distance
        for update in updates:
            pair = update[S], update[T]
            if require_nonempty and not pair[0]:
                continue
            if pair not in seen:
                seen.add(pair)
                todo.append((*pair, distance + 1))
    return inf


def cover_number(B, deletion_sets):
    """Brute force subfamilies; independent of the semantic BFS."""
    for size in range(len(deletion_sets) + 1):
        for selected in combinations(deletion_sets, size):
            covered = 0
            for item in selected:
                covered |= item
            if B & ~covered == 0:
                return size
    return inf


def assertion_formula(n, C, D, P, allowed, require_nonempty):
    B = C & ~P
    Z = D & ~C & ~P
    answers = []
    for z in range(n):
        if not (Z >> z) & 1:
            continue
        survivors = [g for g in range(n) if (C & P) >> g & 1]
        if not require_nonempty:
            survivors = [None]
        for g in survivors:
            usable = [A for A in allowed
                      if (A >> z) & 1 and (g is None or (A >> g) & 1)]
            answers.append(cover_number(B, [B & ~A for A in usable]))
    return min(answers, default=inf)


def check_assertions(n, max_family_size):
    total = 0
    finite = [0, 0]
    assertion_maps = {A: tuple(S & A for S in range(1 << n))
                      for A in range(1 << n)}
    family_count = 0
    for allowed in families(tuple(range(1 << n)), max_family_size):
        family_count += 1
        updates = [assertion_maps[A] for A in allowed]
        for C, D in nested_contexts(n):
            for P in range(1 << n):
                total += 1
                for positive in (False, True):
                    observed = full_pair_distance(C, D, P, updates, positive)
                    expected = assertion_formula(n, C, D, P, allowed, positive)
                    assert observed == expected, (
                        n, C, D, P, allowed, positive, observed, expected)
                    if observed != inf:
                        finite[int(positive)] += 1
                        assert observed <= (C & ~P).bit_count()
                        if positive:
                            assert observed <= C.bit_count() - 1
    return {"n": n, "families": family_count,
            "max_family_size": max_family_size,
            "models_each_tested_in_both_conventions": total,
            "finite_counts_vacuous_and_nonempty": finite}


def images_of_map(f, n):
    return tuple(sum(1 << q for q in
                     {f[p] for p in range(n) if (S >> p) & 1})
                 for S in range(1 << n))


def single_world_distance(n, C, D, P, updates):
    """Reduced graph used in the claimed general deterministic bound."""
    starts = [(C, z) for z in range(n) if (D & ~C) >> z & 1]
    todo = deque((S, z, 0) for S, z in starts)
    seen = set(starts)
    while todo:
        S, z, distance = todo.popleft()
        if S & ~P == 0 and not (P >> z) & 1:
            return distance
        for update in updates:
            new_S = update[S]
            new_z_mask = update[1 << z]
            assert new_S and new_z_mask.bit_count() == 1
            if new_S & new_z_mask:
                continue
            new_z = new_z_mask.bit_length() - 1
            pair = new_S, new_z
            if pair not in seen:
                seen.add(pair)
                todo.append((*pair, distance + 1))
    return inf


def check_total_updates(n, max_family_size):
    maps = tuple(images_of_map(f, n) for f in product(range(n), repeat=n))
    count = finite = 0
    family_count = 0
    for updates in families(maps, max_family_size):
        family_count += 1
        for C, D in nested_contexts(n):
            k = C.bit_count()
            upper = n * sum(comb(n - 1, j)
                            for j in range(1, min(k, n - 1) + 1)) - 1
            for P in range(1 << n):
                count += 1
                actual = full_pair_distance(C, D, P, updates)
                reduced = single_world_distance(n, C, D, P, updates)
                assert actual == reduced, (n, C, D, P, updates, actual, reduced)
                if actual != inf:
                    finite += 1
                    assert actual <= upper
    return {"n": n, "families": family_count,
            "max_family_size": max_family_size,
            "models": count, "finite_models": finite}


def check_free_assertions():
    count = 0
    for n in range(2, 5):
        updates = [tuple(S & A for S in range(1 << n))
                   for A in range(1 << n)]
        for C, D in nested_contexts(n):
            for P in range(1 << n):
                for positive in (False, True):
                    count += 1
                    if not (D & ~C & ~P) or (positive and not (C & P)):
                        expected = inf
                    else:
                        expected = int(bool(C & ~P))
                    assert full_pair_distance(C, D, P, updates, positive) == expected
    return {"n_range": [2, 4], "model_convention_cases": count}


def check_sharp_examples():
    rows = []
    for b in range(1, 8):
        # Empty-context version: b bad worlds, then one additional bad world.
        n = b + 1
        W = (1 << n) - 1
        C = (1 << b) - 1
        allowed = [W & ~(1 << i) for i in range(b)]
        updates = [tuple(S & A for S in range(1 << n)) for A in allowed]
        d_empty = full_pair_distance(C, W, 0, updates)
        assert d_empty == b
        assert full_pair_distance(C, W, 0, updates, True) == inf

        # Nonempty version: add one permanent good world g.
        n = b + 2
        W = (1 << n) - 1
        g = 1 << b
        C = (1 << (b + 1)) - 1
        allowed = [W & ~(1 << i) for i in range(b)]
        updates = [tuple(S & A for S in range(1 << n)) for A in allowed]
        d_nonempty = full_pair_distance(C, W, g, updates, True)
        assert d_nonempty == b
        rows.append({"bad_worlds": b, "empty_allowed_delay": d_empty,
                     "nonempty_preserved_delay": d_nonempty,
                     "world_counts": [b + 1, b + 2]})
    return rows


def main():
    result = {
        "status": "passed",
        "assertion_exhaustive": [check_assertions(2, None),
                                 check_assertions(3, None),
                                 check_assertions(4, 2)],
        "total_deterministic_exhaustive": [check_total_updates(2, None),
                                           check_total_updates(3, 2)],
        "unrestricted_assertions": check_free_assertions(),
        "sharp_assertion_examples": check_sharp_examples(),
        "scope": "Finite checks detect definition and boundary mistakes; not a proof or novelty claim."
    }
    serialized = json.dumps(result, indent=2) + "\n"
    Path(__file__).with_name("review_results.json").write_text(serialized)
    print(serialized, end="")


if __name__ == "__main__":
    main()
