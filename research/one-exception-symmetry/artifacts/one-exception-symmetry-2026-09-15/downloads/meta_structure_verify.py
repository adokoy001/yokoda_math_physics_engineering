from functools import lru_cache
from itertools import combinations,product
import random,json

def sg(n,edges):
    moves=tuple(set(sum(1<<v for v in e) for e in edges))
    @lru_cache(None)
    def g(mask):
        seen={g(mask^e) for e in moves if mask&e==e}
        k=0
        while k in seen:k+=1
        return k
    mask=(1<<n)-1
    return g(mask),sorted({g(mask^e) for e in moves})

def params(r,m,q):
    bs=[set(range(r*i,r*(i+1))) for i in range(m)]
    ex=set(range(r*m,r*m+q))
    orbits=[]
    for a,b in combinations(bs,2):
        allv=a|b
        for e in combinations(sorted(allv),r):
            f=tuple(sorted(allv-set(e)))
            if set(e) not in (a,b) and e<f:orbits.append([e,f])
    for b in bs:
        for e in combinations(sorted(b|ex),r):
            if set(e)&ex:orbits.append([e])
    return [tuple(sorted(b)) for b in bs],orbits

def instance(r,m,q,bits):
    blocks,orbits=params(r,m,q)
    return blocks+[e for i,orb in enumerate(orbits) if bits>>i&1 for e in orb]

if __name__=='__main__':
    report={'exhaustive':[],'random':[],'examples':{},'seed':20260915}
    for r,m,q in [(3,1,0),(3,1,1),(3,1,2),(3,2,0),(3,2,1)]:
        bs,orbits=params(r,m,q)
        for bits in range(1<<len(orbits)):
            es=bs+[e for i,orb in enumerate(orbits) if bits>>i&1 for e in orb]
            val,_=sg(r*m+q,es)
            assert val==m%2,(r,m,q,bits,val)
        report['exhaustive'].append({'r':r,'m':m,'q':q,'count':1<<len(orbits)})
    rng=random.Random(20260915)
    for r,m,q,count in [(3,2,2,500),(3,3,2,500),(3,4,2,300),(4,2,3,300),(4,3,3,300)]:
        bs,orbits=params(r,m,q)
        for _ in range(count):
            bits=rng.getrandbits(len(orbits))
            es=bs+[e for i,orb in enumerate(orbits) if bits>>i&1 for e in orb]
            val,_=sg(r*m+q,es)
            assert val==m%2,(r,m,q,bits,val)
        report['random'].append({'r':r,'m':m,'q':q,'count':count})
    # r=3, blocks A=012 B=345; exception xy=67.
    examples={
      'r3_transfer':(8,[(0,1,2),(3,4,5),(0,1,3),(2,4,5),(6,7,0),(6,3,4),(7,1,2)]),
      'missing_complement':(6,[(0,1,2),(3,4,5),(0,1,3)]),
      'exception_two_blocks':(7,[(0,1,2),(3,4,5),(6,0,3)]),
      'exception_too_large':(6,[(0,1,2),(3,4,0),(5,1,2)]),
      'missing_block':(3,[]),
      'mixed_size':(6,[(0,1),(2,3,4),(0,2),(1,3,4),(5,0),(5,2),(5,3,4)])
    }
    for name,(n,es) in examples.items():
        value,opts=sg(n,es)
        report['examples'][name]={'n':n,'edges':es,'grundy':value,'option_values':opts}
    # Find counterexample with a three-block move, other requirements retained.
    bs,orbits=params(3,3,0)
    cross3=list(product(range(3),range(3,6),range(6,9)))
    for t in range(10000):
        chosen=[orb for orb in orbits if rng.random()<.08]
        es=bs+[e for orb in chosen for e in orb]+[e for e in cross3 if rng.random()<.08]
        val,opts=sg(9,es)
        if val!=1:
            # Remove optional core-orbits/triple moves greedily, preserve failed value.
            groups=chosen+[[e] for e in es[len(bs)+sum(map(len,chosen)):]]
            change=True
            while change:
                change=False
                for i in range(len(groups)):
                    cand=groups[:i]+groups[i+1:]
                    nv,_=sg(9,bs+[e for group in cand for e in group])
                    if nv!=1:groups=cand;change=True;break
            es=bs+[e for group in groups for e in group]
            val,opts=sg(9,es)
            report['examples']['three_blocks']={'n':9,'edges':es,'grundy':val,'option_values':opts}
            break
    print(json.dumps(report,indent=2))
    open('meta_structure_results.json','w').write(json.dumps(report,indent=2))
