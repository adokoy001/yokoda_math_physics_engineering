"""Exact arithmetic checks for sequence rounding; no random tolerance needed."""
from itertools import product
from fractions import Fraction
import json
from pathlib import Path

summary={'denominator':4,'max_n':6,'sequences':0,'rounding_vectors':0,'global_rounding_vectors':0,'failures':0}
q=summary['denominator']
for n in range(1,summary['max_n']+1):
    for a in product(range(q+1),repeat=n):
        s=[0]
        for v in a:s.append(s[-1]+v)
        residues=sorted({v%q for v in s})
        gaps=[b-a for a,b in zip(residues,residues[1:]+[q])]
        produced={}
        for lo,hi in zip(residues,residues[1:]+[q]):
            # Threshold strictly inside the gap; doubled integer arithmetic.
            threshold2=lo+hi
            z=[v//q + int(2*(v%q)>=threshold2) for v in s]
            y=tuple(z[i+1]-z[i] for i in range(n))
            e=[q*z[k]-s[k] for k in range(n+1)]
            D=max(e)-min(e)
            assert D==q-(hi-lo)
            assert y not in produced
            produced[y]=(hi-lo,D)
        globally_feasible=set()
        optimum=q*n+1
        for y in product([0,1],repeat=n):
            # Integer coordinates are required to stay exact when already integer.
            if any(a[i]==0 and y[i] or a[i]==q and not y[i] for i in range(n)):
                continue
            summary['rounding_vectors']+=1
            e=[0]
            for i in range(n):e.append(e[-1]+q*y[i]-a[i])
            D=max(e)-min(e)
            optimum=min(optimum,D)
            if D<q:globally_feasible.add(y)
        assert globally_feasible==set(produced)
        assert optimum==q-max(gaps)
        assert all(sum(m*y[i] for y,(m,D) in produced.items())==a[i] for i in range(n))
        assert sum(m*D for m,D in produced.values())==q*q-sum(g*g for g in gaps)
        summary['sequences']+=1
        summary['global_rounding_vectors']+=len(produced)
print(json.dumps(summary,indent=2))
Path(__file__).with_name('verification.json').write_text(json.dumps(summary,indent=2)+'\n')
