#!/usr/bin/env python3
"""Exact-rational finite audit; supplementary evidence, not a proof."""
from fractions import Fraction as Q
from itertools import product, combinations
from math import comb
import json

def d(x): return sum(t*(1-t) for t in x)

def geometry(n,s,eta):
    lo,hi=Q(s)-eta,Q(s)+eta
    vertices=set()
    for x in product((Q(0),Q(1)),repeat=n):
        if lo<=sum(x)<=hi: vertices.add(x)
    for i in range(n):
        for z in product((Q(0),Q(1)),repeat=n-1):
            for t in (lo,hi):
                u=t-sum(z)
                if 0<u<1: vertices.add(z[:i]+(u,)+z[i:])
    vertices=sorted(vertices)
    edges=[]
    for i,j in combinations(range(len(vertices)),2):
        x,y=vertices[i],vertices[j]
        common=sum(u==v and u in (0,1) for u,v in zip(x,y))
        band=sum(x)==sum(y) and sum(x) in (lo,hi)
        if common+int(band)!=n-1: continue
        delta=[v-u for u,v in zip(x,y)]
        norm=sum(t*t for t in delta)
        slope=sum(v*(1-2*u) for u,v in zip(x,delta))
        t=max(Q(0),min(Q(1),slope/(2*norm)))
        peak=d(x)+slope*t-norm*t*t
        edges.append((i,j,peak))
    return vertices,edges

def expected(n,s,eta,delta):
    k=eta*(1-eta); c=(1-eta*eta)/2; h=Q(1,4); b=comb(n,s)
    if delta<k: return b
    if delta<min(c,h): return (n+1)*b
    if c<=delta<h: return b+comb(n,s-1)+comb(n,s+1)
    if h<=delta<c: return b
    return 1

def count(vertices,edges,delta):
    active={i for i,v in enumerate(vertices) if d(v)<=delta}
    parent={i:i for i in active}
    def root(i):
        while parent[i]!=i:
            parent[i]=parent[parent[i]]
            i=parent[i]
        return i
    for i,j,peak in edges:
        if peak<=delta:
            assert i in active and j in active
            parent[root(i)]=root(j)
    return len({root(i) for i in active})

records=[]
for n in range(2,7):
    for s in range(1,n):
        for eta in (Q(3,5),Q(3,4),Q(9,10)):
            vertices,edges=geometry(n,s,eta)
            thresholds=sorted({Q(0)}|{d(v) for v in vertices}|{p for _,_,p in edges})
            samples=sorted(set(thresholds)|{(a+b)/2 for a,b in zip(thresholds,thresholds[1:])}|{thresholds[-1]+Q(1,10)})
            assert len(vertices)==(n+1)*comb(n,s)
            for delta in samples:
                actual=count(vertices,edges,delta)
                predicted=expected(n,s,eta,delta)
                assert actual==predicted,(n,s,eta,delta,actual,predicted)
            records.append({'n':n,'s':s,'eta':str(eta),'vertices':len(vertices),'edges':len(edges),'samples':len(samples),'status':'PASS'})
print(json.dumps({'scope':'Exact rational enumeration of small-dimensional polytope vertices/edges; not a proof and not a point-grid connectivity test.','geometries':len(records),'sample_counts':sum(r['samples'] for r in records),'status':'PASS','records':records},indent=2))
