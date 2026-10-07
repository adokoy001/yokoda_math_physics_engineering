# Round 9: reversible positive semigroups, prior art and a sharp envelope

Research date: 2026 09 29. This is an intermediate research note, not a novelty claim.

## Proven abstract statement

Let Q be a symmetric positive definite Stieltjes matrix of order k, u,v nonnegative, and a=u^T Q^-1 v>0. Then

f(t)=u^T exp(-Qt)v/a

is a probability density. There exists a probability measure nu on positive rates such that, simultaneously for every t>=0,

f(t) <= C_k integral mu exp(-mu t) nu(dmu),

where C_k=k^k exp(1-k)/(k-1)!. Consequently, for every nonnegative measurable w,

integral w(t) f(t) dt <= C_k sup_{mu>0} integral w(t) mu exp(-mu t) dt.

The right hand side may be infinite. C_1=1, C_2=4/e, C_3=27/(2e^2), and C_k~e sqrt(k/(2pi)). In particular C_k<=k, strictly for k>1. This removes the special measurement-window condition in the earlier component state bound.

## Proof chain and attribution

1. On an irreducible Q block meeting v, h=Q^-1 v is strictly positive. Put H=diag(h), L=-H^-1 Q H, t_exit=H^-1 v, and alpha=u^T H/a. Then L is a transient Markov subgenerator with exit vector -L1=t_exit, alpha1=1, and it is reversible with measure proportional to h_i^2. Its absorption density is exactly f. Reducible Q is handled by the mixture of blocks with positive cross mass; blocks with zero cross mass contribute nothing.

2. Miclo (2010), Theorem 1.2, represents the absorption time of an irreducible reversible k-state transient chain as a convex mixture of convolutions of suffixes of its ordered eigenvalue exponentials. Thus each mixture component is a sum of j<=k independent exponentials. This representation is known, including the exact phase-count bound; do not claim it as new. For real-spectrum but nonreversible chains, the analogous representation can require more than k phases (Miclo explicitly discusses this distinction).

3. If X=sum_{i=1}^j E_i/lambda_i, with iid E_i~Exp(1), write S=sum E_i~Gamma(j,1) and P_i=E_i/S. The Dirichlet proportions P are independent of S. Hence X=A S, where A=sum P_i/lambda_i>0 is independent of S: X is a scale mixture of Erlang(j) densities. This classical gamma-Dirichlet fact is stated and used explicitly in Yu (2009), Theorem 3 proof, pp. 8–9 of the arXiv manuscript.

4. The Erlang density g_{j,lambda}(t)=lambda^j t^(j-1) exp(-lambda t)/(j-1)! satisfies

g_{j,lambda}(t) <= C_j (lambda/j) exp(-lambda t/j).

The ratio is maximized at t=j/lambda. C_j is the optimal exponential rejection-envelope constant. It is classical: Ross (1997), Introduction to Probability Models, sixth edition, Chapter 11 exercise 8, p.615, explicitly gives this same constant as the mean number of exponential-proposal rejection trials. The likely original gamma-sampling antecedent is Fishman (1976), DOI 10.1145/360248.360256; its full text was blocked, so do not cite its precise formula as independently checked.

5. C_{j+1}/C_j=e^-1 (1+1/j)^(j+1)>1, whereas (C_{j+1}/(j+1))/(C_j/j)=e^-1(1+1/j)^j<1. Integrating the Erlang envelope over the scale mixture, then the Miclo mixture, gives the stated common probability envelope with C_k.

## Sharpness

Over mixtures of hypoexponential laws the constant is optimal: take Erlang(k,lambda), and a sequence of narrow nonnegative windows around t0=k/lambda. The denominator tends, after dividing by window width, to sup_mu mu exp(-mu t0)=1/(e t0). The ratio tends to C_k.

Kernel agent/root additionally identified a physical reversible sharpness sequence: Q_eps=I-eps A_path, u=e_1,v=e_k. Its normalized cross density converges to Erlang(k,1), since the shortest path term in the exponential is eps^(k-1) t^(k-1)/(k-1)! and Q_eps^-1(1,k)=eps^(k-1)(1+O(eps^2)). Q_eps is SPD Stieltjes for sufficiently small eps>0. Thus the best universal constant over the reversible class is also C_k, as a supremum. For k>1 this does not assert attainment by a fixed finite reversible network.

## Close prior work inspected

### Miclo (2010)

Laurent Miclo, On absorption times and Dirichlet eigenvalues, ESAIM: Probability and Statistics 14 (2010), 117–150, DOI 10.1051/ps:2008037.

Full primary OA PDF: https://www.numdam.org/item/10.1051/ps:2008037.pdf

Theorem 1.2, printed p.120 / PDF p.4, is exactly the reversible convolution-mixture statement. Proposition 5.4, printed p.138 / PDF p.22, characterizes the closure of reversible absorption laws via these mixtures. Browser retrieval: turn44view0; theorem lines 121–154, closure lines 1030–1048 in turn48view1.

### Yu (2009)

Yaming Yu, Stochastic Ordering of Exponential Family Distributions and Their Mixtures, arXiv:0909.4570v1.

Full author preprint: https://arxiv.org/pdf/0909.4570

Section 3, proof of Theorem 3, PDF p.9, explicitly proves the scale mixture of fixed-shape gamma representation via independence of sum and proportions. Its stated results are stochastic/hazard/likelihood-ratio orders, not our universal nonnegative-observable envelope. Retrieval turn48view0, lines 505–513.

### He–Horvath–Horvath–Telek (2019)

Qi-Ming He, Gabor Horvath, Illes Horvath, Miklos Telek, Moment bounds of PH distributions with infinite or finite support based on the steepest increase property, Advances in Applied Probability 51(1) (2019), 168–183, DOI 10.1017/apr.2019.7.

Full author PDF (successful): https://webspn.hit.bme.hu/~telek/cikkek/he18a.pdf

Author's linking page: https://math.bme.hu/~pollux/publ_hi.html

Alternate author URL returned 502: https://www.engineering.uwaterloo.ca/~q7he/Z_PDF_PS_Published/2019_AAP_PHD_Bounds.pdf

Lemma 1, manuscript pp.3–4: f'(t)/f(t)<=(m-1)/t-lambda for any m-phase PH density, with lambda its generator's slowest decay eigenvalue. Lemma 2: f(t)/Erlang(m,lambda)(t) decreases with t. Corollary 1 gives stochastic domination and moment bounds. Later results address truncated PH distributions and their moments/SCV. This does not itself give the claimed all-nonnegative-observable exponential-mixture envelope: a likelihood-ratio crossing permits some values of f to exceed the comparison density, and nonmonotone observation windows cannot be compared by stochastic order. From steepest increase alone one obtains the weaker pointwise tf(t)<=m, by integrating f(s)>=f(t)(s/t)^(m-1) for s<=t. No assertion that our C_m inequality extends to general nonreversible PH is presently justified.

Browser full body: turn75view0; Lemmas 1–2 lines 90–168; Corollary 1 lines 173–212; moments lines 215–338; remainder truncated-distribution analysis.

### Classical rejection-envelope antecedent

Sheldon M. Ross, Introduction to Probability Models, sixth edition, Academic Press, 1997, Chapter 11 exercise 8 p.615.

Hosted PDF: https://www-elec.inaoep.mx/~rogerio/IntrodProbabModels.pdf

Downloaded locally and text extracted: research_work/ross_models.pdf and research_work/ross_models.txt, lines 25706–25712. Exact C_n formula verified in the exercise. This is a book rather than original research and should be used only to establish that the scalar constant is textbook material. Do not embed or republish the book PDF.

George S. Fishman, Sampling from the Gamma Distribution on a Computer, Communications of the ACM 19(7) (1976), 407–409, DOI 10.1145/360248.360256. Publisher PDF https://dl.acm.org/doi/pdf/10.1145/360248.360256 returned HTTP403. Public abstract describes a rejection algorithm with O(sqrt(alpha)) cost, consistent with this envelope, but exact full-text comparison remains unverified.

## Novelty judgment

The decomposition, gamma scale mixture, and sharp Erlang constant are established tools. The resulting optimal exponential-mixture domination for the whole reversible positive-semigroup class is a short synthesis of known results, with a sharp physical reversible sequence. Focus any novelty claim on that synthesis and its concrete model-order/state-allocation implications, not on its ingredients. The exact whole-class inequality was not located in the searches performed, which is not evidence of absence. The mathematical statement is substantially broader than the earlier special-ramp lemma even if ultimately classified as a useful corollary of existing probability theory.
