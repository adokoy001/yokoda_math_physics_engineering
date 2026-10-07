"""Exact rational certificate for a CP-rank <= 3 approximation of C4.

Python standard library only. No numerical optimizer or floating-point decision
is used. The decimal display is obtained by outward rational rounding.
"""
from dataclasses import dataclass
from fractions import Fraction as Q
import json
from pathlib import Path


@dataclass(frozen=True)
class Interval:
    lo: Q
    hi: Q

    def __init__(self, lo, hi=None):
        object.__setattr__(self, 'lo', Q(lo))
        object.__setattr__(self, 'hi', Q(lo if hi is None else hi))
        assert self.lo <= self.hi

    @staticmethod
    def cast(x):
        return x if isinstance(x, Interval) else Interval(x)

    def __add__(self, other):
        other = self.cast(other)
        return Interval(self.lo + other.lo, self.hi + other.hi)

    __radd__ = __add__

    def __neg__(self):
        return Interval(-self.hi, -self.lo)

    def __sub__(self, other):
        return self + -self.cast(other)

    def __rsub__(self, other):
        return self.cast(other) + -self

    def __mul__(self, other):
        other = self.cast(other)
        ends = [self.lo * other.lo, self.lo * other.hi,
                self.hi * other.lo, self.hi * other.hi]
        return Interval(min(ends), max(ends))

    __rmul__ = __mul__

    def reciprocal(self):
        assert self.lo > 0 or self.hi < 0, 'Division interval contains zero'
        return Interval(1 / self.hi, 1 / self.lo)

    def __truediv__(self, other):
        return self * self.cast(other).reciprocal()

    def __rtruediv__(self, other):
        return self.cast(other) / self

    def __pow__(self, n):
        assert isinstance(n, int) and n >= 0
        out = Interval(1)
        for _ in range(n):
            out = out * self
        return out

    def decimal_enclosure(self, digits=12):
        # Floor lower endpoint; ceil upper endpoint, using integer arithmetic.
        scale = 10 ** digits
        lower = (self.lo.numerator * scale) // self.lo.denominator
        upper = -((-self.hi.numerator * scale) // self.hi.denominator)
        def render(n):
            sign = '-' if n < 0 else ''
            whole, frac = divmod(abs(n), scale)
            return f'{sign}{whole}.{frac:0{digits}d}'
        return [render(lower), render(upper)]


def poly(x):
    return 2 - 11*x + 3*x*x - 2*x**3 + 42*x**4 - 4*x**6


def polynomial_product(a, b):
    out = [Q(0)] * (len(a) + len(b) - 1)
    for i, x in enumerate(a):
        for j, y in enumerate(b):
            out[i+j] += x*y
    return out


def polynomial_subtract(a, b):
    size = max(len(a), len(b))
    return [(a[i] if i < len(a) else 0) -
            (b[i] if i < len(b) else 0) for i in range(size)]


def main():
    # Root isolation: decimal endpoints have denominator 10^15.
    lo = Q(196676467057346, 10**15)
    hi = Q(196676467057347, 10**15)
    assert poly(lo) > 0 and poly(hi) < 0
    assert 0 < lo < hi < Q(1, 5)
    # P'(s) <= -11 + 6/5 + 168/125 = -1057/125 < 0
    # for 0 <= s <= 1/5, since the other derivative terms are nonpositive.
    derivative_upper = -11 + Q(6, 5) + Q(168, 125)
    assert derivative_upper == -Q(1057, 125)

    e = Interval(lo, hi)
    p, q, L, U = 1-e, 1+e, 2-e, 2+e
    x = p * (1-2*e**2) / (2*(1+e+e**2))
    y = e * (1-2*e**2) / (1-4*e)
    d = e**2/x + q**2/y
    quantities = {'e': e, 'p': p, 'q': q, 'L': L, 'U': U,
                  'x': x, 'y': y, 'L-x': L-x, 'L-y': L-y,
                  'd': d, 'd-L': d-L, 'U-d': U-d}
    for name in ['p', 'q', 'L', 'U', 'x', 'y', 'L-x', 'L-y', 'd-L', 'U-d']:
        assert quantities[name].lo > 0, name

    # Exact coefficient check of (L-x)(L-y)-q^2 = P(e)/denominator.
    # Numerator is 2P; denominator is 2(1+e+e^2)(1-4e).
    numerator = polynomial_subtract(
        polynomial_product([3, 3, 4, -4], [2, -10, 4, 2]),
        polynomial_product(polynomial_product([2, 2, 2], [1, -4]), [1, 2, 1]))
    assert numerator == [4, -22, 6, -4, 84, 0, -8]

    # Exact coefficient checks of off-diagonal and diagonal identities.
    # ep/x+eq/y = p follows after multiplying by (1-2e^2).
    # Check the simpler displayed identity:
    # 2e(1+e+e^2) + (1+e)(1-4e) = (1-e)(1-2e^2).
    assert polynomial_subtract(
        polynomial_subtract([0, 2, 2, 2],
                            [-v for v in polynomial_product([1, 1], [1, -4])]),
        polynomial_product([1, -1], [1, 0, -2])) == [0, 0, 0, 0]
    # p^2/x+e^2/y = U:
    # 2(1-e)(1+e+e^2)+e(1-4e) = (2+e)(1-2e^2).
    assert polynomial_subtract(
        polynomial_subtract(polynomial_product([2, -2], [1, 1, 1]), [0, -1, 4]),
        polynomial_product([2, 1], [1, 0, -2])) == [0, 0, 0, 0]

    result = {
        'status': 'All assertions passed using exact rational arithmetic.',
        'polynomial_ascending_coefficients': [2, -11, 3, -2, 42, 0, -4],
        'root_interval': [str(lo), str(hi)],
        'P_root_lower_sign': 1,
        'P_root_upper_sign': -1,
        'derivative_upper_on_zero_to_one_fifth': str(derivative_upper),
        'outward_decimal_enclosures': {k: v.decimal_enclosure() for k, v in quantities.items()},
    }
    output = Path(__file__).with_name('cp3-algebraic-certificate.json')
    output.write_text(json.dumps(result, indent=2) + '\n')
    print(json.dumps(result, indent=2))


if __name__ == '__main__':
    main()
