#!/usr/bin/env python3
"""Exact rational polynomial identity checks; NOT a Lean/proof-kernel substitute."""
from fractions import Fraction as F
import json
from pathlib import Path

class P:
    def __init__(self, terms=0):
        self.d = terms if isinstance(terms, dict) else ({():F(terms)} if terms else {})
        self.d = {m:F(c) for m,c in self.d.items() if c}
    def __add__(self, other):
        o=poly(other); r=dict(self.d)
        for m,c in o.d.items(): r[m]=r.get(m,F(0))+c
        return P(r)
    __radd__=__add__
    def __neg__(self): return P({m:-c for m,c in self.d.items()})
    def __sub__(self,other): return self+-poly(other)
    def __rsub__(self,other): return poly(other)+-self
    def __mul__(self,other):
        o=poly(other); r={}
        for m,c in self.d.items():
            for n,d in o.d.items():
                z=tuple(sorted(m+n)); r[z]=r.get(z,F(0))+c*d
        return P(r)
    __rmul__=__mul__
    def __truediv__(self,n): return self*F(1,n)
    def __pow__(self,n):
        assert isinstance(n,int) and n>=0
        r=P(1)
        for _ in range(n): r=r*self
        return r
def poly(x): return x if isinstance(x,P) else P(x)
def V(name): return P({(name,):F(1)})
S,D,k,t,a,g,eta,delta,rho,Q=[V(s) for s in 'S D k t a g eta delta rho Q'.split()]
def deficit(S,D,k): return D-(S-k)*(1-S+k)
checks=[]
def check(name,lhs,rhs):
    diff=poly(lhs)-poly(rhs)
    checks.append({'name':name,'passed':not diff.d,
        'nonzero_coefficients':{str(m):str(c) for m,c in diff.d.items()}})
check('packing_induction_affine_identity',
    deficit(S+t,D+t*(1-t),k),
    (1-t)*deficit(S,D,k)+t*deficit(S,D,k-1))
check('packing_base_integer_product',deficit(0,0,k),k*(k+1))
check('packing_negative_offset',deficit(S,D,k-1),D-(k-S)*(1-(k-S)))
check('half_coordinate_barrier',
    deficit(S-F(1,2),D-F(1,4),k-1),D-F(1,2)+(S-k)**2)
u=(1-a+g)/2; v=(1-a-g)/2
check('pair_sum',u+v,1-a)
check('pair_gap',u-v,g)
check('pair_defect',u*(1-u)+v*(1-v),(1-a*a-g*g)/2)
b=(1-t)/2; w=(1+t)/2
check('first_branch_defect_mod_root',w*(1-w)-delta,(1-4*delta-t*t)/4)
check('first_branch_bound_mod_root',1-2*delta-b*b-w*w,(1-4*delta-t*t)/2)
check('first_branch_endpoint_order',1-4*delta-(1-2*eta)**2,4*(eta*(1-eta)-delta))
check('middle_branch_box_order',(1-eta)**2-(1-2*delta-eta*eta),2*(delta-eta*(1-eta)))
check('half_scaled_packing',2*rho-4*Q-(2*rho-1)*(2-2*rho),4*(rho*rho-rho+F(1,2)-Q))
check('rounding_barrier_attainment',
    F(1,4)+(F(1,2)-eta)*(F(1,2)+eta),F(1,2)-eta*eta)
record={'status':'PASS' if all(c['passed'] for c in checks) else 'FAIL',
    'scope':'Exact rational coefficient normalization of listed polynomial identities only.',
    'not_checked':['Lean parsing/elaboration/kernel','inequality inference','finite induction validity',
                   'integer casts','sqrt branch semantics','topology','novelty'],
    'checks':checks}
out=Path(__file__).resolve().parent/'algebra-check.json'
out.write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'status':record['status'],'identities':len(checks),
                  'scope':record['scope']},ensure_ascii=False))
raise SystemExit(record['status']!='PASS')
