"""Explicit finite three-state RC construction; standard library only.

All unscaled physical coefficients are rational. The strict signal threshold
is certified with rational Taylor bounds, independently of Decimal display.
"""
import json
from decimal import Decimal, localcontext
from fractions import Fraction as F
from pathlib import Path


def exp_negative_interval(x):
    term = F(1)
    total = term
    for n in range(1, 62):
        term *= -x / n
        total += term
        if n == 60:
            upper = total
    return total, upper  # odd partial sum is lower, even is upper


def q_interval(rate):
    al, ah = exp_negative_interval(F(9, 10) * rate)
    bl, bh = exp_negative_interval(F(11, 10) * rate)
    return al - bh, ah - bl


def main():
    a, b = F(9, 5), F(11, 5)
    qal, qah = q_interval(a)
    qbl, qbh = q_interval(b)
    q1l, q1h = q_interval(F(1))
    hlo = (b * qal - a * qbh) / (b - a)
    hhi = (b * qah - a * qbl) / (b - a)
    slo, shi = hlo + q1l / 2, hhi + q1h / 2
    assert slo > F(7, 50)

    with localcontext() as context:
        context.prec = 70
        D = Decimal
        def q(rate):
            return (-D('.9') * rate).exp() - (-D('1.1') * rate).exp()
        H = (D('2.2') * q(D('1.8')) - D('1.8') * q(D('2.2'))) / D('.4')
        S = H + q(D(1)) / 2
        theta = D('.14') / S
        output = {
            "boundary_path": ["b0", "b1", "b2", "b3"],
            "static_edge_budgets": ["1", "1/2", "1/10"],
            "kernel": "indicator of [9/10,11/10]",
            "unscaled_capacities": {"x1": "55/9", "x2": "55/9", "x3": "2"},
            "unscaled_conductors": [
                ["b0", "x1", "11"], ["x1", "x2", "11/9"], ["x2", "b1", "11"],
                ["b1", "x3", "1"], ["x3", "b2", "1"], ["b2", "b3", "1/10"]],
            "strong_edge_rates": ["9/5", "11/5"],
            "weak_edge_rate": "1",
            "strong_edge_statistic": str(H),
            "total_statistic": str(S),
            "margin_over_0.14": str(S - D('.14')),
            "rational_certificate": {
                "threshold": "7/50",
                "proved_lower_bound": "1447470384394509/10000000000000000",
                "check": bool(slo > F(1447470384394509, 10**16) > F(7, 50)),
                "series_upper_order": 60,
                "series_lower_order": 61,
                "interval_width_less_than": "1e-55",
                "width_check": bool(shi - slo < F(1, 10**55))},
            "exact_target_scaling": {
                "theta_definition": "theta=(7/50)/S, with S given by the exact exponential expression",
                "theta_decimal": str(theta),
                "capacities": {"x1": "55 theta/9", "x2": "55 theta/9", "x3": "2 theta"},
                "conductors": [
                    ["b0", "x1", "11 theta"], ["x1", "x2", "11 theta/9"], ["x2", "b1", "11 theta"],
                    ["b1", "x3", "theta"], ["x3", "b2", "theta"],
                    ["b0", "b1", "1-theta"], ["b1", "b2", "(1-theta)/2"], ["b2", "b3", "1/10"]],
                "exact_total_statistic": "7/50",
                "proof": "Dynamic conductances and capacities scale equally, preserving Q; static budgets and statistics scale by theta. Added direct edges restore K and contribute no transient statistic."}}
        assert output["rational_certificate"]["check"]
        assert output["rational_certificate"]["width_check"]
        Path(__file__).with_suffix('.json').write_text(json.dumps(output, indent=2))
        print(json.dumps(output, indent=2))


if __name__ == '__main__':
    main()
