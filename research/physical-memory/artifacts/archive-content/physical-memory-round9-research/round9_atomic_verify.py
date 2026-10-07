#!/usr/bin/env python3
"""Sanity checks for the analytic theorem; standard library only."""
from fractions import Fraction
from math import sqrt
import random, json
from pathlib import Path
rng=random.Random(2026092909)

def gram(F):
    return [[sum(row[i]*row[j] for row in F) for j in range(len(F[0]))]
            for i in range(len(F[0]))]
def check(F, groups):
    k=len(groups); n=len(F[0]); G=[]
    for row in F:
        out=[0.0]*n
        for group in groups:
            j=max(group,key=lambda i:row[i]); out[j]=row[j]
        G.append(out)
    D=gram(F); D0=gram(G)
    W=sum(D[i][j] for gp in groups for i in gp for j in gp if i!=j)
    I=0
    for g in range(k):
        for h in range(g+1,k):
            z=[(1 if i in groups[g] else -1 if i in groups[h] else 0) for i in range(n)]
            I+=sum(z[i]*D[i][j]*z[j] for i in range(n) for j in range(n))
    I=max(0,I)
    loss=sum(D[i][j]-D0[i][j] for i in range(n) for j in range(n))
    bound=(2*k-.5)*W+2*sqrt((k-1)*I*W)
    crossloss=sum(D[i][j]-D0[i][j] for g in range(k) for h in range(g+1,k)
                  for i in groups[g] for j in groups[h])
    crossbound=(k-1)*W+sqrt((k-1)*I*W)
    scale=max(1.0,sum(map(sum,D)),bound)
    assert min(D[i][j]-D0[i][j] for i in range(n) for j in range(n))>=-1e-12*scale
    assert loss-bound<=1e-11*scale,(loss,bound)
    assert crossloss-crossbound<=1e-11*scale,(crossloss,crossbound)
    return (loss-bound)/scale
worst=-1.0
for trial in range(600):
    k=rng.randint(2,6); sizes=[rng.randint(1,6) for _ in range(k)]
    groups=[]; offset=0
    for size in sizes:
        groups.append(list(range(offset,offset+size))); offset+=size
    F=[]
    for _ in range(rng.randint(1,9)):
        row=[]
        for size in sizes:
            vs=[0 if rng.random()<.35 else 10**rng.uniform(-3,3) for _ in range(size)]
            if trial%2==0:
                s=sum(vs)
                if s==0: vs[0]=1; s=1
                vs=[v/s for v in vs]
            row.extend(vs)
        F.append(row)
    worst=max(worst,check(F,groups))
sharp=[]
for k in range(2,10):
    W=Fraction(1,2)
    loss=Fraction(k*k)-Fraction(2*k-1,2)**2
    assert loss==(2*k-Fraction(1,2))*W
    sharp.append({'k':k,'W':str(W),'loss':str(loss),'coefficient':str(loss/W)})
result={'random_cases':600,'max_normalized_excess':worst,'exact_rational_sharp_cases':sharp}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
