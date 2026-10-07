#!/usr/bin/env python3
"""Finite checks of the edge-star construction; not a proof of optimality."""
import json, math
from pathlib import Path
import numpy as np

def stable_r(x):
    return x/math.expm1(x) if x < 700 else 0.0

def kernel(mu,t,h,T):
    return math.exp(-mu*t)*(-math.expm1(-mu*h))**2/mu*((-math.expm1(-mu*T)/(mu*T))**2 if T else 1.0)

def optimum(t,h,T):
    a,b=t/h,T/h
    def g(x):return 2*stable_r(x)+(2*stable_r(b*x) if b else 2)-3-a*x
    lo,hi=0.0,1.0
    while g(hi)>0:hi*=2
    for _ in range(100):
        mid=(lo+hi)/2
        if g(mid)>0:lo=mid
        else:hi=mid
    mu=(lo+hi)/(2*h)
    return mu,kernel(mu,t,h,T)

def build(n,lam,c0,budgets,rates):
    ports=2*n; kappa=lam*c0/n
    active=[(i,j,float(budgets[i,j]),float(rates[i,j])) for i in range(n) for j in range(n) if budgets[i,j]>0]
    r=len(active);spokes=np.zeros((r,ports));diag=np.zeros(r);caps=np.zeros(r)
    for z,(i,j,a,mu) in enumerate(active):
        spokes[z,i]=spokes[z,n+j]=2*a;diag[z]=4*a;caps[z]=4*a/mu
    direct=np.zeros((ports,ports))
    for i in range(n):
        for j in range(n):
            v=np.zeros(ports);v[i]=1;v[n+j]=-1
            direct+=(kappa-budgets[i,j])*np.outer(v,v)
    Lbb=direct+np.diag(spokes.sum(axis=0))
    K=Lbb-(spokes.T/diag)@spokes if r else Lbb.copy()
    B=spokes/np.sqrt(caps)[:,None] if r else spokes
    return K,Lbb,B,np.array([mu for _,_,_,mu in active])

def target(n,lam,c0):
    I=np.eye(n);J=np.ones((n,n))/n
    H=c0*np.block([[I,J],[J,I]])
    K=lam*c0*np.block([[I,-J],[-J,I]])
    return K,H

out={'checks':[]}
for n in range(2,11):
    for k in range(n+1):
        lam,c0=1.7,.8;kappa=lam*c0/n
        budgets=np.zeros((n,n));rates=np.full((n,n),lam)
        for i in range(n):
            for shift in range(k):budgets[i,(i+shift)%n]=kappa
        K,Lbb,B,poles=build(n,lam,c0,budgets,rates)
        Kstar,H=target(n,lam,c0)
        static=float(np.max(np.abs(K-Kstar)))
        HF=Kstar+lam*H
        actual=float(np.linalg.norm(HF-Lbb,2));expected=2*lam*c0*(1-k/n)
        assert static<1e-12 and abs(actual-expected)<1e-12
        for omega in [.2,1,20]:
            if len(poles):Y=Lbb-B.T@((1/(poles+1j*omega))[:,None]*B)
            else:Y=Lbb.astype(complex)
            Ys=Kstar+(1j*omega*lam/(1j*omega+lam))*H
            got=float(np.linalg.norm(Ys-Y,2))
            want=expected*abs(1j*omega/(1j*omega+lam))
            assert abs(got-want)<1e-12
        out['checks'].append({'n':n,'k':k,'states':n*k,'static_error':static,'high_frequency_norm':actual,'exact_formula':expected})
n=10;lam=c0=h=1.;t=T=.1;eps=.05
mu,qmax=optimum(t,h,T);alpha=lam*kernel(lam,t,h,T)
quotient=n*n*(alpha-eps)/(lam*qmax);r=math.ceil(quotient);kappa=lam*c0/n
budgets=np.zeros((n,n));budgets.flat[:r-1]=kappa;budgets.flat[r-1]=(quotient-r+1)*kappa
rates=np.full((n,n),mu)
K,Lbb,B,poles=build(n,lam,c0,budgets,rates)
Kstar,H=target(n,lam,c0)
# D=B.T f(Q) B, with f(mu)=q(mu)/mu because B.T B coefficients are a*mu.
D=B.T@((np.array([kernel(p,t,h,T)/p for p in poles]))[:,None]*B)
d=float(D[:n,n:].sum()/n)
assert np.max(np.abs(K-Kstar))<1e-12
assert abs(d-(alpha-eps))<1e-12
assert abs(r-85)==0
out['scalar_case']={'states':r,'real_quotient':quotient,'mu':mu,'qmax':qmax,'alpha':alpha,'actual_d':d,'target_lower_endpoint':alpha-eps,'partial_budget_fraction':quotient-r+1,'static_error':float(np.max(np.abs(K-Kstar)))}
path=Path(__file__).with_suffix('.json');path.write_text(json.dumps(out,indent=2))
print(json.dumps({'cases':len(out['checks']),'scalar':out['scalar_case'],'all_passed':True},indent=2))
