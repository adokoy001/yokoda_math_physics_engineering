"""Independent finite-window thermal response checks.

Numerical checks are not proofs of cp-rank lower bounds or global optimality.
Python 3 + NumPy + SciPy. Run from any working directory.
"""
from pathlib import Path
from itertools import permutations
import json
import math
import numpy as np
from scipy.special import beta as beta_function
from scipy.linalg import expm
from scipy.optimize import minimize
from numpy.polynomial.legendre import leggauss

SEED = 20260920 + 713
rng = np.random.default_rng(SEED)
gx, gw = leggauss(40)

def quad_nodes(a, b):
    return (a + b)/2 + (b-a)*gx/2, (b-a)*gw/2

def fun_matrix(evals, evecs, values):
    return (evecs * values) @ evecs.T

def step_response(time, ev, U, B, K):
    return K + B.T @ fun_matrix(ev,U,np.exp(-time*ev)/ev) @ B

def physical_graph(r, n=4):
    weights = rng.uniform(.05,1.2,(r,r))
    weights = (weights+weights.T)/2
    weights[rng.random((r,r)) < .25] = 0
    weights = np.minimum(weights,weights.T)
    np.fill_diagonal(weights,0)
    # Include positive boundary connections and grounding; this makes Q SPD.
    B = rng.uniform(0,1.2,(r,n))
    B[rng.random((r,n))<.25] = 0
    internal_ground = rng.uniform(.05,.6,r)
    Q = np.diag(weights.sum(axis=1)+B.sum(axis=1)+internal_ground)-weights
    Lbb = np.diag(B.sum(axis=0)+rng.uniform(.05,.6,n))
    K = Lbb-B.T @ np.linalg.solve(Q,B)
    full = np.block([[Lbb,-B.T],[-B,Q]])
    assert np.linalg.eigvalsh(full)[0]>0
    return Q,B,K

def cp_factor_small_dnn(M):
    """Construct a nonnegative <=3-row factor via permuted Cholesky.

    Existence for 3x3 DNN also follows from a normalized correlation argument.
    This function checks a numerical factor rather than inferring cp-rank from rank.
    """
    r=M.shape[0]
    for perm in permutations(range(r)):
        p=np.array(perm)
        L=np.linalg.cholesky(M[np.ix_(p,p)])
        if L.min()>=-2e-12:
            F=np.zeros_like(L)
            F[:,p]=L.T
            return F
    raise AssertionError('No nonnegative permuted Cholesky factor found')

step_error=gram_error=ramp_error=cp_small_error=0.
min_step_factor=1.
min_ramp_internal=1.
min_ramp_eigenvalue=1.
max_constant_cancellation=0.
cases=[]
for r in range(1,9):
    for trial in range(20):
        Q,B,K=physical_graph(r)
        ev,U=np.linalg.eigh(Q)
        t=float(rng.uniform(.2,2)); h=float(rng.uniform(.1,1.4))
        times1,ww=quad_nodes(t,t+h)
        times2,_=quad_nodes(t+h,t+2*h)
        # Independently integrate the complete response, including unknown K.
        numerical=sum(w*(step_response(x,ev,U,B,K)-step_response(y,ev,U,B,K))
                      for w,x,y in zip(ww,times1,times2))
        target=B.T@fun_matrix(ev,U,np.exp(-ev*t)*(-np.expm1(-ev*h))**2/ev**2)@B
        Ah=fun_matrix(ev,U,-np.expm1(-ev*h)/ev)
        F=expm(-Q*t/2)@Ah@B
        step_error=max(step_error,float(np.max(abs(numerical-target))))
        gram_error=max(gram_error,float(np.max(abs(F.T@F-target))))
        min_step_factor=min(min_step_factor,float(F.min()))
        altered_K=K+rng.normal(size=K.shape)
        altered=sum(w*(step_response(x,ev,U,B,altered_K)-step_response(y,ev,U,B,altered_K))
                    for w,x,y in zip(ww,times1,times2))
        max_constant_cancellation=max(max_constant_cancellation,float(np.max(abs(altered-numerical))))

        # Common monotone ramp: derivative is a positive mixture of beta densities.
        duration=float(rng.uniform(.1,1.3))
        s,ws=quad_nodes(0,duration)
        x=s/duration
        aa=rng.integers(1,6,3); bb=rng.integers(1,6,3)
        mix=rng.uniform(.1,1,3); mix/=mix.sum()
        density=sum(weight*x**(a-1)*(1-x)**(b-1)/beta_function(a,b)/duration
                    for weight,a,b in zip(mix,aa,bb))
        ws=ws*density
        assert abs(ws.sum()-1)<1e-12
        start=duration+t
        ts1,wt=quad_nodes(start,start+h)
        ts2,_=quad_nodes(start+h,start+2*h)
        # This integral is independent of the compact spectral formula below.
        ramp_numerical=np.zeros((4,4))
        for timeweight,time1,time2 in zip(wt,ts1,ts2):
            v1=sum(w*step_response(time1-shift,ev,U,B,K) for w,shift in zip(ws,s))
            v2=sum(w*step_response(time2-shift,ev,U,B,K) for w,shift in zip(ws,s))
            ramp_numerical+=timeweight*(v1-v2)
        ramp_scalar=sum(w*np.exp(-ev*(start-shift)) for w,shift in zip(ws,s))
        M=fun_matrix(ev,U,ramp_scalar*(-np.expm1(-ev*h))**2/ev**2)
        ramp_target=B.T@M@B
        ramp_error=max(ramp_error,float(np.max(abs(ramp_target-ramp_numerical))))
        min_ramp_internal=min(min_ramp_internal,float(M.min()))
        min_ramp_eigenvalue=min(min_ramp_eigenvalue,float(np.linalg.eigvalsh(M)[0]))
        if r<=3:
            R=cp_factor_small_dnn(M)
            Framp=R@B
            assert Framp.min()>=-1e-11
            cp_small_error=max(cp_small_error,float(np.max(abs(Framp.T@Framp-ramp_target))))
        cases.append(dict(r=r,trial=trial,post_hold_start=start,ramp_duration=duration,h=h))

# Four-cycle target and a local (not globally certified) three-row approximation search.
F0=np.array([[1,1,0,0],[0,1,1,0],[0,0,1,1],[1,0,0,1]],float)
H0=F0.T@F0
delta=(2*math.sqrt(7)-5)/3  # Improved four-cycle support/Cauchy certificate.
lam=.25; t=1.; h=2.
coefficient=math.exp(-lam*t)*(-math.expm1(-lam*h))**2
Dstar=coefficient*H0
assert np.linalg.matrix_rank(H0)==3
K=4*np.eye(4)-np.ones((4,4))
B=lam*F0; Q=lam*np.eye(4)
ev,U=np.linalg.eigh(Q)
tt1,ww=quad_nodes(t,t+h); tt2,_=quad_nodes(t+h,t+2*h)
window1=sum(w*step_response(time,ev,U,B,K) for time,w in zip(tt1,ww))
window2=sum(w*step_response(time,ev,U,B,K) for time,w in zip(tt2,ww))
assert np.max(abs(window1-window2-Dstar))<1e-12

def constraints(z):
    G=z[:12].reshape(3,4)
    E=(G.T@G-H0).ravel()
    return np.r_[z[12]-E,z[12]+E]

def jac(z):
    G=z[:12].reshape(3,4)
    J=np.zeros((16,12))
    for i in range(4):
        for j in range(4):
            for k in range(3):
                J[4*i+j,4*k+i]+=G[k,j]
                J[4*i+j,4*k+j]+=G[k,i]
    return np.vstack((np.column_stack((-J,np.ones(16))),np.column_stack((J,np.ones(16)))))

best=None; trials=[]
for restart in range(40):
    G=rng.uniform(.01,1.2,(3,4))
    e=float(np.max(abs(G.T@G-H0)))
    z0=np.r_[G.ravel(),e+.1]
    opt=minimize(lambda z:z[12],z0,jac=lambda z:np.r_[np.zeros(12),1.],
                 method='SLSQP',bounds=[(0,None)]*13,
                 constraints=[dict(type='ineq',fun=constraints,jac=jac)],
                 options=dict(maxiter=1500,ftol=1e-12))
    actual=float(np.max(abs(opt.x[:12].reshape(3,4).T@opt.x[:12].reshape(3,4)-H0)))
    trials.append(dict(success=bool(opt.success),objective=float(opt.fun),actual=actual))
    if best is None or actual<best[0]: best=(actual,opt.x[:12].reshape(3,4))
assert best[0]>=delta-1e-9

# Same finite linear ramp for the target. After hold, its only change is a positive scale.
ramp_duration=.8; ramp_start=1.2
ramp_gain=math.expm1(lam*ramp_duration)/(lam*ramp_duration)
ramp_coefficient=math.exp(-lam*ramp_start)*(-math.expm1(-lam*h))**2*ramp_gain

# Controls: removing the post-hold or common-waveform assumptions can break the claim.
# Scalar physical graph Q=2, B=1, K=.5; unit-duration linear ramp.
# During the ramp the output is .5*t + .25*(1-exp(-2*t)).
bad_t=.1; bad_h=.2
bt1,bw=quad_nodes(bad_t,bad_t+bad_h); bt2,_=quad_nodes(bad_t+bad_h,bad_t+2*bad_h)
pre_hold_D=sum(w*(.5*x+.25*(-math.expm1(-2*x))-.5*y-.25*(-math.expm1(-2*y)))
               for w,x,y in zip(bw,bt1,bt2))
assert pre_hold_D<0
# Two distinct positive linear ramps, both completed before measurement.
# A one-hidden-node, two-boundary-node physical graph with Q=1, B=(.3,.3).
durations=np.array([.2,1.]); different_gains=np.expm1(durations)/durations
unequal_D=np.outer(np.array([.3,.3]),np.array([.3,.3]))
unequal_D*=math.exp(-1.2)*(-math.expm1(-.5))**2*different_gains[None,:]
assert np.max(abs(unequal_D-unequal_D.T))>1e-4

results=dict(seed=SEED,random_cases=len(cases),hidden_node_counts=list(range(1,9)),
             max_step_window_integral_error=step_error,
             max_step_nonnegative_gram_error=gram_error,
             minimum_step_factor_entry=min_step_factor,
             max_unknown_constant_cancellation_error=max_constant_cancellation,
             max_common_monotone_ramp_integral_error=ramp_error,
             minimum_ramp_internal_matrix_entry=min_ramp_internal,
             minimum_ramp_internal_eigenvalue=min_ramp_eigenvalue,
             max_ramp_cp_factor_error_for_r_le_3=cp_small_error,
             target=dict(lam=lam,t=t,h=h,coefficient=coefficient,H0=H0.tolist(),
                         window1=window1.tolist(),window2=window2.tolist(),Dstar=Dstar.tolist(),
                         analytical_cp3_entrywise_lower_bound=delta,
                         finite_window_entrywise_lower_bound=coefficient*delta,
                         lower_bound_if_each_window_has_entrywise_error_eta=coefficient*delta/2,
                         local_search_restarts=len(trials),local_search_best_error=best[0],
                         local_search_best_factor=best[1].tolist(),
                         local_search_is_global_certificate=False),
             linear_ramp_target=dict(duration=ramp_duration,start=ramp_start,h=h,
                                     coefficient=ramp_coefficient,
                                     cp3_entrywise_lower_bound=ramp_coefficient*delta),
             assumption_counterexamples=dict(
                 during_linear_ramp_scalar_D=pre_hold_D,
                 unequal_port_ramps_D=unequal_D.tolist(),
                 unequal_port_ramps_asymmetry=float(np.max(abs(unequal_D-unequal_D.T)))),
             scope='Numerical identity checks and local searches only; cp-rank theorem not numerically proved.')
assert max(step_error,gram_error,ramp_error,cp_small_error)<1e-10
here=Path(__file__).resolve().parent
(here/'finite-window-results.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
