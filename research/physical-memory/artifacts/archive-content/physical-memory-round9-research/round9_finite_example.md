# Explicit finite 3-state realization of the rectangular-window target

Date: 2026 09 29. This is a finite construction, not a limiting Erlang realization.

Let the four prescribed-temperature boundary ports be b0,b1,b2,b3, with fixed static path conductances 1, 1/2, 1/10. Observe the sum of cross statistics on these three edges with kernel w(t)=1_[9/10,11/10](t).

## Unscaled network

Use three internal states x1,x2,x3 with capacities

    C_x1 = C_x2 = 55/9,       C_x3 = 2.

The only conductors are:

| Endpoints | Conductance |
|---|---:|
| b0 -- x1 | 11 |
| x1 -- x2 | 11/9 |
| x2 -- b1 | 11 |
| b1 -- x3 | 1 |
| x3 -- b2 | 1 |
| b2 -- b3 | 1/10 |

The first three conductors are in series, so their static conductance is

    [1/11 + 9/11 + 1/11]^-1 = 1.

The next two give static conductance 1/2. The last edge is direct. Thus the exact required static matrix K is realized.

The strong-edge normalized internal matrix is

    Q = [[2,-1/5],[-1/5,2]],

with rates a=9/5 and b=11/5. Its normalized cross density is HypoExp(a,b). The medium-edge one-state star has rate 1. Define

    q(rho) = exp(-9rho/10) - exp(-11rho/10).

Then the exact total statistic is

    S = [b q(a) - a q(b)]/(b-a) + q(1)/2
      = 0.14474703843945091659785910408661817...,

strictly larger than 7/50=0.14. The strong edge contributes 0.1078977504181911373... .

The accompanying standard-library script evaluates the numbers with 70-digit Decimal arithmetic and separately proves S > 0.14 using exact Fraction arithmetic. Even and odd Taylor sums of exp(-x) at orders 60 and 61 give rigorous upper and lower bounds. In particular it certifies

    S > 1447470384394509 / 10000000000000000 > 7/50.

## Exact target by finite positive scaling

Set theta=(7/50)/S, an exactly defined real number, approximately 0.967204590224230055. Multiply every capacity and every conductor incident on an internal state by theta. Do not scale the third direct edge. Add direct boundary conductors:

    b0 -- b1: 1-theta,
    b1 -- b2: (1-theta)/2.

Since 0<theta<1, every coefficient remains positive. Scaling internal capacities and conductances together leaves Q unchanged, and scales the dynamic static conductance and transient response by theta. The new direct conductors supply precisely the unused static budgets and have zero transient statistic. Therefore the scaled finite network still has the exact original K and exactly

    S_scaled = theta S = 7/50.

It uses exactly three internal states; no limiting conductance or capacity is required.

## A short rigorous certificate that two states cannot suffice

For the rectangular kernel, the exponential benchmark satisfies

    q_* = sup_rho integral_(9/10)^(11/10) rho exp(-rho t) dt
        <= (1/5) / [(9/10)e] = 2/(9e),

because rho exp(-rho t) <= 1/(et). With at most two states, the universal coefficient envelope allows at most

    max(1+1/2, C_2) q_* = (3/2)q_*,

where C_2=4/e<3/2. The last strict inequality follows from e>8/3. Consequently

    S_(at most 2 states) <= 1/(3e) < 1/8 < 7/50.

This gives a fully analytic impossibility certificate with no optimized-rate decimal comparison. Combined with the finite construction above, the minimum state count for the scalar target 0.14 is exactly 3.

The sharper dynamic-program value for two states is 0.11054848082888258..., but it is unnecessary for this integer certificate.
