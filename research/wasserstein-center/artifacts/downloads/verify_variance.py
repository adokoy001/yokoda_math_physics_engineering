"""Reproducible checks for the fixed-mean, fixed-variance W2 center.

This is NOT a formal proof. Rational moment/envelope/equality checks are exact.
Logarithms and square roots use Decimal at 60 digits. Independent direct
quadrature and barycenter checks use SciPy double precision.

Run: python3 verify_variance.py
Dependencies: Python standard library and scipy (for independent quadrature).
"""
from fractions import Fraction as F
from decimal import Decimal as D, localcontext
from functools import lru_cache
from pathlib import Path
import json
import math
import random
import time
from scipy.integrate import quad

PRECISION = 60
TOL = D('1e-52')

def dec(x):
    if isinstance(x,F): return D(x.numerator)/D(x.denominator)
    return D(x)

def compositions(n,k):
    if k==1:
        yield (n,)
    else:
        for i in range(n+1):
            for rest in compositions(n-i,k-1): yield (i,)+rest

def clean(law):
    masses={}
    for x,w in law:
        if w: masses[x]=masses.get(x,F(0))+w
    return sorted(masses.items())

def moments(law):
    mu=sum(x*w for x,w in law)
    v=sum(w*(x-mu)**2 for x,w in law)
    return mu,v

@lru_cache(None)
def parameters(mu,v):
    M=mu*(1-mu)
    if v==0:return D(0),D(0),D(0)
    L=(dec(M)/dec(v)).ln()
    k=D(2)/(D(2)+L)
    return L,k,dec(v)*(1-k)

def envelope(p,mu,v):
    return min(dec(mu*p),dec((1-mu)*(1-p)),dec(v*p*(1-p)).sqrt())

def check_law(law,counts):
    law=clean(law)
    assert sum(w for x,w in law)==1
    mu,v=moments(law);M=mu*(1-mu)
    assert 0<=mu<=1 and 0<=v<=M
    counts['laws']+=1
    counts['asymmetric_mean']+=int(mu!=F(1,2))
    if v==0:
        assert len(law)==1
        counts['zero_variance']+=1
        return
    if v==M:
        assert all(x in (0,1) for x,w in law)
        counts['maximum_variance']+=1
        return
    L,k,r2=parameters(mu,v)
    cumulative=F(0);prefix_moment=F(0);variance_identity=F(0)
    h_integral=D(0);all_contacts=True
    for i,(x,w) in enumerate(law[:-1]):
        cumulative+=w;prefix_moment+=x*w
        p=cumulative;A=mu*p-prefix_moment;dx=law[i+1][0]-x
        # Each of these is an exact rational comparison, including Cauchy.
        assert A>=0 and A<=mu*p and A<=(1-mu)*(1-p)
        assert A*A<=v*p*(1-p)
        variance_identity+=A*dx
        contact=(A==mu*p or A==(1-mu)*(1-p) or A*A==v*p*(1-p))
        all_contacts &= contact
        h_integral+=envelope(p,mu,v)*dec(dx)
        counts['exact_envelope_cut_checks']+=1
    assert variance_identity==v
    classified=(len(law)<=2 or (len(law)==3 and law[0][0]==0 and law[-1][0]==1))
    assert all_contacts==classified
    distance2=dec(v)*(1+k)-2*k*h_integral
    assert distance2>=-TOL and distance2<=r2+TOL
    if classified:
        assert abs(distance2-r2)<TOL
        counts['equality_laws']+=1
    else:
        assert distance2<r2
        counts['strict_laws']+=1
    shrink_radius2=dec(v*(1-v/M))
    assert r2 < shrink_radius2

def qcenter(u,mu,v):
    M=mu*(1-mu)
    if v==0:return mu
    if v==M:return 0. if u<1-mu else 1.
    L=math.log(M/v);k=2/(2+L)
    a=v/(mu*mu+v);b=(1-mu)**2/((1-mu)**2+v)
    if u<a:return mu*(1-k)
    if u>b:return mu+k*(1-mu)
    return mu+k*math.sqrt(v)*(2*u-1)/(2*math.sqrt(u*(1-u)))

def direct_quadrature(law):
    law=clean(law);muq,vq=moments(law);mu=float(muq);v=float(vq)
    if not 0<v<mu*(1-mu):return None
    a=v/(mu*mu+v);b=(1-mu)**2/((1-mu)**2+v)
    breaks=sorted(set([0.,a,b,1.]+[float(sum(w for x,w in law[:i])) for i in range(1,len(law))]))
    def quantile(u):
        cumulative=0.
        for x,w in law:
            cumulative+=float(w)
            if u<cumulative:return float(x)
        return float(law[-1][0])
    value=mean=variance=0.
    for lo,hi in zip(breaks,breaks[1:]):
        x=quantile((lo+hi)/2)
        value+=quad(lambda u:(x-qcenter(u,mu,v))**2,lo,hi,epsabs=1e-13,epsrel=1e-13)[0]
        mean+=quad(lambda u:qcenter(u,mu,v),lo,hi,epsabs=1e-13,epsrel=1e-13)[0]
        variance+=quad(lambda u:(qcenter(u,mu,v)-mu)**2,lo,hi,epsabs=1e-13,epsrel=1e-13)[0]
    L,k,r2=parameters(muq,vq);ip=D(0);p=F(0)
    for i,(x,w) in enumerate(law[:-1]):
        p+=w;ip+=envelope(p,muq,vq)*dec(law[i+1][0]-x)
    formula=dec(vq)*(1+k)-2*k*ip
    assert abs(value-float(formula))<2e-11
    assert abs(mean-mu)<2e-11
    assert abs(variance-float(k*dec(vq)))<2e-11
    return dict(mu=str(muq),variance=str(vq),distance2_direct=value,
        distance2_formula=str(formula),absolute_error=abs(value-float(formula)))

def barycenter_check(mu,v):
    """Integrate a mixture of TWO-POINT INPUT quantiles, independently of H."""
    L=math.log(mu*(1-mu)/v);den=L+2
    ya=math.log(v/(mu*mu));yb=math.log((1-mu)**2/v)
    def binary(y,u):
        p=1/(1+math.exp(-y))
        return mu-math.sqrt(v)*math.exp(-y/2) if u<p else mu+math.sqrt(v)*math.exp(y/2)
    max_error=0.
    for u in [.0001,.01,.1,.27,.5,.73,.9,.99,.9999]:
        z=math.log(u/(1-u));cuts=sorted(set([ya,yb]+([z] if ya<z<yb else [])))
        integral=sum(quad(lambda y:binary(y,u),lo,hi,epsabs=1e-13,epsrel=1e-13)[0] for lo,hi in zip(cuts,cuts[1:]))
        mixture=(binary(ya,u)+binary(yb,u)+integral/2)/den
        err=abs(mixture-qcenter(u,mu,v));max_error=max(max_error,err)
        assert err<2e-11
    return dict(mu=mu,variance=v,max_absolute_error=max_error)

def run():
    start=time.perf_counter()
    counts={k:0 for k in ['laws','asymmetric_mean','zero_variance','maximum_variance',
        'exact_envelope_cut_checks','equality_laws','strict_laws']}
    grid=8
    for ns in compositions(grid,grid+1):
        check_law([(F(i,grid),F(n,grid)) for i,n in enumerate(ns)],counts)
    grid_count=counts['laws']
    rng=random.Random(20260907)
    random_laws=[]
    for j in range(2000):
        xs=sorted(rng.sample(range(38),rng.randint(1,8)))
        weights=[rng.randint(1,31) for x in xs];s=sum(weights)
        law=[(F(x,37),F(w,s)) for x,w in zip(xs,weights)]
        check_law(law,counts)
        if j<8 and len(law)>1:random_laws.append(law)
    direct=[];bary=[]
    for mu in [F(1,8),F(1,3),F(1,2),F(3,4)]:
        M=mu*(1-mu)
        for fraction in [F(1,8),F(1,2),F(7,8)]:
            v=M*fraction;upper=mu+v/mu;upper_mass=mu/upper
            binary=[(F(0),1-upper_mass),(upper,upper_mass)]
            triple=[(F(0),v/mu),(mu,1-v/M),(F(1),v/(1-mu))]
            direct.extend([direct_quadrature(binary),direct_quadrature(triple)])
            bary.append(barycenter_check(float(mu),float(v)))
    direct.extend(direct_quadrature(p) for p in random_laws)
    limits=[]
    for mu in [F(1,10**12),F(1,3),1-F(1,10**12)]:
        M=mu*(1-mu)
        for f in [F(1,10**40),1-F(1,10**40)]:
            v=M*f;L,k,r2=parameters(mu,v)
            assert 0<k<1 and 0<r2<dec(v)
            limits.append(dict(mu=str(mu),variance_fraction=str(f),radius2=str(r2)))
    comparison=[]
    for v in [F(1,16),F(1,8),F(3,16)]:
        L,k,r2=parameters(F(1,2),v)
        comparison.append(dict(mean='1/2',variance=str(v),optimal_radius2=str(r2),
            optimal_radius=str(r2.sqrt()),shrunken_binary_radius2=str(dec(v*(1-4*v)))))
    result=dict(status='PASS',arithmetic={'exact':'fractions.Fraction',
        'high_precision':'decimal.Decimal','decimal_digits':PRECISION,
        'high_precision_absolute_tolerance':str(TOL),
        'independent_quadrature':'scipy.integrate.quad (double precision)',
        'quadrature_absolute_tolerance':2e-11},
        scope='Finite computational evidence; not a proof or a machine-checked theorem.',
        counts=counts,grid={'locations_denominator':8,'mass_denominator':8,'laws':grid_count},
        random={'seed':20260907,'laws':2000,'locations_denominator':37},
        direct_quantile_quadrature=direct,barycenter_mixture_checks=bary,
        near_degenerate_parameters=limits,comparison=comparison,
        elapsed_seconds=time.perf_counter()-start)
    path=Path(__file__).with_name('variance_results.json')
    path.write_text(json.dumps(result,indent=2)+'\n')
    print(json.dumps({k:result[k] for k in ['status','counts','elapsed_seconds']},indent=2))
    print('Direct quadrature cases:',len(direct))
    print('Independent barycenter cases:',len(bary))
    print('Wrote',path)

if __name__=='__main__':
    with localcontext() as ctx:
        ctx.prec=PRECISION
        run()
