"""Exact rational margins for the Round 6 coordinate-plane exclusion.

The mathematical implication is proved in round6_geometry.md; this script
certifies the chosen constants and strict signs without floating-point tests.
"""
from fractions import Fraction as Q
from pathlib import Path
import json


def certify(e):
    assert Q(1, 6) < e < Q(1, 4)
    m, M, L, D = 1-e, 1+e, 2-e, 2+e
    assert 0 < e < m <= M < L <= D
    A = max(L, 1/e-4+e)
    V = min(M, 2*e*m/(1-4*e))
    R = min(M, 2*D*e*m/(e*e+m*m))
    U = (1-4*e)/2
    assert 0 < U <= e < m
    assert L <= A <= D
    assert m <= V <= M and m <= R <= M
    assert A > R
    assert m*m > D*e
    assert D*m > M*e
    assert A*m > R*e
    Pmax = (A*(U*U+V*V)-2*R*U*V)/(A*A-R*R)
    assert Pmax >= 0
    assert L-Pmax > M
    return dict(error_budget=e, m=m, M=M, L=L, D=D,
                A=A, U=U, V=V, R=R,
                opposite_pair_margin=m*m-D*e,
                projected_norm_upper=Pmax,
                fourth_edge_margin=L-M-Pmax)


def main():
    main_result = certify(Q(11, 62))
    # A slightly larger rational budget certifies a uniform strict margin
    # for general-position approximation of a boundary/degenerate factor.
    perturbation_result = certify(Q(17742, 100000))
    assert perturbation_result['error_budget'] > main_result['error_budget']
    data = {'status': 'Exact rational assertions passed',
            'proved_lower_bound': str(main_result['error_budget']),
            'main_exact': {k: str(v) for k,v in main_result.items()},
            'display_only': {k: float(v) for k,v in main_result.items()},
            'strict_perturbation_budget': str(perturbation_result['error_budget']),
            'strict_perturbation_margin': str(perturbation_result['fourth_edge_margin']),
            'pairwise_independence_directly_from_L_greater_than_M': True,
            'global_optimality_claimed': False}
    output = Path(__file__).with_name('round6_geometry_certificate.json')
    output.write_text(json.dumps(data, indent=2)+'\n')
    print(json.dumps(data, indent=2))


if __name__ == '__main__':
    main()
