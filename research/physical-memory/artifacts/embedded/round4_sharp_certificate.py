"""Reproduce sharp aggregate bounds and the physical design constants.

Python standard library only. The general theorem is proved in the HTML;
these finite checks verify explicit attaining factors and implementation.
This script does not claim a global solution of the H0 approximation problem.
"""
from pathlib import Path
import json
import math


def envelope_squared(d, z):
    d = max(0.0, d)
    z = min(max(0.0, z), d)
    return min(z*(2*d-z), (d+z)**2/4)


def gram(f):
    return [[sum(row[i]*row[j] for row in f) for j in range(4)]
            for i in range(4)]


def attaining_factor(d, z):
    assert d > 0 and 0 <= z <= d
    if z <= d/5:
        a, b, c = math.sqrt(z/2), math.sqrt(d-z/2), math.sqrt(d-2*z)
        return [[0,a,b,2*a],[2*a,b,a,0],[c,0,0,c]]
    if z == d:
        return [[math.sqrt(d)]*4,[0]*4,[0]*4]
    # Scaled H_rho with rho=2z/(d-z), using the known octant rotation.
    s = (d-z)/2
    h = math.sqrt((d+z)/(d-z))
    q = math.sqrt(3/8)
    return [[math.sqrt(s)*v for v in row] for row in
            [[h/2-q,h/2+q,h/2+q,h/2-q],
             [q*h-1/4,q*h-3/4,q*h+1/4,q*h+3/4],
             [q*h+3/4,q*h+1/4,q*h-3/4,q*h-1/4]]]


def phi(x):
    return -math.expm1(-x)/x if x else 1.0


def main():
    cycles = [(0,1),(1,2),(2,3),(3,0)]
    worst = 0.0
    count = 0
    for d in [1e-6,1.0,1e6]:
        for ratio in [0,.001,.01,.05,.1,.199,.2,.201,.4,.75,1]:
            z = d*ratio
            f = attaining_factor(d,z)
            a = gram(f)
            assert min(min(row) for row in f) >= -1e-12*math.sqrt(d)
            m = min(a[i][j] for i,j in cycles)
            error = max(max(abs(a[i][i]-d) for i in range(4)),
                        abs(a[0][2]-z),abs(a[1][3]-z),
                        abs(m-math.sqrt(envelope_squared(d,z))))/d
            assert error < 5e-13
            worst = max(worst,error)
            count += 1
    lam,total_rise,tau = .25,1.,.1
    h = 1.2564312086261697/lam
    linear_a = math.exp(-lam*tau)*phi(lam*total_rise)*(-math.expm1(-lam*h))**2
    quadratic_a = math.exp(-lam*tau)*phi(lam*total_rise/2)**2*(-math.expm1(-lam*h))**2
    result = dict(
        theorem_source='Brandts-Krizek 2016 Corollary 3.6; quantitative specialization derived here',
        exact_noise_radius='1/6 (sufficient open max-entry ball; not the exact distance)',
        attaining_factor_cases=count,
        maximum_relative_factor_error=worst,
        full_matrix_distance_lower='1/6',
        full_matrix_distance_upper_strict='0.196676467057347',
        design=dict(s_J_per_K=1.,lambda_per_second=lam,total_rise_seconds=total_rise,
                    hold_seconds=tau,window_seconds=h,
                    linear_coefficient=linear_a,quadratic_coefficient=quadratic_a,
                    linear_heat_flow_floor_W_per_K=linear_a/(12*h),
                    quadratic_heat_flow_floor_W_per_K=quadratic_a/(12*h)),
        scope='Synthetic mathematical model; no laboratory measurement. Attainment concerns aggregate constraints, not all entries of the H0 error box.')
    (Path(__file__).resolve().parent/'round4-sharp-results.json').write_text(json.dumps(result,indent=2))
    print(json.dumps(result,indent=2))


if __name__ == '__main__':
    main()
