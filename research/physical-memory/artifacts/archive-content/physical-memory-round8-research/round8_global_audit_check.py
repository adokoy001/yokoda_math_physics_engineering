"""Independent exact-rational scalar threshold and randomized RC-component checks.

Requires Python 3, numpy, scipy. Example: python -m pip install numpy scipy
Writes a JSON result beside this script; no project-directory layout is needed.
"""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np
from scipy.optimize import brentq

# Alternating series, exact rationals, 0 <= x <= 1.
def expneg(x, n=32):
    term=F(1); even=term
    for k in range(1,n+1):
        term *= -x/k
        even += term
    odd=even + term*(-x)/(n+1)
    return odd, even

def G_bounds(x):
    xl,xh=expneg(x)
    yl,yh=expneg(x/10)
    return (2*x*xl/(1-xl)+2*(x/10)*yl/(1-yl)-3-x/10,
            2*x*xh/(1-xh)+2*(x/10)*yh/(1-yh)-3-x/10)

lo=F('0.96093330677944'); hi=F('0.96093330677945')
assert G_bounds(lo)[0]>0 and G_bounds(hi)[1]<0
el,eh=expneg(lo/10); fl,fh=expneg(hi/10)
gl,gh=expneg(lo); hl,hh=expneg(hi)
qlo=fl*(1-eh)**2*(1-gh)**2*100/hi**3
qhi=eh*(1-fl)**2*(1-hl)**2*100/lo**3
al,ah=expneg(F(1,10)); bl,bh=expneg(F(1))
alpha_lo=al*(1-ah)**2*100*(1-bh)**2
alpha_hi=ah*(1-al)**2*100*(1-bl)**2
assert F(84,100)*qhi < alpha_lo-F(1,20)
assert F(85,100)*qlo > alpha_hi-F(1,20)
# The finite-ramp k>=3 certificate also verified by exact rational arithmetic.
assert 3*alpha_lo>F(29,30)

def q(x):
    return np.exp(-x*.1)*(-np.expm1(-x*.1)/(x*.1))**2*(-np.expm1(-x))**2/x
xstar=brentq(lambda x:2*x/np.expm1(x)+.2*x/np.expm1(.1*x)-3-.1*x,.8,1.1)
qstar=q(xstar)
rng=np.random.default_rng(902913)
rows=[]
for k in range(1,9):
    maximum=0.; max_budget_ratio=0.; negative_residue=0
    for trial in range(400):
        edges=rng.uniform(.02,1.,(k,k)); edges=np.triu(edges,1); edges=edges+edges.T
        # Include sparse port attachment to give negative spectral residues.
        left=rng.uniform(.02,1.,k); right=rng.uniform(.02,1.,k)
        if k>1 and trial%2==0:
            left[1:]=0.; right[:-1]=0.
        cap=10**rng.uniform(-.6,.6,k)
        lap=np.diag(edges.sum(axis=1)+left+right)-edges
        inv=np.diag(cap**-.5); Q=inv@lap@inv
        u=inv@left; v=inv@right
        rates,V=np.linalg.eigh(Q)
        residues=(V.T@u)*(V.T@v)
        negative_residue += int(np.any(residues< -1e-12))
        budget=u@np.linalg.solve(Q,v)
        response=np.sum(residues*np.exp(-rates*.1)*(-np.expm1(-rates*.1)/(rates*.1))**2*(-np.expm1(-rates))**2/rates**2)
        assert response >= -1e-11 and response <= k*budget*qstar+1e-10
        maximum=max(maximum,response/(k*budget*qstar))
        max_budget_ratio=max(max_budget_ratio,response/(budget*qstar))
    rows.append({'states':k,'trials':400,'max_D_over_k_a_qstar':maximum,'max_D_over_a_qstar':max_budget_ratio,'negative_spectral_residue_cases':negative_residue})
result={'root_bracket':[float(lo),float(hi)],'qstar_bounds':[float(qlo),float(qhi)],'alpha_bounds':[float(alpha_lo),float(alpha_hi)],'84_upper':float(F(84,100)*qhi),'required_lower':float(alpha_lo-F(1,20)),'85_lower':float(F(85,100)*qlo),'required_upper':float(alpha_hi-F(1,20)),'threshold_85_certified_by_rational_arithmetic':True,'kernel_height_condition_certified_by_rational_arithmetic':True,'random_checks':rows}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,indent=2), encoding='utf-8')
print(json.dumps(result,indent=2))
