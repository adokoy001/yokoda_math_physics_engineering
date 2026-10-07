import itertools as it
import json
import numpy as np
from scipy.optimize import linprog

def model(n):
    edges=list(it.combinations(range(1,n),2))
    edge_idx={e:i for i,e in enumerate(edges)}
    def vec(sequence):
        out=np.zeros(len(edges))
        for a,b in zip(sequence,sequence[1:]+sequence[:1]):
            if a==0 or b==0: continue
            out[edge_idx[tuple(sorted((a,b)))]]+=1 if a<b else -1
        return out
    triangles=list(it.combinations(range(n),3))
    T=np.array([vec(t) for t in triangles])
    cycles=[]
    C=[]
    for k in range(3,n+1):
        for subset in it.combinations(range(n),k):
            for tail in it.permutations(subset[1:]):
                cyc=(subset[0],)+tail
                if cyc[1]>cyc[-1]: continue
                cycles.append(cyc)
                C.append(vec(cyc)/k)
    return edges,triangles,T,cycles,np.array(C)

def constant(n,selection,mdl=None):
    if mdl is None:mdl=model(n)
    edges,triangles,T,cycles,C=mdl
    A=T[selection]
    if np.linalg.matrix_rank(A)<len(edges): return float('inf'),None
    best=(-1,None)
    for cyc,c in zip(cycles,C):
        res=linprog(-c,A_ub=np.r_[A,-A],b_ub=np.ones(2*len(A)),bounds=[(None,None)]*len(edges),method='highs')
        assert res.success
        if -res.fun>best[0]+1e-8:best=(-res.fun,{'cycle':cyc,'gauge_edges':edges,'values':res.x.tolist()})
    return best

def main():
    out={'basic':[]}
    for n in range(3,9):
        mdl=model(n)
        tris=mdl[1]
        # n=8 has 8000+ cycles, explicit full worst matrix provides a smaller check.
        if n<=6:
            full=constant(n,list(range(len(tris))),mdl)[0]
            star=constant(n,[i for i,t in enumerate(tris) if 0 in t],mdl)[0]
            single_missing=constant(n,list(range(len(tris)-1)),mdl)[0] if n>=4 else 'unbounded'
            out['basic'].append({'n':n,'full':full,'star':star,'single_missing':single_missing})
    mdl=model(5)
    hist={}
    worst=(0,None)
    count=0
    for sel in it.combinations(range(10),6):
        c,w=constant(5,list(sel),mdl)
        if not np.isfinite(c):continue
        count+=1
        key=str(round(c,8))
        hist[key]=hist.get(key,0)+1
        if c>worst[0]+1e-8:worst=(c,{'triangles':[mdl[1][i] for i in sel],'witness':w})
    out['n5_bases']={'count':count,'histogram':hist,'worst':worst}
    print(json.dumps(out,indent=2))

if __name__=='__main__':main()
