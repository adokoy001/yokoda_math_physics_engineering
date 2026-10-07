from itertools import combinations
import json
import numpy as np
from scipy.optimize import milp, Bounds, LinearConstraint

def solve(n,k,m):
    blocks=list(combinations(range(n),k)); pairs=list(combinations(range(n),2)); b=len(blocks)
    rows=[]; lo=[]; hi=[]
    r=np.zeros(2*b+1);r[:b]=1;rows.append(r);lo.append(1);hi.append(1)
    r=np.zeros(2*b+1);r[b:2*b]=1;rows.append(r);lo.append(-np.inf);hi.append(m)
    for z in range(b):
        r=np.zeros(2*b+1);r[z]=1;r[b+z]=-1;rows.append(r);lo.append(-np.inf);hi.append(0)
    for i,j in pairs:
        r=np.zeros(2*b+1);r[-1]=1
        for z,S in enumerate(blocks):
            if i in S and j in S:r[z]=-1
        rows.append(r);lo.append(-np.inf);hi.append(0)
    obj=np.zeros(2*b+1);obj[-1]=-1
    ints=np.zeros(2*b+1);ints[b:2*b]=1
    res=milp(obj,integrality=ints,bounds=Bounds(np.zeros(2*b+1),np.ones(2*b+1)),constraints=LinearConstraint(np.array(rows),lo,hi),options={'time_limit':8,'mip_rel_gap':1e-9})
    return {'n':n,'k':k,'m':m,'status':int(res.status),'value':None if res.x is None else float(res.x[-1]),'dual_bound':None if getattr(res,'mip_dual_bound',None) is None else -float(res.mip_dual_bound),'schedule':[] if res.x is None else [(list(S),float(w)) for S,w in zip(blocks,res.x[:b]) if w>1e-7]}

if __name__ == '__main__':
    cases = [(4,2),(5,3),(6,4),(7,4),(7,5),(8,5),(8,6),(9,6),(10,7)]
    for n, k in cases:
        result = solve(n, k, 4)
        print(json.dumps(result, ensure_ascii=False), flush=True)
        if result['status'] != 0:
            raise RuntimeError('MILP did not finish optimally; increase time_limit and rerun.')