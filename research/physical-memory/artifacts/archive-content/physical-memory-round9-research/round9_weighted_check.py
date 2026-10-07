"""Numerical corroboration only; analytic proofs are in round9_weighted.md."""
import heapq
import json
import math
from pathlib import Path
import random

import numpy as np
from scipy.integrate import quad
from scipy.linalg import eigh


def q(x):
    return math.exp(-x / 10) * (-math.expm1(-x / 10) / (x / 10)) ** 2 * (-math.expm1(-x)) ** 2 / x


def constant(k):
    return 0.0 if k == 0 else math.exp(k * math.log(k) - k + 1 - math.lgamma(k))


q_star = 0.32764158598953086
w_star = 29 / 30
d = [min(q_star * constant(k), w_star) for k in range(9)]
gains = np.diff(d)
assert min(gains) > 0
assert max(np.diff(gains)) < 0

# Independent finite allocation dynamic program versus marginal sorting.
rng = random.Random(73152)
max_disagreement = 0.0
for _ in range(200):
    m = rng.randrange(1, 8)
    weights = [10 ** rng.uniform(-2, 2) for _ in range(m)]
    r = rng.randrange(8 * m + 1)
    sorted_value = sum(sorted((c * v for c in weights for v in gains), reverse=True)[:r])
    table = [0.0] + [-math.inf] * r
    for c in weights:
        nxt = [-math.inf] * (r + 1)
        for used, value in enumerate(table):
            for k in range(min(8, r - used) + 1):
                nxt[used + k] = max(nxt[used + k], value + c * d[k])
        table = nxt
    dp_value = max(table)
    max_disagreement = max(max_disagreement, abs(dp_value - sorted_value))
    assert math.isclose(dp_value, sorted_value, rel_tol=2e-14, abs_tol=2e-14)

# Physically assembled two-state path, independently normalized by its static cross response.
C = np.diag([4.0, 4.0])
L = np.array([[6.0, -2.0], [-2.0, 6.0]])
R = np.diag(1 / np.sqrt(np.diag(C)))
Q = R @ L @ R
u = R @ np.array([4.0, 0.0])
v = R @ np.array([0.0, 4.0])
rate, vectors = eigh(Q)
residue = (u @ vectors) * (v @ vectors)
static_cross = float(sum(residue / rate))
response = float(sum(residue * np.array([q(x) for x in rate]) / rate))
formula_response = 2 * q(1) - q(2)
assert math.isclose(static_cross, 1.0, abs_tol=1e-14)
assert math.isclose(response, formula_response, abs_tol=1e-14)
top_two_distinct_stars = 1.1 * q_star
assert response > top_two_distinct_stars

out = {
    "status": "analytic proof plus numerical corroboration; not novelty certification",
    "d_values": d,
    "marginal_gains": list(gains),
    "allocation_cases": 200,
    "max_dp_sort_disagreement": max_disagreement,
    "counterexample": {
        "static_conductance": static_cross,
        "rates": list(rate),
        "two_state_path_response": response,
        "two_distinct_stars_maximum": top_two_distinct_stars,
        "strict_gap": response - top_two_distinct_stars,
    },
}
Path(__file__).with_suffix(".json").write_text(json.dumps(out, indent=2))
print(json.dumps(out, indent=2))
