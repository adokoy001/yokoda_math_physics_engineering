"""Numerical cp-rank lower-bound comparisons; no floating-point output is a proof.

Fawzi--Parrilo (2014), arXiv:1404.3240v1, section 4, equation (51).
Optional conservative robust entry-box relaxation is derived in accompanying notes.
Requires Python, numpy, cvxpy and Clarabel/SCS. Tested cvxpy 1.9.3.
"""
from pathlib import Path
import sys, json, math, time
HERE=Path(__file__).resolve().parent
try:
    import cvxpy as cp
except ModuleNotFoundError:
    sys.path.insert(0,str(HERE/'sdp_dependencies'))
    import cvxpy as cp
import numpy as np

F0=np.array([[1,1,0,0],[0,1,1,0],[0,0,1,1],[1,0,0,1]],float)
H0=F0.T@F0
n=4; nn=n*n

def minor_constraints(X):
    # Only i<k and j<l, exactly as in equation (51); no extra X>=0 constraint.
    return [X[i+n*j,k+n*l]==X[i+n*l,k+n*j]
            for i in range(n) for k in range(i+1,n)
            for j in range(n) for l in range(j+1,n)]

def solve_problem(problem, solver):
    started=time.time()
    if solver=='CLARABEL':
        value=problem.solve(solver=solver,tol_gap_abs=1e-9,tol_gap_rel=1e-9,
                            tol_feas=1e-9,max_iter=300)
    else:
        value=problem.solve(solver=solver,eps=2e-7,max_iters=200000)
    info=dict(value=float(value),status=problem.status,solver=solver,
              elapsed_seconds=time.time()-started,
              num_iters=problem.solver_stats.num_iters)
    extra=problem.solver_stats.extra_stats
    if isinstance(extra,dict) and 'info' in extra:
        info['solver_info']={k:float(extra['info'][k]) for k in
                             ['pobj','dobj','res_pri','res_dual','gap'] if k in extra['info']}
    return info

def tau_exact(A,solver='CLARABEL'):
    ev,U=np.linalg.eigh(A)
    assert ev.min()>-1e-9
    keep=ev>1e-9
    W=np.kron(U[:,keep],U[:,keep])
    # Facial reduction removes only the exact nullspace of A tensor A.
    Y=cp.Variable((W.shape[1],W.shape[1]),symmetric=True)
    X=W@Y@W.T
    t=cp.Variable()
    a=A.reshape(nn,1,order='F')
    ar=W.T@a
    upper=np.diag(np.kron(ev[keep],ev[keep]))
    block=cp.bmat([[cp.reshape(t,(1,1),order='F'),ar.T],[ar,Y]])
    equalities=minor_constraints(X)
    constraints=[block>>0,cp.diag(X)<=a.ravel()**2,upper-Y>>0]+equalities
    prob=cp.Problem(cp.Minimize(t),constraints)
    result=solve_problem(prob,solver)
    xv=np.asarray(X.value)
    result.update(rank=int(keep.sum()),matrix=A.tolist(),
                  primal_min_eigenvalue=float(np.linalg.eigvalsh(block.value).min()),
                  upper_slack_min_eigenvalue=float(np.linalg.eigvalsh(upper-Y.value).min()),
                  maximum_diagonal_violation=float(max(0,np.max(np.diag(xv)-a.ravel()**2))),
                  maximum_equality_residual=float(max(abs(eq.expr.value) for eq in equalities)),
                  X=xv.tolist())
    return result

def tau_robust_box(center,eps,solver='CLARABEL'):
    """Lower bound for inf{tau_sos(A): A CP, |A-center|<=eps}.

    Relaxations, all conservative for any PSD A in the box:
      diag(X)<= (center_ij+eps)*A_ij (instead of A_ij**2);
      X <= center tensor A + A tensor center - center tensor center
           + n*n*eps*eps*I (instead of A tensor A).
    The second follows since E tensor E <= ||E||op**2 I <= n*n*eps*eps I.
    Thus this is NOT an exact minimization of the pointwise Fawzi-Parrilo bound.
    """
    A=cp.Variable((n,n),symmetric=True)
    X=cp.Variable((nn,nn),symmetric=True)
    t=cp.Variable()
    a=cp.reshape(A,(nn,1),order='F')
    upper_entries=(center+eps).ravel(order='F')
    kron_upper=cp.kron(center,A)+cp.kron(A,center)-np.kron(center,center)+(n*eps)**2*np.eye(nn)
    block=cp.bmat([[cp.reshape(t,(1,1),order='F'),a.T],[a,X]])
    equalities=minor_constraints(X)
    constraints=[A>>0,A>=0,A>=center-eps,A<=center+eps,
                 block>>0,cp.diag(X)<=cp.multiply(upper_entries,cp.reshape(a,(nn,),order='F')),
                 kron_upper-X>>0]+equalities
    prob=cp.Problem(cp.Minimize(t),constraints)
    result=solve_problem(prob,solver)
    result.update(epsilon=eps,relaxation='conservative_affine_entry_box_envelope',
                  matrix_at_relaxed_optimum=A.value.tolist(),X=X.value.tolist(),
                  primal_min_eigenvalue=float(np.linalg.eigvalsh(block.value).min()),
                  upper_slack_min_eigenvalue=float(np.linalg.eigvalsh(kron_upper.value-X.value).min()),
                  maximum_equality_residual=float(max(abs(eq.expr.value) for eq in equalities)))
    return result

results=dict(source='https://arxiv.org/html/1404.3240v1#S4',equation='51',
             cvxpy_version=cp.__version__,solvers=cp.installed_solvers(),
             pointwise=[],robust_boxes=[],cross_checks=[],
             caveats=['All solver values are numerical, not certified proofs.',
                      'A pointwise bound does not certify an entire entrywise noise box.',
                      'Robust-box results use our conservative affine envelope of Eq.51, not exact FP box optimization.',
                      'For epsilon>0 the circulant epsilon family has ordinary rank four, so its cp-rank lower bound is already four.',
                      'No claim of optimality is made for saved nonconvex factor fits.'])
def save():
    (HERE/'round3_sdp_results.json').write_text(json.dumps(results,indent=2))

rho_grid=[0,.02,.05,.10,.15,.16,.20,.25,.30,.31,.35,.45,.49,.50,.75,1.]
for rho in rho_grid:
    res=tau_exact(H0+rho*np.ones((4,4)))
    res.update(family='H0+rho*J',rho=rho,
               cheap_m2_minus_4zd=(1+rho)**2-4*rho*(2+rho),
               improved_m2_minus_4z_dminusz=(1+rho)**2-8*rho)
    results['pointwise'].append(res);save()
    print(json.dumps({k:res[k] for k in ['family','rho','value','status','cheap_m2_minus_4zd']}),flush=True)

for eps in [.01,.05,.10,.19]:
    A=H0.copy()
    for i in range(4):
        for j in range(4): A[i,j]+= eps if i==j or (i-j)%4==2 else -eps
    res=tau_exact(A)
    res.update(family='circulant_epsilon',epsilon=eps,
               cheap_m2_minus_4zd=(1-eps)**2-4*eps*(2+eps),
               improved_m2_minus_4z_dminusz=(1-eps)**2-8*eps)
    results['pointwise'].append(res);save()
    print(json.dumps({k:res[k] for k in ['family','epsilon','rank','value','status']}),flush=True)

for eps in [.01,.025,.049038105676658,.075,.097167540709727,.10,.125,.15,.19]:
    res=tau_robust_box(H0,eps)
    res['cheap_m2_minus_4zd']=(1-eps)**2-4*eps*(2+eps)
    res['improved_m2_minus_4z_dminusz']=(1-eps)**2-8*eps
    results['robust_boxes'].append(res);save()
    print(json.dumps({k:res[k] for k in ['epsilon','value','status','cheap_m2_minus_4zd']}),flush=True)

# Cross solver checks resolve numerical doubts only, not strict certificates.
for rho in [0,.20,.49]:
    res=tau_exact(H0+rho*np.ones((4,4)),solver='SCS')
    res.update(family='H0+rho*J',rho=rho)
    results['cross_checks'].append(res);save()
    print(json.dumps({k:res[k] for k in ['family','rho','solver','value','status']}),flush=True)

finite_results=HERE/'finite-window-results.json'
if finite_results.exists():
    saved=json.loads(finite_results.read_text())['target']
    G=np.array(saved['local_search_best_factor'])
    # Round downward/upward neither matters: direct reconstruction gives a feasible CP3 matrix.
    # Use eight decimals and report its directly evaluated entrywise error as a numerical upper bound.
    Gr=np.round(G,8)
    results['explicit_cp3_upper_comparator']=dict(
        factor=Gr.tolist(),matrix=(Gr.T@Gr).tolist(),
        entrywise_error=float(np.max(abs(Gr.T@Gr-H0))),
        provenance='Existing 40-start local fit; no new nonconvex search.',
        is_global_optimum=False)
    # These finite decimals give an exact rational factor, hence a certified
    # feasible upper comparator independent of the nonconvex optimizer.
    from fractions import Fraction
    Gf=[[Fraction(str(round(x,8))) for x in row] for row in Gr.tolist()]
    GG=[[sum(Gf[k][i]*Gf[k][j] for k in range(3)) for j in range(4)] for i in range(4)]
    err=max(abs(GG[i][j]-int(H0[i,j])) for i in range(4) for j in range(4))
    results['explicit_cp3_upper_comparator'].update(
        entrywise_error_exact_rational=str(err),
        entrywise_error_exact_decimal=float(err),
        strict_upper_bound='0.19667648')
    assert err < Fraction('0.19667648')
results['analytic_thresholds']={
    'old_pointwise_rho':-1+2/math.sqrt(3),
    'improved_pointwise_rho':3-2*math.sqrt(2),
    'improved_uniform_box_epsilon':5-2*math.sqrt(6),
    'proved_SDP_lower_bound_crossing_rho':(math.sqrt(5)-1)/4,
    'proved_SDP_lower_bound_formula':'max(3,(4+4*rho+2*rho**2)/(1+2*rho+2*rho**2))',
    'equality_to_SDP_optimum_proven':False}
save()
