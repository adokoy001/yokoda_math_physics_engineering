"""Independent numeric audit of fixed-variance W2 minimax representatives.
Python 3 + NumPy + SciPy.  No optimization/search is treated as a proof.
"""
import json, math
from pathlib import Path
import numpy as np
from scipy.integrate import quad

SEED=20261006
rng=np.random.default_rng(SEED)
worst={}
counts={}
def record(k,val):
    worst[k]=max(worst.get(k,0.0),float(abs(val)))
def inc(k,n=1): counts[k]=counts.get(k,0)+n

def pars(mu,v):
    M=mu*(1-mu); k=2/(2+math.log(M/v))
    return k,v/(mu*mu+v),(1-mu)**2/((1-mu)**2+v)
def hp(u,mu,v):
    k,a,b=pars(mu,v)
    if u<a:return mu
    if u>b:return -(1-mu)
    return math.sqrt(v)*(1-2*u)/(2*math.sqrt(u*(1-u)))
def qw(u,mu,v,w):return mu-math.sqrt(pars(mu,v)[0]*w/v)*hp(u,mu,v)
def integrate(fun,breaks):
    bs=sorted(set([0.,1.]+[float(z) for z in breaks if 0<z<1]))
    # Almost coincident analytically identical cuts differ at machine precision.
    # Midpoint integration of these tiny intervals avoids QUADPACK roundoff warnings.
    return sum((r-l)*fun((l+r)/2) if r-l<1e-13 else
               quad(fun,l,r,epsabs=3e-13,epsrel=3e-12,limit=150)[0]
               for l,r in zip(bs[:-1],bs[1:]))
def atoms(x,p):
    order=np.argsort(x);x=np.asarray(x)[order];p=np.asarray(p)[order];p=p/p.sum()
    mask=p>1e-15;x=x[mask];p=p[mask];p=p/p.sum()
    cp=np.cumsum(p);cp[-1]=1.
    return x,p,cp

def two(mu,v,p):
    return atoms([mu-math.sqrt(v*(1-p)/p),mu+math.sqrt(v*p/(1-p))],[p,1-p])
def three(mu,v,c):
    D=mu*(1-mu)-v
    return atoms([0,c,1],[1-mu-D/c,D/(c*(1-c)),mu-D/(1-c)])
def at(u,dist):
    x,p,cp=dist;return x[min(np.searchsorted(cp,u,side='right'),len(x)-1)]
def dist_to_opt(dist,mu,v,w):
    k,a,b=pars(mu,v)
    return integrate(lambda u:(at(u,dist)-qw(u,mu,v,w))**2,[a,b,*dist[2]])
def steploss(d1,d2):
    bs=sorted(set([0.,1.,*d1[2],*d2[2]]))
    return sum((r-l)*(at((l+r)/2,d1)-at((l+r)/2,d2))**2 for l,r in zip(bs[:-1],bs[1:]))

cases=[(mu,mu*(1-mu)*s) for mu in (.08,.3,.5,.91) for s in (.02,.4,.93)]
for mu,v in cases:
    k,a,b=pars(mu,v)
    for w in (.15*v,k*v,v,v/k,1.4*v/k):
        R=v+w-2*math.sqrt(k*v*w)
        alpha=math.sqrt(k*w/v)
        m=integrate(lambda u:qw(u,mu,v,w),[a,b])
        var=integrate(lambda u:(qw(u,mu,v,w)-mu)**2,[a,b])
        record('mean_absolute_error',m-mu);record('variance_absolute_error',var-w)
        inc('moment_checks')
        cmin=(mu*(1-mu)-v)/(1-mu)
        cmax=1-(mu*(1-mu)-v)/mu
        for p in np.linspace(a,b,9):
            record('two_point_equality_absolute_error',dist_to_opt(two(mu,v,p),mu,v,w)-R)
            inc('two_point_equality_checks')
        for c in np.linspace(cmin,cmax,9):
            record('three_point_equality_absolute_error',dist_to_opt(three(mu,v,c),mu,v,w)-R)
            inc('three_point_equality_checks')
        supportlo=mu*(1-alpha);supporthi=mu+alpha*(1-mu)
        assert ((supportlo>=-1e-12 and supporthi<=1+1e-12)==(w<=v/k+1e-12))
        inc('support_threshold_checks')

# Every random input is assessed against its own exact first two moments.
min_slack=math.inf
for j in range(100):
    x=np.sort(rng.uniform(0,1,int(rng.integers(4,11))))
    p=rng.dirichlet(np.ones(len(x)))
    dist=atoms(x,p);mu=float(p@x);v=float(p@((x-mu)**2));k,a,b=pars(mu,v)
    for w in (.25*v,v,v/k,1.5*v/k):
        R=v+w-2*math.sqrt(k*v*w)
        d=dist_to_opt(dist,mu,v,w)
        min_slack=min(min_slack,R-d)
        assert d<=R+2e-10
        inc('random_input_upper_bound_checks')

# Independently integrate the least-favorable two-point measure nu.
# Test arbitrary monotone finite quantiles with specified mean and variance.
min_cs_slack=math.inf
for mu,v in cases:
    k,a,b=pars(mu,v)
    w=v
    x=np.sort(rng.normal(size=7));p=rng.dirichlet(np.ones(7))
    x=x-p@x;x*=math.sqrt(w/(p@(x*x)));x+=mu
    q=atoms(x,p)
    boundary=(k/2)*(steploss(two(mu,v,a),q)+steploss(two(mu,v,b),q))
    breaks=sorted(set([a,b]+[float(t) for t in q[2] if a<t<b]))
    middle=sum(quad(lambda t:steploss(two(mu,v,t),q)*k/(4*t*(1-t)),l,r,
                    epsabs=2e-12,epsrel=2e-11,limit=150)[0] for l,r in zip(breaks[:-1],breaks[1:]))
    meanloss=boundary+middle
    R=v+w-2*math.sqrt(k*v*w)
    d=dist_to_opt(q,mu,v,w)
    target=R+math.sqrt(k*v/w)*d
    record('least_favorable_stability_identity_error',meanloss-target)
    min_cs_slack=min(min_cs_slack,meanloss-R)
    inc('arbitrary_representative_stability_checks')

assert max(worst.values())<2e-10,worst
out={'seed':SEED,'method':'piecewise adaptive quadrature; exact step-quantile distances; independently integrated witness measure',
     'counts':counts,'max_absolute_errors':worst,'minimum_random_upper_bound_slack':min_slack,
     'minimum_arbitrary_representative_stability_slack':min_cs_slack,
     'limitations':['Finite numerical checks are not a proof.', 'Random inputs each use their own moments, not one common class.',
       'Fixed-support high-variance regime w>v/kappa is not claimed solved.']}
path=Path(__file__).with_name('w2_validation_results.json');path.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps(out,indent=2))
