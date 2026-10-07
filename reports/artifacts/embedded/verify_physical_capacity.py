"""Reproducible implementation checks, not a substitute for the proof.
Requires Python 3, NumPy. Run from any directory; writes sibling JSON.
"""
from fractions import Fraction
from pathlib import Path
import json
import math
import numpy as np

def add(a,b):
    out=[0]*max(len(a),len(b))
    for i,v in enumerate(a): out[i]+=v
    for i,v in enumerate(b): out[i]+=v
    return out

def cheby_shifted(n):
    a,b=[1],[-1,2]
    if n==0: return a
    for _ in range(1,n):
        twice_x_b=add([-2*v for v in b],[0]+[4*v for v in b])
        a,b=b,add(twice_x_b,[-v for v in a])
    return b

def evaluate(c,x):
    out=0
    for v in reversed(c): out=out*x+v
    return out

exact=[]
for N in range(1,32,2):
    c=cheby_shifted(N)
    assert evaluate(c,Fraction(1,2))==0
    slope=evaluate([i*c[i] for i in range(1,len(c))],Fraction(1,2))
    assert abs(slope)==2*N
    assert sum(abs(x) for x in c)==abs(evaluate(c,-1))
    # Target window I_m*=kappa*2^(-m)*(1+m*log(2))/4.
    const=sum(Fraction(c[m],2**m) for m in range(N+1))
    linear=sum(Fraction(m*c[m],2**m) for m in range(N+1))
    assert const==0 and abs(linear)==N
    exact.append({'N':N,'l1_coefficient_norm':sum(abs(x) for x in c)})

rng=np.random.default_rng(20261006)
a=math.log(2)
worst_identity=0.
max_resource_ratio=0.
cases=0
for rep in range(240):
    n=1+rep%12
    edge=rng.uniform(0,1,(n,n)); edge=np.triu(edge,1); edge+=edge.T
    gl=rng.uniform(.01,2,n); gr=rng.uniform(.01,2,n)
    cap=rng.uniform(.05,3,n)
    L=np.diag(edge.sum(axis=1)+gl+gr)-edge
    Q=L/np.sqrt(cap[:,None]*cap[None,:])
    u=gl/np.sqrt(cap); v=gr/np.sqrt(cap)
    z=np.linalg.solve(Q,u+v); y=np.linalg.solve(Q,u-v)
    B=cap.sum()
    assert np.all(np.abs(y)<=z+1e-10)
    assert abs(z@z-B)<1e-9
    rates,V=np.linalg.eigh(Q)
    residues=(V.T@u)*(V.T@v)
    for N in (1,3,5,7):
        c=np.array(cheby_shifted(N),dtype=float)
        times=a*np.arange(1,N+2)
        windows=(np.exp(-times[:,None]*rates)-np.exp(-(times[:,None]+a)*rates))@(residues/rates)
        direct=float(c@windows)
        x=np.exp(-a*rates)
        # recurrence evaluation of Chebyshev polynomial is better conditioned.
        p=np.polynomial.chebyshev.chebval(2*x-1,[0]*N+[1])
        mult=rates*x*(1-x)*p
        spectral=float((((V.T@z)**2-(V.T@y)**2)*mult).sum()/4)
        err=abs(direct-spectral)/max(1.,B)
        worst_identity=max(worst_identity,err)
        bound=2*B/(math.e**2*a)
        max_resource_ratio=max(max_resource_ratio,abs(spectral)/bound)
        assert abs(spectral)<=bound*(1+1e-10)
        assert err<1e-8
        cases+=1

out={'date':'2026 10 06','seed':20261006,'exact_odd_degrees':len(exact),
     'random_circuits':240,'window_certificate_checks':cases,
     'max_scaled_window_spectral_identity_error':worst_identity,
     'max_observed_certificate_to_bound_ratio':max_resource_ratio,
     'capacity_coefficient':math.e**2*a*a/8,
     'noise_coefficient':math.e**2*a/2,
     'exact_coefficient_checks':exact,
     'interpretation':'Checks verify algebra/implementation; the analytic proof is primary. No novelty claim.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({k:v for k,v in out.items() if k!='exact_coefficient_checks'},indent=2))
