"""Reproduce finite numerical checks in thermal-memory research note.
Python 3 + NumPy + SciPy. Numerical checks do not establish minimality.
"""
import json
import math
from pathlib import Path
from fractions import Fraction
import numpy as np
from scipy.linalg import expm

SEED = 20260920
rng = np.random.default_rng(SEED)

def laplacian(weights):
    return np.diag(weights.sum(axis=1)) - weights

def build(F, lam, K, cb):
    # F has one nonnegative row per hidden heat-capacity node.
    H = F.T @ F
    z = F.sum(axis=1)
    assert np.all(z > 0)
    caps = z*z
    W = F / z[:, None]
    links = lam * caps[:, None] * W
    direct = K - lam*(np.diag(H.sum(axis=1))-H)
    Lbb = direct + np.diag(links.sum(axis=0))
    Lbi = -links.T
    Lii = np.diag(lam*caps)
    return Lbb, Lbi, Lii, caps, direct

def response(s, parts, cb):
    Lbb,Lbi,Lii,caps,_ = parts
    return Lbb+s*np.diag(cb)-Lbi@np.linalg.solve(Lii+s*np.diag(caps),Lbi.T)

def exact_rank(mat):
    a = [[Fraction(int(v)) for v in row] for row in mat]
    row = 0
    for col in range(len(a[0])):
        pivot = next((i for i in range(row,len(a)) if a[i][col]),None)
        if pivot is None: continue
        a[row],a[pivot]=a[pivot],a[row]
        v=a[row][col]; a[row]=[x/v for x in a[row]]
        for i in range(len(a)):
            if i != row:
                v=a[i][col]; a[i]=[x-v*y for x,y in zip(a[i],a[row])]
        row+=1
    return row

worst_response=worst_moment=worst_rowsum=0.
checks=0
ss = np.r_[np.logspace(-4,3,21), 1j*np.logspace(-4,3,21)]
for case in range(120):
    n=int(rng.integers(2,9)); r=int(rng.integers(1,9))
    F=rng.uniform(.1,2,(r,n))
    F[rng.random((r,n))<.3]=0
    for row in F:
        if row.sum()==0: row[int(rng.integers(n))]=1.
    H=F.T@F; lam=float(rng.uniform(.1,2))
    a=rng.uniform(.1,1,(n,n)); a=(a+a.T)/2
    weights=lam*H+a; np.fill_diagonal(weights,0)
    K=laplacian(weights); cb=rng.uniform(.1,2,n)
    parts=build(F,lam,K,cb)
    Lbb,Lbi,Lii,caps,direct=parts
    W=-np.linalg.solve(Lii,Lbi.T)
    moment=W.T@np.diag(caps)@W
    worst_moment=max(worst_moment,np.linalg.norm(moment-H)/max(1,np.linalg.norm(H)))
    L=np.block([[Lbb,Lbi],[Lbi.T,Lii]])
    worst_rowsum=max(worst_rowsum,np.max(np.abs(L.sum(axis=1))))
    off=L.copy(); np.fill_diagonal(off,0)
    assert off.max()<1e-10
    assert np.linalg.eigvalsh(L)[0]>-1e-10
    for s in ss:
        target=K+s*np.diag(cb)+s*lam/(s+lam)*H
        error=np.linalg.norm(response(s,parts,cb)-target)/max(1,np.linalg.norm(target))
        worst_response=max(worst_response,float(error)); checks+=1

F0=np.array([[1,1,0,0],[0,1,1,0],[0,0,1,1],[1,0,0,1]],float)
H0=F0.T@F0
K=laplacian(np.ones((4,4))-np.eye(4)); cb=np.ones(4); lam=.25
parts=build(F0,lam,K,cb)
# Exact algebraic rank and positive 4-factor identity.
assert exact_rank(H0.astype(int))==3
Q=np.array([[.5,-math.sqrt(3/8),math.sqrt(3/8)],
            [math.sqrt(3/8),-.25,-.75],
            [math.sqrt(3/8),.75,.25]])
worst_factor=0.
for rho in [0,.01,.05,.25,.49,.5,.75,1,2,10]:
    H=H0+rho*np.ones((4,4))
    alpha=(math.sqrt(1+rho)-1)/2
    F4=F0+alpha*np.ones((4,4))
    worst_factor=max(worst_factor,float(np.max(np.abs(F4.T@F4-H))))
    V=np.array([[math.sqrt(1+rho)]*4,[1,0,-1,0],[0,1,0,-1]],float)
    assert np.max(np.abs(V.T@V-H))<1e-12
    if rho>=.5:
        F3=Q@V
        assert F3.min()>-1e-12
        worst_factor=max(worst_factor,float(np.max(np.abs(F3.T@F3-H))))

# A signed 3-mode realization has precisely the same full transfer.
vals,vecs=np.linalg.eigh(H0); keep=vals>1e-10
G=np.sqrt(vals[keep])[:,None]*vecs[:,keep].T
assert G.shape==(3,4)
algebraic_error=0.
for s in ss:
    reduced=K+lam*H0+s*np.diag(cb)-lam**2/(s+lam)*(G.T@G)
    algebraic_error=max(algebraic_error,float(np.max(np.abs(reduced-response(s,parts,cb)))))

# Dynamic numerical check with a smooth boundary temperature pulse.
from scipy.integrate import solve_ivp
def u(t): return np.array([t*t*np.exp(-t),0.,0.,0.])
def du(t): return np.array([(2*t-t*t)*np.exp(-t),0.,0.,0.])
Lbb,Lbi,Lii,caps,_=parts
times=np.linspace(0,20,401)
physical=solve_ivp(lambda t,z:(-Lii@z-Lbi.T@u(t))/caps,[0,20],np.zeros(4),t_eval=times,rtol=1e-10,atol=1e-12)
abstract=solve_ivp(lambda t,z:-lam*z+lam*G@u(t),[0,20],np.zeros(3),t_eval=times,rtol=1e-10,atol=1e-12)
q4=np.array([Lbb@u(t)+Lbi@z+du(t) for t,z in zip(times,physical.y.T)])
q3=np.array([(K+lam*H0)@u(t)-lam*G.T@z+du(t) for t,z in zip(times,abstract.y.T)])

results=dict(seed=SEED,random_networks=120,frequency_checks=checks,
             max_relative_transfer_error=worst_response,max_relative_moment_error=worst_moment,
             max_laplacian_rowsum_residual=worst_rowsum,
             base_eigenvalues=np.linalg.eigvalsh(H0).tolist(),base_exact_rank=3,
             factor_identity_max_absolute_error=worst_factor,
             algebraic3_physical4_max_transfer_difference=algebraic_error,
             pulse_max_absolute_difference=float(np.max(np.abs(q3-q4))),
             approximate_moment_lower_bound=(3*math.sqrt(3)-5)/4)
assert worst_response<1e-10 and worst_moment<1e-10
assert np.max(np.abs(q3-q4))<1e-8
here=Path(__file__).resolve().parent
(here/'verification-results.json').write_text(json.dumps(results,indent=2))
np.savez(here/'pulse-data.npz',times=times,q3=q3,q4=q4)
print(json.dumps(results,indent=2))
