"""Portable demonstration of the exact Erlang-envelope state allocation.

All computations use the Python standard library.  The analytical variational
theorem is in round9_weighted.md.  Printed floating values are not interval
certificates.  V_r is a physical SUPREMUM, not necessarily an attained maximum.
"""
import json
import math
from pathlib import Path


def erlang_window(shape, rate, left, right):
    """P(left <= Gamma(integer shape, rate) <= right)."""
    def survival(x):
        term = 1.0
        terms = [term]
        for k in range(1, shape):
            term *= x / k
            terms.append(term)
        return math.exp(-x) * math.fsum(terms)
    return survival(rate * left) - survival(rate * right)


def constant(k):
    if k == 0:
        return 0.0
    return math.exp(k * math.log(k) + 1 - k - math.lgamma(k))


def allocate(weights, envelope, budget):
    """Independent max-plus dynamic program; returns a maximizing allocation."""
    states = [(0.0, ()) for _ in range(budget + 1)]
    for weight in weights:
        states = [max((states[s-k][0] + weight * envelope[k],
                       states[s-k][1] + (k,)) for k in range(s + 1))
                  for s in range(budget + 1)]
    return states[budget]


def main():
    left, right = .9, 1.1
    weights = [1.0, .5, .1]
    max_budget = 8
    q_shapes = [0.0]
    envelope = [0.0]
    rates = [0.0]
    for j in range(1, max_budget + 1):
        rate = j * math.log(right / left) / (right - left)
        value = erlang_window(j, rate, left, right)
        # Derivative sign follows exactly from b^j exp(-rho b)-a^j exp(-rho a).
        # These checks corroborate the implementation of the unique rate maximum.
        assert value > erlang_window(j, .95 * rate, left, right)
        assert value > erlang_window(j, 1.05 * rate, left, right)
        rates.append(rate)
        q_shapes.append(value)
        envelope.append(max(envelope[-1], value))

    q = q_shapes[1]
    universal = [min(1.0, q * constant(k)) for k in range(max_budget + 1)]
    gains = sorted((c * (universal[k] - universal[k-1])
                    for c in weights for k in range(1, max_budget + 1)), reverse=True)
    rows = []
    for r in range(1, max_budget + 1):
        exact_supremum, allocation = allocate(weights, envelope, r)
        concave_upper = math.fsum(gains[:r])
        stars = q * math.fsum(sorted(weights, reverse=True)[:r])
        assert stars <= exact_supremum + 1e-14
        assert exact_supremum <= concave_upper + 1e-14
        relaxation_dp, _ = allocate(weights, universal, r)
        assert math.isclose(relaxation_dp, concave_upper, rel_tol=1e-13)
        rows.append({"states": r, "erlang_envelope_allocation": allocation,
                     "physical_supremum": exact_supremum,
                     "universal_concave_upper": concave_upper,
                     "attainable_distinct_star_value": stars})

    result = {"kernel": {"type": "indicator", "interval": [left, right]},
              "weighted_static_budgets": weights,
              "erlang_optimal_rates": rates[1:],
              "erlang_optimal_probabilities": q_shapes[1:],
              "state_allocation": rows,
              "status": "Analytic rate optimization; floating evaluation. Physical supremum may not be attained."}
    Path(__file__).with_suffix(".json").write_text(json.dumps(result, indent=2))
    print(json.dumps(result, indent=2))


if __name__ == "__main__":
    main()
