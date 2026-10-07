#!/usr/bin/env python3
"""Independent finite-dimensional checks for the Round 7 fixed-K certificate.

These reproducible numerical checks are not proofs.  The physical generator
builds conductances and diagonal capacities before forming Q and B.  No target
CP factor is used to construct the physical cases.

Definitions: U,V each contain n boundary ports; S = sum(D[U,V]); d = S/n is
the average left output when all right inputs have amplitude one.  It is not
the average over n**2 matrix entries.  W_U and W_V are ORDERED off-diagonal
sums in their respective principal blocks.
"""
from __future__ import annotations

import json
import math
from pathlib import Path

import numpy as np
from scipy.linalg import block_diag, eigh, expm, solve


SEED = 20260922
RNG = np.random.default_rng(SEED)
TOL = 2e-8


def laplacian_from_edges(size, edges):
    out = np.zeros((size, size))
    for i, j, g in edges:
        out[i, i] += g
        out[j, j] += g
        out[i, j] -= g
        out[j, i] -= g
    return out


def physical_case(index, approximate=False):
    n = int(RNG.integers(1, 7))
    lam = float(10 ** RNG.uniform(-1, 1))
    kappa = lam / n
    delta = float(kappa * RNG.uniform(0.001, 0.3)) if approximate else 0.0
    kcross = (kappa + RNG.uniform(-delta, delta, (n, n))
              if approximate else np.full((n, n), kappa))
    num_components = 0 if index == 0 else int(RNG.integers(1, 13))
    comps = []
    for _ in range(num_components):
        i, j = map(int, RNG.integers(0, n, 2))
        size = int(RNG.integers(1, 5))
        caps = 10 ** RNG.uniform(-1, 1, size)
        internal = laplacian_from_edges(size, [
            (a, a + 1, float(10 ** RNG.uniform(-1, 1)))
            for a in range(size - 1)
        ])
        spokes = np.zeros((size, 2))
        if RNG.random() < 0.5:
            spokes[0, 0] = 10 ** RNG.uniform(-1, 1)
            spokes[-1, 1] = 10 ** RNG.uniform(-1, 1)
        else:
            spokes = 10 ** RNG.uniform(-1, 1, (size, 2))
        lint = internal + np.diag(spokes.sum(axis=1))
        cross0 = float((spokes.T @ solve(lint, spokes, assume_a="pos"))[0, 1])
        comps.append(dict(i=i, j=j, size=size, caps=caps, lint=lint,
                          spokes=spokes, cross0=cross0))
    for i in range(n):
        for j in range(n):
            chosen = [c for c in comps if c["i"] == i and c["j"] == j]
            if not chosen:
                continue
            weights = RNG.dirichlet(np.ones(len(chosen)))
            occupancy = 1.0 if index % 13 == 0 else float(RNG.uniform(0.02, 0.98))
            for c, weight in zip(chosen, weights):
                alpha = occupancy * kcross[i, j] * weight / c["cross0"]
                c["lint"] *= alpha
                c["spokes"] *= alpha
    r = sum(c["size"] for c in comps)
    if r:
        lint = block_diag(*(c["lint"] for c in comps))
        caps = np.concatenate([c["caps"] for c in comps])
        spokes = np.zeros((r, 2 * n))
        offset = 0
        for c in comps:
            sl = slice(offset, offset + c["size"])
            spokes[sl, c["i"]] = c["spokes"][:, 0]
            spokes[sl, n + c["j"]] = c["spokes"][:, 1]
            offset += c["size"]
        cinvhalf = 1 / np.sqrt(caps)
        Q = cinvhalf[:, None] * lint * cinvhalf[None, :]
        B = cinvhalf[:, None] * spokes
        M0 = B.T @ solve(Q, B, assume_a="pos")
        poles, eigenvectors = eigh(Q)
        assert poles[0] > 0
    else:
        Q, B = np.empty((0, 0)), np.empty((0, 2 * n))
        M0 = np.zeros((2 * n, 2 * n))
        spokes = np.zeros((0, 2 * n))
        poles, eigenvectors = np.array([]), np.empty((0, 0))
    direct_cross = kcross - M0[:n, n:]
    assert direct_cross.min() >= -TOL * max(1., kappa)
    direct = laplacian_from_edges(2 * n, [
        (i, n + j, max(0., direct_cross[i, j]))
        for i in range(n) for j in range(n)
    ])
    Lbb = direct + np.diag(spokes.sum(axis=0))
    K = Lbb - M0
    expected_K = laplacian_from_edges(2 * n, [
        (i, n + j, kcross[i, j]) for i in range(n) for j in range(n)
    ])
    assert np.max(np.abs(K - expected_K)) <= TOL * max(1., np.max(np.abs(K)))
    h = float(10 ** RNG.uniform(-1, 1) / lam)
    wait = 0.0 if index % 11 == 0 else float(RNG.uniform(0.01, 1) / lam)
    duration = 0.1 / lam  # each uniform factor; total ramp duration = 2*duration
    results = []
    for protocol in ("ideal_step", "triangular_derivative_ramp"):
        if r:
            ah = -np.expm1(-poles * h) / poles
            ph = np.ones(r) if protocol == "ideal_step" else (
                -np.expm1(-poles * duration) / (poles * duration))
            f = np.exp(-poles * wait) * ph**2 * ah**2
            VtB = eigenvectors.T @ B
            D = VtB.T @ (f[:, None] * VtB)
            # Independent matrix-exponential factor computation, without the
            # eigenvectors used for D. A_h(Q)=Q^-1(I-exp(-Q*h)).
            ah_matrix = solve(Q, np.eye(r) - expm(-Q * h), assume_a="pos")
            ramp_matrix = (np.eye(r) if protocol == "ideal_step" else
                           solve(Q, np.eye(r) - expm(-Q * duration),
                                 assume_a="pos") / duration)
            F = expm(-Q * wait / 2) @ ramp_matrix @ ah_matrix @ B
            factor_error = float(np.max(np.abs(D - F.T @ F)))
            factor_min = float(F.min())
            assert factor_error <= TOL * max(1., float(np.max(np.abs(D))))
            assert factor_min >= -TOL * max(1., float(np.max(np.abs(F))))
        else:
            D = np.zeros((2 * n, 2 * n))
            factor_error, factor_min = 0.0, 0.0
        within_u = D[:n, :n] - np.diag(np.diag(D[:n, :n]))
        within_v = D[n:, n:] - np.diag(np.diag(D[n:, n:]))
        within_max = float(max(np.max(np.abs(within_u)), np.max(np.abs(within_v))))
        S = float(D[:n, n:].sum())
        d = S / n
        b = float(D[:n, n:].max())
        cap = h * (kappa + delta)
        psd_kernel_min = float(np.linalg.eigvalsh(h * M0 - D).min())
        entrywise_kernel_min = float((h * M0 - D).min())
        assert within_max <= TOL * max(1., float(np.max(np.abs(D))))
        assert entrywise_kernel_min >= -TOL * max(1., float(np.max(np.abs(h * M0))))
        assert psd_kernel_min >= -TOL * max(1., float(np.max(np.abs(h * M0))))
        assert S <= r * b + TOL * max(1., S)
        assert b <= cap + TOL * max(1., cap)
        assert d <= r * cap / n + TOL * max(1., d)
        # An observation a with known error epsilon can be above the true d;
        # the conservative lower endpoint remains d in this constructed case.
        epsilon = float(RNG.uniform(0, 0.1) * max(1., d))
        a = d + epsilon
        inferred_lower = n * max(0., a - epsilon) / cap
        assert inferred_lower <= r + TOL * max(1., r)
        results.append(dict(
            index=index, protocol=protocol, n=n, hidden_states=r,
            components=num_components, approximate_K=approximate,
            lambda_reference=lam, kappa=kappa, delta=delta, h=h, wait=wait,
            ramp_factor_duration=(0.0 if protocol == "ideal_step" else duration),
            S=S, d_average_cross_row_sum=d, mean_cross_entry=S/(n*n),
            b=b, cross_entry_cap=cap, row_mean_bound=r*cap/n,
            inferred_state_lower=inferred_lower,
            bound_ratio=(d/(r*cap/n) if r else 0.0),
            within_offdiag_max_abs=within_max,
            entrywise_hM0_minus_D_min=entrywise_kernel_min,
            psd_hM0_minus_D_min=psd_kernel_min,
            nonnegative_factor_min=factor_min,
            independent_factor_error=factor_error,
            min_pole=(float(poles[0]) if r else None),
            max_pole=(float(poles[-1]) if r else None)))
    return results


def check_root_leak(F, n, label):
    D = F.T @ F
    r = len(F)
    du, dv, cross = D[:n, :n], D[n:, n:], D[:n, n:]
    TU, TV = float(np.trace(du)), float(np.trace(dv))
    # Explicit off-diagonal extraction avoids cancellation at tiny leakage.
    WU = float(du[~np.eye(n, dtype=bool)].sum())
    nv = len(dv)
    WV = float(dv[~np.eye(nv, dtype=bool)].sum())
    S, b = float(cross.sum()), float(cross.max())
    penalty = math.sqrt(TU * WV) + math.sqrt(TV * WU) + math.sqrt(WU * WV)
    bound = r * b + penalty
    assert S <= bound + TOL * max(1., S, bound)
    lower = max(0., S - penalty) / b if b else 0.0
    assert lower <= r + TOL * max(1., r)
    return dict(label=label, rows=r, nU=n, nV=nv, S=S, b=b,
                TU=TU, TV=TV, WU=WU, WV=WV, penalty=penalty,
                upper_bound=bound, bound_ratio=(S/bound if bound else 0.0),
                inferred_factor_rows_lower=lower)


def random_cp_case(index):
    n = int(RNG.integers(1, 10))
    nv = int(RNG.integers(1, 10))
    r = int(RNG.integers(1, 25))
    if index % 3 == 0:
        F = 10 ** RNG.uniform(-7, -2, (r, n + nv))
        for row in F:
            row[int(RNG.integers(n))] = 10 ** RNG.uniform(-2, 2)
            row[n + int(RNG.integers(nv))] = 10 ** RNG.uniform(-2, 2)
    else:
        F = 10 ** RNG.uniform(-3, 3, (r, n + nv))
        F[RNG.random(F.shape) < RNG.uniform(0, 0.95)] = 0
    return check_root_leak(F, n, f"random_{index}")


def main():
    physical = []
    for i in range(250):
        physical.extend(physical_case(i, approximate=(i >= 200)))
    cp = [random_cp_case(i) for i in range(750)]
    cp.extend([
        check_root_leak(np.zeros((3, 4)), 2, "zero"),
        check_root_leak(np.array([[1., 0, 0, 0], [0, 2., 0, 0]]), 2, "only_U"),
        check_root_leak(np.ones((1, 7)), 3, "rank_one_dense"),
        check_root_leak(np.array([[1., 0, 1, 0], [0, 1., 0, 1.]]), 2,
                        "zero_leak_equality"),
        check_root_leak(np.array([[1., 0, 1, 0], [1., 0, 1, 0.]]), 2,
                        "repeated_pair_strict"),
    ])
    report = dict(
        seed=SEED,
        status="all_assertions_passed",
        caveat="Numerical validation only; not a proof or novelty claim.",
        conventions=dict(
            n="boundary ports per partition in physical cases",
            S="sum over U x V block, each cross entry counted once",
            d="S/n, average output on U under equal unit inputs on V",
            within_leak="ordered off-diagonal sums, not unordered edge sums",
            K_budget="-K_ij <= kappa + delta on cross entries",
            exact_bound="d <= r*h*lambda/n^2 when kappa=lambda/n and delta=0",
            approximate_bound="r >= n*max(a-epsilon,0)/(h*(kappa+delta))",
            ramp="derivative is convolution of two uniform probability densities"),
        summary=dict(
            physical_networks=250,
            physical_protocol_checks=len(physical),
            exact_K_networks=200,
            approximate_K_networks=50,
            random_CP_cases=750,
            deterministic_CP_edge_cases=5,
            max_physical_bound_ratio=max(x["bound_ratio"] for x in physical),
            max_CP_leak_bound_ratio=max(x["bound_ratio"] for x in cp),
            max_within_zero_error=max(x["within_offdiag_max_abs"] for x in physical),
            max_independent_factor_error=max(x["independent_factor_error"] for x in physical),
            min_nonnegative_factor_entry=min(x["nonnegative_factor_min"] for x in physical),
            min_entrywise_hM0_minus_D=min(x["entrywise_hM0_minus_D_min"] for x in physical),
            min_psd_hM0_minus_D=min(x["psd_hM0_minus_D_min"] for x in physical)),
        physical_cases=physical,
        CP_leak_cases=cp)
    output = Path(__file__).with_suffix(".json")
    output.write_text(json.dumps(report, ensure_ascii=False, indent=2) + "\n")
    print(json.dumps(report["summary"], indent=2))
    print(f"Saved {output}")


if __name__ == "__main__":
    main()
