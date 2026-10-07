# A sharp universal kernel bound for reversible positive dynamics

Date: 2026 09 29. Analytic derivation built on an explicitly identified classical theorem. The mathematical statement below is proved; academic novelty remains unestablished.

## Main theorem

Let Q be a k by k symmetric positive definite Stieltjes matrix (its off-diagonal entries are nonpositive), and let u,v be nonnegative vectors with a = u^T Q^{-1}v > 0. Define the normalized transient density

    f(t) = u^T exp(-Qt) v / a,    t >= 0.

For k >= 1 put

    C_k = k^k exp(-(k-1)) / (k-1)!.

Then there is a probability measure nu on positive rates such that the POINTWISE bound

    f(t) <= C_k integral mu exp(-mu t) nu(dmu)

holds for every t >= 0. Consequently, for EVERY nonnegative measurable measurement kernel w,

    integral w(t) f(t) dt <= C_k q_*(w),
    q_*(w) = sup_{mu > 0} integral w(t) mu exp(-mu t) dt.

This is useful when q_* is finite; if it is infinite the extended-valued inequality is trivial. No compact support, triangular shape, waiting-time restriction, smoothness, or condition 3 q_* >= sup w is required.

The constant C_k is the smallest constant valid uniformly over this entire k-state class and all nonnegative kernels. Sharpness is a supremum approached by physical two-terminal thermal/grounded-capacitor RC networks, not in general an attained equality at one nondegenerate network and a bounded-width kernel.

Its properties are

    C_1 = 1, C_2 = 4/e, C_3 = 27/(2e^2),
    C_k ~ e sqrt(k/(2 pi)),
    1 <= C_k <= k.

Thus the universal enhancement over the best one-state response grows only as the square root of the number of internal states. This describes a single normalized cross transient and its measurement. It is not a statement that an entire k-state system can be replaced by one state.

## Proof, step 1: turn the cross transient into a reversible absorption law

First suppose Q is irreducible. Since v is nonzero, h = Q^{-1}v is strictly positive. Let H = diag(h) and

    T = -H^{-1} Q H,
    alpha_i = u_i h_i / a,
    beta = H^{-1}v.

T has nonnegative off-diagonal entries, T 1 = -beta <= 0, and alpha is a probability vector. The missing row mass defines transitions to an absorbing state. The absorption-time density is exactly

    alpha^T exp(Tt) beta = f(t).

Moreover, the transient generator T is reversible with respect to pi_i proportional to h_i^2, since pi_i T_ij is proportional to -h_i h_j Q_ij. Its eigenvalues are the negatives of the eigenvalues of Q. Positive definiteness guarantees eventual absorption.

We now invoke an established result, not a discovery of this project:

Laurent Miclo, "On absorption times and Dirichlet eigenvalues", ESAIM: Probability and Statistics 14 (2010), 117-150, DOI 10.1051/ps:2008037, Theorem 1.2, printed p.120 (PDF p.3), assumptions (B1), (B2) on printed p.119. It states that an irreducible reversible finite-state absorption law with k transient states is a convex mixture of sums of at most k independent exponential variables. Their rates are successive Dirichlet eigenvalues.

Open access full text:
https://www.numdam.org/item/10.1051/ps:2008037.pdf

Source inspected directly, including the theorem and assumptions. The theorem has a typographical theta in the distribution notation; the surrounding definition uses lambda, the continuous-time rates. We use the defined continuous-time statement, not the typo.

If Q is reducible, permute it to block diagonal form. Blocks with positive a_l = u_l^T Q_l^{-1}v_l contribute normalized densities with mixture weights a_l/a. Blocks with a_l = 0 contribute identically zero. Apply the irreducible argument to each contributing block. In every case f is a convex mixture of hypoexponential densities involving at most k exponential summands.

This is the only non-elementary imported theorem in this proof. Merely knowing that the eigenvalues are real does not give the same k-stage representation in arbitrary nonreversible systems: Miclo discusses why additional stages may be required there.

## Proof, step 2: every hypoexponential is a scale mixture of Erlang laws

Let X = sum_{i=1}^j E_i/lambda_i, with the E_i independent Exp(1). Set R = sum E_i and P_i = E_i/R. The elementary gamma-Dirichlet change of variables gives

    R ~ Gamma(j, rate 1),
    P ~ Dirichlet(1,...,1),
    R independent of P.

Indeed, the joint density of (R,P) is exp(-R) R^{j-1} on the simplex, which factors into the Gamma density and uniform simplex density.

Conditionally on P,

    X = R A(P),    A(P) = sum P_i/lambda_i,

is Gamma(j, rate rho), where rho = 1/A(P). Thus the hypoexponential density is a probability mixture of Erlang densities of one fixed integer shape j, with varying rates rho. Equal or repeated lambda_i pose no problem.

## Proof, step 3: the optimal Erlang exponential envelope

Write g_mu(t) = mu exp(-mu t), and

    p_{j,rho}(t) = rho^j t^{j-1} exp(-rho t)/(j-1)!.

For j > 1,

    p_{j,rho}(t) / g_{rho/j}(t)
      = j (rho t)^{j-1} exp(-(1-1/j)rho t)/(j-1)!.

Its maximum occurs at rho t = j and equals C_j. For j=1 the bound is equality. Hence

    p_{j,rho}(t) <= C_j g_{rho/j}(t).

The ratio C_{j+1}/C_j = (1+1/j)^{j+1}/e is greater than 1, so C_j <= C_k for j <= k. Mixing the envelopes from step 2 and then step 1 proves the stated pointwise exponential-mixture envelope. More precisely, one first obtains an envelope of total mass sum p_j C_j <= C_k. Adding any missing mass at an arbitrary positive rate yields a probability measure nu after division by C_k.

Integrating against nonnegative w proves the kernel inequality by Tonelli's theorem.

Also,

    (C_{j+1}/(j+1)) / (C_j/j) = (1+1/j)^j/e < 1,

so C_k/k <= C_1 = 1. The displayed asymptotic follows from Stirling's formula.

## Proof, step 4: sharpness within symmetric Stieltjes systems

Let A be the adjacency matrix of the path on k vertices and, for 0 < epsilon < 1/2, take

    Q_epsilon = I - epsilon A,    u=e_1, v=e_k.

Q_epsilon is irreducible, symmetric, Stieltjes and positive definite. Its normalized endpoint density is

    f_epsilon(t) = (exp(-Q_epsilon t))_{1k} / (Q_epsilon^{-1})_{1k}.

The path has a unique walk of minimum length k-1 from 1 to k. Consequently the matrix-exponential and inverse power series give, uniformly on compact time intervals,

    epsilon^{-(k-1)} (exp(-Q_epsilon t))_{1k}
       -> exp(-t) t^{k-1}/(k-1)!,
    epsilon^{-(k-1)} (Q_epsilon^{-1})_{1k} -> 1.

Thus f_epsilon tends to the Erlang(k,1) density. Take nonnegative rectangle kernels supported in [k-delta,k+delta], with delta positive and tending to zero. Dividing both integrals by 2 delta,

    q_*(w_delta)/(2 delta) -> 1/(e k),

because the maximum of mu exp(-mu k) is 1/(e k). This limit also follows directly by bounding the average exponential density above by 1/[e(k-delta)] and evaluating the candidate rate 1/k for a lower bound.

Therefore, first sending epsilon to zero and then delta to zero,

    integral w_delta f_epsilon / q_*(w_delta)
       -> e k * exp(-k) k^{k-1}/(k-1)! = C_k.

No smaller universal constant is possible. Smooth nonnegative kernels of shrinking support give the same sharpness, if smoothness is desired.

## Physical realization and fixed static conductance

The sharpness construction is compatible with the physical model, without an unmodeled heat sink or negative conductance.

For any irreducible Q and nonzero u,v >= 0, set z=Q^{-1}(u+v)>0. Choose internal capacities and conductances

    C_i = z_i^2,
    g_ij = -Q_ij z_i z_j  (i != j),
    g_{iL} = z_i u_i,
    g_{iR} = z_i v_i.

The identity Qz=u+v shows that the physical internal Laplacian is

    L_II = diag(z) Q diag(z),

and its normalized two boundary coupling vectors are u and v. Every capacity is positive and every conductance is nonnegative. The exact two-terminal static conductance is a=u^T Q^{-1}v.

To make this conductance equal to any prescribed kappa>0, multiply all capacities and conductances by kappa/a. This keeps Q and the normalized density f unchanged. This family may require diverging or vanishing element values as epsilon tends to zero; sharpness is for the present unconstrained-positive-element model. Lower bounds on element sizes or bounded total material budgets would be additional hypotheses and may improve the constant.

## Consequences for the existing state-complexity theorem

### Exact variational reduction for a fixed kernel

Define, for a nonnegative measurable kernel w,

    E_k(w) = max_{1 <= j <= k} sup_{rho > 0}
               integral w(t) p_{j,rho}(t) dt.

The proof actually gives a stronger fixed-kernel statement:

    sup_{normalized reversible positive components with <= k states}
       integral w(t) f(t) dt = E_k(w).

The upper bound follows because the normalized density is a probability mixture of Erlang densities with shape at most k. The lower bound follows by the symmetric-path limit for each j and rho: replace Q_epsilon by rho(I-epsilon A_path,j). Pointwise convergence and Fatou's lemma give liminf integral w f_epsilon >= integral w p_{j,rho}. Taking the supremum over j and rho proves equality, including infinite values. Thus no continuity or compact-support hypothesis on a nonnegative w is needed.

This replaces optimization over all admissible internal topologies and parameters by at most k one-dimensional optimizations over a rate. It is an equality of SUPREMA. For j>1 an Erlang optimum can lie only in the closure of the reversible physical class, and an exact finite network need not attain it. The universal coefficient above follows from E_k(w) <= C_k q_*(w).

For bounded signed kernels the same variational equality also holds: the mixture upper bound remains valid, and the path densities converge in L1 by Scheffe's lemma, so bounded-kernel expectations converge. The multiplicative C_k q_* inequality, however, was proved only for nonnegative kernels and must not be extended to arbitrary signed kernels.

### Uniform triangle-free static budget corollary

The old round-8 bound D <= k a q_* now holds for every nonnegative kernel, because C_k <= k. Therefore the exact scalar state-count result for uniform triangle-free static budgets no longer requires 3 q_* >= sup w. Assume the best one-state rate is attained, q_*>0, there are m static edges of equal conductance kappa, and S_target lies in [0,m kappa q_*]. Then

    r_min = ceil((S_target-error)_+/(kappa q_*)).

The lower bound applies to arbitrary reversible physical networks in the model. One optimal-rate one-state star per selected edge attains it, with a partial final edge and direct conductors completing the static budgets. If the supremum q_* is not attained, exact endpoint attainment needs separate handling; strict inequalities and approximation-to-supremum remain valid.

For a single two-terminal component, the stronger consequence is

    D/(a q_*) <= C_k,

which inverts to a state lower bound k >= min{j: C_j >= D/(a q_*)}. The asymptotic interpretation is quadratic state cost for large normalized temporal concentration. The exact inverse C_j, rather than its asymptotic, should be used for a finite numerical certificate.

## Novelty caution

Miclo's reversible absorption decomposition, the gamma-Dirichlet change of variables, Erlang exponential envelopes, Stirling's asymptotic and simple path limits are established ingredients. Their combination yields the sharp universal envelope and kernel theorem stated here. We have not yet established whether this exact combination, sharp constant, or its two-terminal physical interpretation is already published. Do not present it as a new named law or claim priority without a separate literature audit.
