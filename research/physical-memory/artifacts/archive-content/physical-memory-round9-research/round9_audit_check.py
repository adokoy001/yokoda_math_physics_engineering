#!/usr/bin/env python3
"""Independent stdlib-only checks of Round 9. Tests supplement, not replace, proofs."""
from fractions import Fraction as F
from decimal import Decimal, localcontext
import math, random, json
from pathlib import Path

RNG=random.Random(29092026)

def solve(a,b):
    n=len(b); z=[list(a[i])+[b[i]] for i in range(n)]
    for j in range(n):
        q=next(i for i in range(j,n) if z[i][j])
        z[j],z[q]=z[q],z[j]
        d=z[j][j]; z[j]=[x/d for x in z[j]]
        for i in range(n):
            if i!=j:
                d=z[i][j]
                z[i]=[x-d*y for x,y in zip(z[i],z[j])]
    return [z[i][-1] for i in range(n)]

def dot(x,y): return sum((a*b for a,b in zip(x,y)),F(0))
def ck(k): return math.exp(k*math.log(k)-(k-1)-math.lgamma(k))

# Exact rational audit of the physical realization and conditional absorption law.
physical=[]
for k in range(1,10):
    eps=F(1,10)
    Q=[[F(i==j)-eps*F(abs(i-j)==1) for j in range(k)] for i in range(k)]
    u=[F(i==0) for i in range(k)]
    v=[F(i==k-1) for i in range(k)]
    hu=solve(Q,u); hv=solve(Q,v); z=[x+y for x,y in zip(hu,hv)]
    a=dot(u,hv); assert a>0 and min(z)>0 and min(hv)>0
    alpha=[u[i]*hv[i]/a for i in range(k)]
    assert sum(alpha)==1
    T=[[-Q[i][j]*hv[j]/hv[i] for j in range(k)] for i in range(k)]
    for i in range(k):
        assert sum(T[i])==-v[i]/hv[i]
        for j in range(k):
            assert hv[i]**2*T[i][j]==hv[j]**2*T[j][i]
            if i!=j: assert T[i][j]>=0
    C=[x*x for x in z]
    g=[[-Q[i][j]*z[i]*z[j] if i!=j else F(0) for j in range(k)] for i in range(k)]
    left=[z[i]*u[i] for i in range(k)]; right=[z[i]*v[i] for i in range(k)]
    L=[[(-g[i][j] if i!=j else sum(g[i])+left[i]+right[i]) for j in range(k)] for i in range(k)]
    assert all(L[i][j]==z[i]*Q[i][j]*z[j] for i in range(k) for j in range(k))
    kap=dot(left,solve(L,right)); assert kap==a
    assert sum(left)-dot(left,solve(L,left))==a
    assert sum(right)-dot(right,solve(L,right))==a
    Ln=[[x/a for x in row] for row in L]
    ln=[x/a for x in left]; rn=[x/a for x in right]
    assert dot(ln,solve(Ln,rn))==1
    physical.append({'k':k,'static_conductance':str(a),'all_checks_exact':True})

# Stable positive walk series avoids eigendecomposition cancellation in tiny endpoint entries.
def path_constant_ratio(k,eps):
    with localcontext() as ctx:
        ctx.prec=65
        ep=Decimal(eps); t=Decimal(k)
        d0=d1=Decimal(1)
        for n in range(2,k+1): d0,d1=d1,d1-ep*ep*d0
        determinant=d1
        walks=[0]*k; walks[0]=1
        value=Decimal(0); factorial=1
        for n in range(500):
            if n>=k-1:
                term=Decimal(walks[-1])*ep**(n-k+1)*t**n/Decimal(factorial)
                value+=term
                if n>k+30 and term and abs(term)<Decimal('1e-60'): break
            walks=[(walks[i-1] if i else 0)+(walks[i+1] if i+1<k else 0) for i in range(k)]
            factorial*=n+1
        f=determinant*(-t).exp()*value
        c=Decimal(k)**k*Decimal(-(k-1)).exp()/Decimal(math.factorial(k-1))
        ratio=Decimal(1).exp()*Decimal(k)*f/c
        assert ratio<=1+Decimal('1e-50')
        return float(ratio)
path_limits=[]
for k in [2,3,5,8,12]:
    ratios=[path_constant_ratio(k,e) for e in ['0.2','0.1','0.05','0.01','0.001']]
    assert all(x<y for x,y in zip(ratios,ratios[1:]))
    assert ratios[-1]>.9999
    path_limits.append({'k':k,'ratio_to_Ck':ratios})

# Exact rational multi-group Gram estimates. No floating square-root comparisons.
max_loss_ratio=0.; exact_trials=0; nontrivial_sqrt=0
for trial in range(1200):
    p=RNG.randint(2,7); r=RNG.randint(1,5)
    sizes=[RNG.randint(1,5) for _ in range(p)]
    rows=[]
    for _ in range(r):
        row=[]
        for n in sizes:
            scale=F(10)**RNG.randint(-3,3)
            row.append([scale*F(RNG.choice([0,0,0,1,2,3,5]),RNG.choice([1,2,3])) for _ in range(n)])
        rows.append(row)
    W=I=loss=cross=diagloss=F(0)
    for row in rows:
        a=[sum(g,F(0)) for g in row]; m=[max(g) for g in row]
        ws=[a[j]*a[j]-dot(row[j],row[j]) for j in range(p)]
        W+=sum(ws); I+=sum((a[i]-a[j])**2 for i in range(p) for j in range(i))
        loss+=sum(a)**2-sum(m)**2
        cross+=sum(a[i]*a[j]-m[i]*m[j] for i in range(p) for j in range(i))
        diagloss+=sum(dot(g,g)-max(g)**2 for g in row)
    assert 2*diagloss<=W
    residue=cross-(p-1)*W
    if residue>0: assert residue**2<=(p-1)*I*W
    residue=loss-(2*p-F(1,2))*W
    if residue>0:
        nontrivial_sqrt+=1
        assert residue**2<=4*(p-1)*I*W
    if W>0: max_loss_ratio=max(max_loss_ratio,float(loss/W))
    exact_trials+=1

# Equality families prove both coefficients cannot be reduced; numeric trend for the latter.
linear_sharp=[]
for p in range(2,13):
    loss=F(p*p)-(F(p)-F(1,2))**2; W=F(1,2)
    assert loss==(2*p-F(1,2))*W
    linear_sharp.append({'groups':p,'loss_over_W':str(loss/W)})
sqrt_sharp=[]
for p in [2,3,5,10]:
    A=1e9; b=1.; m=100000
    W=b*b*(1-1/m); I=(p-1)*(A-b)**2
    # Factored difference avoids catastrophic cancellation.
    loss=(b-b/m)*(2*(p-1)*A+b+b/m)
    ratio=(loss-(2*p-.5)*W)/math.sqrt(I*W)
    assert ratio<2*math.sqrt(p-1)
    sqrt_sharp.append({'groups':p,'ratio':ratio,'sharp_coefficient':2*math.sqrt(p-1)})

# Ck monotonicity and envelope ratio, using logarithms to avoid overflow.
assert all(ck(k+1)>ck(k) for k in range(1,300))
assert all(ck(k)<=k*(1+1e-12) for k in range(1,300))
worst_log_ratio=-float('inf')
for k in range(2,31):
    for t in [k*(10**(i/100)) for i in range(-300,301)]:
        log_ratio=(k-1)*(math.log(t/k)-(t/k-1))
        worst_log_ratio=max(worst_log_ratio,log_ratio)
        assert log_ratio<=1e-12

out={'status':'PASS','physical_realization_exact':physical,'path_sharpness':path_limits,
     'atomic_exact_fraction_trials':exact_trials,'atomic_trials_requiring_sqrt_term':nontrivial_sqrt,
     'largest_sample_loss_over_W':max_loss_ratio,'linear_sharpness':linear_sharp,
     'sqrt_sharpness':sqrt_sharp,'gamma_envelope_max_log_ratio':worst_log_ratio,
     'limits':'Finite tests do not establish novelty or replace the analytic argument; no general signed-kernel, nonreversible, or Loewner-order extension is tested or claimed.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
