"""Exact finite checks for the derived progress-budget lemma; not a proof assistant."""
from fractions import Fraction as Q
from itertools import product
from random import Random
import json
from pathlib import Path

rng=Random(20261006)
def osc(v): return max(v)-min(v)
def sub(a,b): return [x-y for x,y in zip(a,b)]
generic=closed=gauge=0
for _ in range(500):
    m=rng.randrange(2,8); n=rng.randrange(2,30)
    w=[[Q(rng.randrange(-20,21),4) for _ in range(m)] for _ in range(n)]
    path=[rng.randrange(m) for _ in range(n+1)]
    if _%2==0: path[-1]=path[0]
    gain=sum(w[t][path[t+1]]-w[t][path[t]] for t in range(n))
    drift=sum(osc(sub(w[t],w[t-1])) for t in range(1,n))
    telescoping=w[0][path[-1]]-w[0][path[0]]+sum((w[t][path[-1]]-w[t-1][path[-1]])-(w[t][path[t]]-w[t-1][path[t]]) for t in range(1,n))
    assert gain==telescoping
    assert gain<=osc(w[0])+drift
    generic+=1
    if path[-1]==path[0]:
        assert gain<=drift;closed+=1
    shifts=[rng.randrange(-1000,1001) for _ in range(n)]
    shifted=[[x+c for x in row] for row,c in zip(w,shifts)]
    assert osc(shifted[0])==osc(w[0])
    assert sum(osc(sub(shifted[t],shifted[t-1])) for t in range(1,n))==drift
    gauge+=1

states=list(product([0,1],repeat=3)); idx={s:i for i,s in enumerate(states)}
a=(-1,0,1); gamma=(Q(2),)*3; eta=Q(1,4)
accepted=0;g04runs=0;g04closed=0
for _ in range(200):
    state=rng.randrange(8);path=[state]; ws=[];surpluses=[]
    for tick in range(50):
        phi=[Q(rng.randrange(-20,21),4) for _ in states]
        h=[Q(rng.randrange(-4,5),4) for _ in states]
        u=[[phi[s]+a[i]*h[s] for s in range(8)] for i in range(3)]
        w=[max(u[i][s]-gamma[i]/2 for i in range(3)) for s in range(8)]
        for i in range(3):
            for s in range(8):
                assert u[i][s]-gamma[i]/2<=w[s]<=u[i][s]+gamma[i]/2
        moves=[]
        for i in range(3):
            target=list(states[state]);target[i]=1-target[i];dest=idx[tuple(target)]
            diff=u[i][dest]-u[i][state]
            if diff>gamma[i]+eta: moves.append((i,dest,diff))
        if not moves:continue
        i,dest,diff=rng.choice(moves)
        assert w[dest]-w[state]>=diff-gamma[i]>eta
        ws.append(w);surpluses.append(diff-gamma[i]);path.append(dest);state=dest
    if not ws:continue
    n=len(ws);accepted+=n;g04runs+=1
    potential_sum=sum(ws[t][path[t+1]]-ws[t][path[t]] for t in range(n))
    drift=sum(osc(sub(ws[t],ws[t-1])) for t in range(1,n))
    assert sum(surpluses)<=potential_sum<=osc(ws[0])+drift
    assert n*eta<osc(ws[0])+drift
    for start in range(n):
        for end in range(start+1,n+1):
            if path[start]!=path[end]:continue
            localdrift=sum(osc(sub(ws[t],ws[t-1])) for t in range(start+1,end))
            assert (end-start)*eta<localdrift
            g04closed+=1

# Infinite counterexample's initial 100 terms, exactly.
counter_n=100
counter=[[Q(0),Q((-1)**t,2**t)] for t in range(counter_n)]
path=[t%2 for t in range(counter_n+1)]
for t in range(counter_n):
    assert counter[t][path[t+1]]-counter[t][path[t]]==Q(1,2**t)>0
counter_drift=sum(osc(sub(counter[t],counter[t-1])) for t in range(1,counter_n))
assert counter_drift==3*(1-Q(1,2**(counter_n-1)))<3

# Sharpness examples.
assert (1-0)+(2-1)==1+osc([0,0,1])
assert (1-0)+(1-0)==osc([1,-1])

out={"seed":20261006,"arithmetic":"fractions.Fraction","generic_paths":generic,"closed_generic_paths":closed,"gauge_invariance_cases":gauge,"g04_runs":g04runs,"g04_accepted_steps":accepted,"g04_closed_subpaths":g04closed,"counterexample_prefix":counter_n,"sharpness_examples":2,"status":"passed"}
Path(__file__).with_name('dynamic_progress_results.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out))
