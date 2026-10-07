"""Exact rational verification of all 6-triangle audit designs on K5.

For a full-rank audit basis B in root-zero gauge, the worst repair
constant is max_cycle ||c B^{-1}||_1 / length(c). This follows from
the known maximum-cycle-mean formula and box duality. There are no
floating-point rank, optimization, or equality decisions here.
"""
import itertools as it
import json
from fractions import Fraction as F

def invert(matrix):
    size=len(matrix)
    aug=[[F(x) for x in row]+[F(i==j) for j in range(size)] for i,row in enumerate(matrix)]
    for col in range(size):
        pivot=next((r for r in range(col,size) if aug[r][col]),None)
        if pivot is None:return None
        aug[col],aug[pivot]=aug[pivot],aug[col]
        p=aug[col][col]
        aug[col]=[v/p for v in aug[col]]
        for r in range(size):
            if r!=col and aug[r][col]:
                p=aug[r][col]
                aug[r]=[a-p*b for a,b in zip(aug[r],aug[col])]
    return [row[size:] for row in aug]

n=5
edges=list(it.combinations(range(1,n),2))
edge_idx={e:i for i,e in enumerate(edges)}
def vec(cycle):
    v=[0]*len(edges)
    for a,b in zip(cycle,cycle[1:]+cycle[:1]):
        if a==0 or b==0:continue
        v[edge_idx[tuple(sorted((a,b)))]]+=1 if a<b else -1
    return v

triangles=list(it.combinations(range(n),3))
T=[vec(t) for t in triangles]
cycles=[]
for k in range(3,n+1):
    for subset in it.combinations(range(n),k):
        for tail in it.permutations(subset[1:]):
            cycle=(subset[0],)+tail
            if cycle[1]<cycle[-1]:cycles.append(cycle)
C=[vec(c) for c in cycles]
hist={}
designs=[]
for sel in it.combinations(range(10),6):
    B=[T[i] for i in sel]
    inv=invert(B)
    if inv is None:
        hist['unbounded']=hist.get('unbounded',0)+1
        continue
    Q=[[sum(row[k]*inv[k][j] for k in range(6)) for j in range(6)] for row in C]
    values=[sum(abs(q) for q in Q[j])/len(cycle) for j,cycle in enumerate(cycles)]
    worst=max(values)
    key=str(worst)
    hist[key]=hist.get(key,0)+1
    common=set(range(n))
    for i in sel:common.intersection_update(triangles[i])
    assert (worst==1)==bool(common)
    designs.append({'triangles':[triangles[i] for i in sel], 'constant':key, 'common_anchor':list(common)})

out={'n':n,'total_designs':210,'cycles_up_to_reversal':len(cycles),'histogram':hist,'designs':designs}
print(json.dumps(out,indent=2))
