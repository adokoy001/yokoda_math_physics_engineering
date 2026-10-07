from functools import lru_cache
from itertools import combinations
import random,json

def sg(n,edges):
    moves=tuple((1<<u)|(1<<v) for u,v in edges)
    @lru_cache(None)
    def g(mask):
        seen={g(mask^e) for e in moves if mask&e==e}
        x=0
        while x in seen:x+=1
        return x
    return g((1<<n)-1)

def core(m,bits):
    edges=[(2*i,2*i+1) for i in range(m)]
    k=0
    for i,j in combinations(range(m),2):
        for flip in (0,1):
            if bits>>k&1:edges.extend([(2*i,2*j+flip),(2*i+1,2*j+1-flip)])
            k+=1
    return edges
report=[]
for m in range(4):
    count=0
    for bits in range(1<<(m*(m-1))):
        e=core(m,bits)
        for a in range(1<<(2*m)):
            edges=e+[(2*m,j) for j in range(2*m) if a>>j&1]
            value=sg(2*m+1,edges)
            assert value==m%2,(m,bits,a,value)
            count+=1
    report.append({'pairs':m,'exhaustive_labeled_graphs':count})
rng=random.Random(20260915)
for m,counts in [(4,2000),(5,1000),(6,300),(7,30)]:
    for _ in range(counts):
        bits=rng.randrange(1<<(m*(m-1)));a=rng.randrange(1<<(2*m))
        edges=core(m,bits)+[(2*m,j) for j in range(2*m) if a>>j&1]
        assert sg(2*m+1,edges)==m%2
    report.append({'pairs':m,'random_graphs':counts,'seed':20260915})
print(json.dumps(report,indent=2))
open('paired_core_results.json','w').write(json.dumps(report,indent=2))
