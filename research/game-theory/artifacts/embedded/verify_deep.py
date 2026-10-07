"""Reproducible checks for sharp shared-error margins and capped audit schedules."""
from itertools import combinations,product
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
from scipy.optimize import linprog

rng=np.random.default_rng(20260910)

def margin_lp(a,weights,eps=1):
    n=len(a);rows=[];rhs=[]
    for i,j in combinations(range(n),2):
        r=np.zeros(n);r[i]=r[j]=-1;rows.append(r);rhs.append(-2*eps*np.sum(np.abs(a[i]-a[j])))
    res=linprog(weights,A_ub=rows,b_ub=rhs,bounds=[(0,None)]*n,method='highs')
    assert res.success
    return res.x,res.fun

margin_edges=0;games=0;scalar_medians=0;witnesses=0
for n in range(2,7):
    states=list(product([0,1],repeat=n));S=len(states);index={s:i for i,s in enumerate(states)}
    for case in range(30):
        a=rng.integers(-5,6,size=(n,3)).astype(float);eps=float(rng.uniform(.05,1))
        gamma,_=margin_lp(a,rng.uniform(.1,3,size=n),eps)
        h=rng.uniform(-eps,eps,size=(S,3));phi=rng.normal(size=S)*10
        U=phi[:,None]+h@a.T;W=np.max(U-gamma/2,axis=1)
        assert np.all(W[:,None]>=U-gamma/2-1e-8)
        assert np.all(W[:,None]<=U+gamma/2+1e-8)
        for s_idx,s in enumerate(states):
            for i in range(n):
                t=list(s);t[i]=1-t[i];t_idx=index[tuple(t)]
                if U[t_idx,i]-U[s_idx,i]>gamma[i]+1e-8:
                    assert W[t_idx]>W[s_idx]-1e-8; margin_edges+=1
        games+=1
for n in range(2,12):
    for case in range(10):
        a=rng.integers(-10,11,size=(n,1));weights=rng.integers(1,8,size=n)
        _,val=margin_lp(a,weights)
        candidates=[2*sum(int(w)*abs(int(x)-int(alpha)) for w,x in zip(weights,a[:,0])) for alpha in a[:,0]]
        assert abs(val-min(candidates))<1e-7;scalar_medians+=1
# Exact rational square witnesses, norm is infinity and dual norm is 1.
for _ in range(200):
    ai=[int(x) for x in rng.integers(-4,5,size=3)];aj=[int(x) for x in rng.integers(-4,5,size=3)]
    distance=sum(abs(y-x) for x,y in zip(ai,aj))
    if not distance:continue
    eps=F(1,3);gi=gj=eps*distance/F(2)
    v=[(y>x)-(y<x) for x,y in zip(ai,aj)]
    aa=sum(x*y for x,y in zip(ai,v));bb=sum(x*y for x,y in zip(aj,v))
    q=(gi+2*eps*aa+2*eps*bb-gj)/2
    gains=[q-2*eps*aa,-q+2*eps*bb,q-2*eps*aa,-q+2*eps*bb]
    assert gains[0]>gi and gains[1]>gj and gains[2]>gi and gains[3]>gj;witnesses+=1

audit_exact=0;audit_lp_cases=0
for n in range(5,31):
    edges=list(combinations(range(n),2));N=len(edges);r=n-2;D=n*n-3*n-2
    for fraction in [F(0),F(1,3),F(2,3),F(1)]:
        rho=fraction/N;target=F((n-3)*(n-4),D)+F(2*(n-3),D)*rho
        weights=[]
        for e in edges:
            if e==(0,1):w=rho
            elif 0 in e or 1 in e:w=(1-rho-target)/(2*r)
            else:w=2*target/(r*(r-1))
            weights.append(w)
        assert min(weights)>=0 and sum(weights)==1
        # Three symmetry classes checked exactly; for n<=12 enumerate all rows.
        q_values=[]
        testpairs=edges if n<=12 else [(0,1),(0,2),(2,3)]
        for e in testpairs:q_values.append(sum(w for f,w in zip(edges,weights) if set(e).isdisjoint(f)))
        assert min(q_values)==target;audit_exact+=1
        if n<=10:
            M=np.array([[int(set(e).isdisjoint(f)) for f in edges] for e in edges],float)
            obj=np.zeros(N+1);obj[-1]=-1
            bounds=[(0,float(rho))]+[(0,1)]*(N-1)+[(0,1)]
            res=linprog(obj,A_ub=np.column_stack([-M,np.ones(N)]),b_ub=np.zeros(N),A_eq=[list(np.ones(N))+[0]],b_eq=[1],bounds=bounds,method='highs')
            assert res.success and abs(-res.fun-float(target))<1e-9;audit_lp_cases+=1

def graph_case(name,M):
    v=len(M);degrees=M.sum(axis=1);assert np.all(degrees==degrees[0]);d=int(degrees[0])
    common=M@M;ls={int(common[i,j]) for i,j in combinations(range(v),2) if M[i,j]};mus={int(common[i,j]) for i,j in combinations(range(v),2) if not M[i,j]}
    assert len(ls)==len(mus)==1
    la=ls.pop();mu=mus.pop();assert mu>=la and mu>0
    for f in [F(0),F(1,3),F(2,3),F(1)]:
        rho=f/v;T=(F(mu)+(d-mu)*rho)/(d+mu-la)
        w=[rho]+[T/d if M[0,i] else (1-rho-T)/(v-d-1) for i in range(1,v)]
        assert min(w)>=0 and sum(w)==1
        q=[sum(w[j] for j in range(v) if M[i,j]) for i in range(v)]
        assert min(q)==T
        obj=np.zeros(v+1);obj[-1]=-1
        res=linprog(obj,A_ub=np.column_stack([-M,np.ones(v)]),b_ub=np.zeros(v),A_eq=[list(np.ones(v))+[0]],b_eq=[1],bounds=[(0,float(rho))]+[(0,1)]*v,method='highs')
        assert res.success and abs(-res.fun-float(T))<1e-9
    return {'name':name,'v':v,'d':d,'lambda':la,'mu':mu,'cases':4}

graphs=[]
for q in [5,13,17]:
    residues={(x*x)%q for x in range(1,q)}
    M=np.array([[int(i!=j and (j-i)%q in residues) for j in range(q)] for i in range(q)],int)
    graphs.append(graph_case('Paley'+str(q),M))
for q in [3,4]:
    pts=list(product(range(q),repeat=2));M=np.array([[int(x!=y and (x[0]==y[0] or x[1]==y[1])) for y in pts] for x in pts],int)
    graphs.append(graph_case('Rook'+str(q),M))
for n in range(5,10):
    E=list(combinations(range(n),2));M=np.array([[int(set(e).isdisjoint(f)) for f in E] for e in E],int)
    graphs.append(graph_case('KG('+str(n)+',2)',M))
for parts,size in [(2,3),(3,3),(4,2)]:
    pts=list(product(range(parts),range(size)));M=np.array([[int(x[0]!=y[0]) for y in pts] for x in pts],int)
    graphs.append(graph_case('Multipartite'+str((parts,size)),M))
out={'seed':20260910,'vector_games':games,'accepted_edges_checked':margin_edges,'scalar_weighted_medians':scalar_medians,'rational_cycle_witnesses':witnesses,'audit_exact_constructions':audit_exact,'audit_full_LP_cases':audit_lp_cases,'strongly_regular_graphs':graphs,'srg_LP_cases':sum(g['cases'] for g in graphs)}
Path('deep_verification_results.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out))