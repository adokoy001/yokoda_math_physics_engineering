"""Independent WAK verification by direct capacity-state mex, without clone reduction.
Python standard library only. Run: python weighted_verify.py
"""
from functools import lru_cache
from itertools import product
from pathlib import Path
import json,random

def wak_grundy(capacities,edges):
    edges=tuple(edges)
    @lru_cache(None)
    def dp(caps):
        options=set()
        for a,b in edges:
            if caps[a] and caps[b]:
                nxt=list(caps);nxt[a]-=1;nxt[b]-=1
                options.add(dp(tuple(nxt)))
        g=0
        while g in options:g+=1
        return g
    return dp(tuple(capacities)),dp.cache_info().currsize

def core_edges(m,mask):
    edges=[(2*i,2*i+1) for i in range(m)]
    bit=0
    for i in range(m):
        for j in range(i+1,m):
            for flip in range(2):
                if mask>>bit&1:
                    edges.extend([(2*i,2*j+flip),(2*i+1,2*j+1-flip)])
                bit+=1
    return edges

def evaluate(m,c,coremask,adjmask):
    z=2*m
    capacities=[v for x in c for v in (x,x)]+[1]
    edges=core_edges(m,coremask)+[(i,z) for i in range(z) if adjmask>>i&1]
    got,states=wak_grundy(capacities,edges)
    expected=sum(c)%2
    return got,expected,states

def main():
    report={'method':'capacity tuple dynamic programming with mex; no clone reduction used by verifier',
            'seed':20260915,'exhaustive':[],'random':{},'counterexample':{},'total_checked':0,'violations':[]}
    states=0
    for m in (1,2):
        checked=0;observed={}
        for c in product(range(1,4),repeat=m):
            for cm in range(1<<(m*(m-1))):
                for am in range(1<<(2*m)):
                    got,expected,numstates=evaluate(m,c,cm,am)
                    states+=numstates;checked+=1
                    observed[got]=observed.get(got,0)+1
                    if got!=expected:report['violations'].append(dict(m=m,c=c,coremask=cm,adjmask=am,got=got,expected=expected))
        report['exhaustive'].append(dict(pairs=m,capacities='each c_i in 1..3',symmetric_core_count=1<<(m*(m-1)),exception_neighbor_count=1<<(2*m),cases=checked,grundy_histogram=observed))
        report['total_checked']+=checked
    rng=random.Random(report['seed']);m=3;seen=set();observed={}
    while len(seen)<200:
        c=tuple(rng.randint(1,3) for _ in range(m));cm=rng.randrange(1<<(m*(m-1)));am=rng.randrange(1<<(2*m))
        key=(c,cm,am)
        if key in seen:continue
        seen.add(key)
        got,expected,numstates=evaluate(m,c,cm,am)
        states+=numstates;observed[got]=observed.get(got,0)+1
        if got!=expected:report['violations'].append(dict(m=m,c=c,coremask=cm,adjmask=am,got=got,expected=expected))
    report['random']=dict(pairs=3,cases=200,capacities='each c_i in 1..3',sampling='uniform draws without duplicate parameter tuples',grundy_histogram=observed)
    report['total_checked']+=200
    g,n=wak_grundy([1,1,2],[(0,1),(0,2),(1,2)])
    report['counterexample']=dict(graph='triangle',capacities=[1,1,2],core_pairs=[[0,1]],exception=2,actual_grundy=g,claimed_parity_if_generalized=1,option_grundy_values=[0,1])
    report['sum_dp_states_across_cases']=states
    dest=Path(__file__).with_name('weighted_verify.json')
    dest.write_text(json.dumps(report,indent=2,ensure_ascii=False)+'\n')
    print(json.dumps(report,indent=2,ensure_ascii=False))
    assert not report['violations']
    assert g==2
if __name__=='__main__':main()
