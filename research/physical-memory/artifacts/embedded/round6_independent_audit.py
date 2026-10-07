"""Independent numerical checks accompanying round6_independent_audit.md.
Analytic arguments are in the note; floating-point checks are not proofs.
"""
import json
import math
from pathlib import Path
import numpy as np


H0 = np.array([[2, 1, 0, 1], [1, 2, 1, 0],
               [0, 1, 2, 1], [1, 0, 1, 2]], dtype=float)
J = np.ones((4, 4))
A = H0 - 2 * np.eye(4)
K = 2 * np.eye(4) - A
CB = 4 * np.eye(4)


def e_integral(rate, left, right):
    return (math.exp(-rate * left) - math.exp(-rate * right)) / rate


def two_window(fun_integral, T, h):
    return fun_integral(T, T+h) - fun_integral(T+h, T+2*h)


def F3(rho):
    h, q = math.sqrt(1+rho), math.sqrt(3/8)
    return np.array([[h/2-q, h/2+q, h/2+q, h/2-q],
                     [q*h-.25, q*h-.75, q*h+.25, q*h+.75],
                     [q*h+.75, q*h+.25, q*h-.75, q*h-.25]])


def F4(rho):
    F0 = np.array([[1, 1, 0, 0], [0, 1, 1, 0],
                   [0, 0, 1, 1], [1, 0, 0, 1]], dtype=float)
    return F0 + ((math.sqrt(1+rho)-1)/2) * J


def main():
    result = {'checks_are_numerical': True}
    # Zero-internal-node sensor counterexample.
    T, h = .7, .8
    y = lambda t: K + H0 * math.exp(-t)
    iy = lambda l, r: K * (r-l) + H0 * e_integral(1, l, r)
    Dy = two_window(iy, T, h)
    Ey = 2*y(T+h) - y(T) - y(T+2*h)
    coefficient = math.exp(-T) * (1-math.exp(-h))**2
    result['fake_sensor'] = {
        'coefficient': coefficient,
        'uncorrected_residual': float(np.max(np.abs(Dy-coefficient*H0))),
        'corrected_residual': float(np.max(np.abs(Dy+Ey))),
        'K_min_eigenvalue': float(np.linalg.eigvalsh(K).min()),
        'K_row_sums': K.sum(axis=1).tolist(),
    }
    assert np.max(np.abs(Dy-coefficient*H0)) < 1e-14
    assert np.max(np.abs(Dy+Ey)) < 1e-14

    # General first-order sensor: q(t)=q0+sum weights exp(-alpha t).
    # Independent exact antiderivatives; nonzero sensor initialization.
    records = []
    q0, weights, rates, initial = 1.7, [2.3, -.4], [.31, 1.73], -1.2
    for beta in [.2, .9, 3.1, 7.0]:
        for T, h in [(.03, .07), (.5, .8), (1.4, 2.0)]:
            def y(t):
                return q0 + (initial-q0)*math.exp(-beta*t) + sum(
                    w*beta/(beta-a)*(math.exp(-a*t)-math.exp(-beta*t))
                    for w, a in zip(weights, rates))
            def iq(l, r):
                return q0*(r-l) + sum(w*e_integral(a, l, r)
                                      for w, a in zip(weights, rates))
            def iy(l, r):
                return q0*(r-l) + (initial-q0)*e_integral(beta, l, r) + sum(
                    w*beta/(beta-a)*(e_integral(a, l, r)-e_integral(beta, l, r))
                    for w, a in zip(weights, rates))
            Dq, Dy = two_window(iq, T, h), two_window(iy, T, h)
            Ey = 2*y(T+h)-y(T)-y(T+2*h)
            residual = abs(Dq-Dy-Ey/beta)
            assert residual < 3e-14
            records.append({'beta': beta, 'T': T, 'h': h, 'residual': residual})
    result['sensor_identity'] = records

    # Shared-endpoint composite trapezoidal weights and exact l1 noise bound.
    trap_records = []
    for N in [1, 2, 5, 10]:
        h = .8
        dt = h/N
        for tau in [.01, .2, 1.0]:
            w = np.r_[dt/2, np.full(N-1, dt), 0.,
                      np.full(N-1, -dt), -dt/2]
            w[0] -= tau
            w[N] += 2*tau
            w[-1] -= tau
            exact = abs(dt/2-tau)+3*tau+dt/2+2*(N-1)*dt
            assert abs(np.sum(np.abs(w))-exact) < 1e-14
            trap_records.append({'N': N, 'tau': tau, 'l1_weight': exact})
    result['trapezoid_noise_weights'] = trap_records

    factor_records = []
    for rho in [1e-6, .1, .49, .5, .500001, .7, 1., 5.]:
        expected = H0 + rho*J
        g4 = F4(rho)
        assert g4.min() > 0
        assert np.max(np.abs(g4.T@g4-expected)) < 2e-14
        record = {'rho': rho, 'F4_min': float(g4.min()),
                  'F4_gram_residual': float(np.max(np.abs(g4.T@g4-expected)))}
        if rho >= .5:
            g3 = F3(rho)
            assert g3.min() >= -2e-16
            if rho > .5: assert g3.min() > 0
            assert np.max(np.abs(g3.T@g3-expected)) < 2e-14
            record.update(F3_min=float(g3.min()),
                          F3_gram_residual=float(np.max(np.abs(g3.T@g3-expected))))
        factor_records.append(record)
    result['factors'] = factor_records

    # Gain cancellation through symmetric geometric means.
    H = H0+.3*J
    a, b = np.array([.3, 2., 1.2, 4.]), np.array([3., .7, 2., .4])
    M = a[:, None] * H * b[None, :]
    C = np.sqrt(M*M.T/np.outer(np.diag(M), np.diag(M)))
    normalized_H = H / np.sqrt(np.outer(np.diag(H), np.diag(H)))
    result['gain_normalization_residual'] = float(np.max(np.abs(C-normalized_H)))
    assert np.max(np.abs(C-normalized_H)) < 1e-14

    out = Path(__file__).with_suffix('.json')
    out.write_text(json.dumps(result, indent=2)+'\n')
    print('All independent numerical checks passed.')
    print('Maximum sensor identity residual:', max(x['residual'] for x in records))
    print('Results:', out)


if __name__ == '__main__':
    main()
