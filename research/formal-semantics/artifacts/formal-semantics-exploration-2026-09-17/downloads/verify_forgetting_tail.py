from itertools import product
from math import lcm
from verify_forgetting import partitions, image
import json
from pathlib import Path

def G(n,r):
    return max(lcm(*p) for s in range(1,n+1) for p in partitions(s) if len(p)<=r)

def predicted(n,k):
    return max(h+G(n-h,k+1)-1 for h in range(n-1))

def exhaustive(n):
    maxima=[-1]*n
    count=0
    for f in product(range(n), repeat=n):
        rel=[1<<q for q in f]
        images=[image(S,rel) for S in range(1<<n)]
        for C in range(1,(1<<n)-1):
            size=C.bit_count()
            for z in range(n):
                if C&(1<<z):
                    continue
                seen=set()
                trajectory=[]
                S,q=C,z
                while (S,q) not in seen:
                    if S&(1<<q):
                        break
                    seen.add((S,q))
                    trajectory.append((S,q))
                    S,q=images[S],f[q]
                for P in range(1<<n):
                    count+=1
                    for t,(S,q) in enumerate(trajectory):
                        if not S&~P and not P&(1<<q):
                            maxima[size]=max(maxima[size],t)
                            break
    rows=[]
    for k in range(1,n):
        obs=max(maxima[1:k+1])
        expect=predicted(n,k)
        assert obs==expect,(n,k,obs,expect)
        rows.append(obs)
    return {'n':n,'all_total_maps':n**n,'C_z_P_cases':count,'max_by_k':rows}

def check_named_six_world_example():
    # a0->a1->a0, b0->b1->b2->b0, z->b0.
    f=[1,0,3,4,2,2]
    C=1<<0
    D=C|(1<<5)
    P=(1<<0)|(1<<2)|(1<<3)|(1<<5)
    rel=[1<<q for q in f]
    record=[]
    S,T=C,D
    for t in range(7):
        mismatch=not (S&~P) and bool(T&~P)
        record.append({'t':t,'C_mask':S,'D_mask':T,'mismatch':mismatch})
        assert mismatch==(t==6)
        S,T=image(S,rel),image(T,rel)
    return record

if __name__=='__main__':
    result={'status':'passed','exhaustive':[exhaustive(n) for n in range(2,6)],
            'six_world_first_strict_improvement':check_named_six_world_example(),
            'scope':'The finite verification does not establish novelty.'}
    Path('forgetting_tail_results.json').write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps(result,indent=2))
