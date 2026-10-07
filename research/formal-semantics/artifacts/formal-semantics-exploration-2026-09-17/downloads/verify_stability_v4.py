"""Finite checks for deletion-onset and nonlocality results. No external modules."""
from itertools import product
import json
from pathlib import Path


def all_covers(signatures, allowed=None):
    allowed = list(range(len(signatures))) if allowed is None else list(allowed)
    covers = [(0, 0, 0)]
    for j in allowed:
        covers += [(n + 1, mask | (1 << j), cov | signatures[j])
                   for n, mask, cov in covers[:]]
    return sorted(covers)


def tau(covers, demand):
    return next(n for n, _, cov in covers if not demand & ~cov)


def generic_audit():
    initial_optima = onsets = minimal_failures = 0
    n = 3
    full = (1 << n) - 1
    for signatures in product(range(1 << n), repeat=3):
        if (signatures[0] | signatures[1] | signatures[2]) != full:
            continue
        original = all_covers(signatures)
        optimum = tau(original, full)
        for size, retained, cov in original:
            if size != optimum or cov != full:
                continue
            initial_optima += 1
            tc = all_covers(signatures, [j for j in range(3) if retained >> j & 1])
            bad = []
            for deleted in range(1 << n):
                future = full ^ deleted
                if tau(tc, future) > tau(original, future):
                    bad.append(deleted)
            brute = min((x.bit_count() for x in bad), default=None)
            formula = min(((full ^ cov).bit_count() for size, _, cov in original
                           if tau(tc, cov) > size), default=None)
            assert brute == formula
            if brute is not None:
                onsets += 1
            for deleted in bad:
                if any(other != deleted and (other & deleted) == other for other in bad):
                    continue
                minimal_failures += 1
                future = full ^ deleted
                k = tau(original, future)
                assert tau(tc, future) == k + 1
                for size, _, cov in original:
                    if size == k and future & ~cov == 0:
                        assert cov == future
    return dict(initial_optima=initial_optima, finite_onsets=onsets,
                inclusion_minimal_failures=minimal_failures)


def planar_path(m):
    q = m + 1
    scale = q
    candidates = [(scale * j, scale * (2 * m - j)) for j in range(1, 2 * m)]
    edge_demands = [(scale * i - a, scale * (2 * m - i - 1))
                    for i in range(1, 2 * m - 1) for a in range(q)]
    private = [candidates[j - 1] for j in range(1, 2 * m, 2)]
    demands = edge_demands + private
    assert len(set(demands)) == len(demands)
    signatures = [sum(1 << i for i, d in enumerate(demands)
                      if all(x <= y for x, y in zip(d, r))) for r in candidates]
    full = (1 << len(demands)) - 1
    original = all_covers(signatures)
    retained_indices = list(range(0, 2 * m - 1, 2))
    retained_mask = sum(1 << j for j in retained_indices)
    tc = all_covers(signatures, retained_indices)
    assert [(size, mask) for size, mask, cov in original if cov == full and size <= m] == [(m, retained_mask)]
    even_mask = sum(1 << j for j in range(1, 2 * m - 1, 2))
    future = (1 << len(edge_demands)) - 1
    assert tau(original, future) == m - 1 and tau(tc, future) == m
    assert [(size, mask) for size, mask, cov in original
            if not future & ~cov and size <= m - 1] == [(m - 1, even_mask)]
    certificates = [(full ^ cov, mask) for size, mask, cov in original
                    if tau(tc, cov) > size]
    onset = min(deleted.bit_count() for deleted, _ in certificates)
    witnesses = [(deleted, mask) for deleted, mask in certificates if deleted.bit_count() == onset]
    assert onset == m
    assert witnesses == [(full ^ future, even_mask)]
    assert max(tau(tc, s) for s in signatures) == 2
    star_onset = min((full ^ s).bit_count() for s in signatures if tau(tc, s) > 1)
    assert star_onset == (2 * m - 4) * q + m
    return dict(m=m, candidates=len(candidates), demands=len(demands),
                onset=onset, earliest_loss=f"{m}/{m-1}", required_discarded=m-1,
                single_star_deletions=star_onset, unrestricted_worst_loss=2)


if __name__ == "__main__":
    result = {"general_incidence": generic_audit(),
              "planar_nonlocality": [planar_path(m) for m in range(3, 9)]}
    output = Path(__file__).with_name("stability_v4_results.json")
    output.write_text(json.dumps(result, indent=2), encoding="utf-8")
    print(json.dumps(result, indent=2))
