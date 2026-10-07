"""Independent floating-point checks; analytic statements are in round10_spectral.md."""
import json, math
from pathlib import Path
import numpy as np
from scipy.linalg import expm
from scipy.integrate import quad
from scipy.stats import gamma

report = {'scope': 'numerical corroboration, not a replacement for proof', 'path_checks': [], 'rectangle_band_example': {}, 'two_state_checks': []}
for j in (2,3,5,8,12):
    A = np.diag(np.ones(j-1), 1) + np.diag(np.ones(j-1), -1)
    beta = 2*math.cos(math.pi/(j+1))
    for eps in (.03,.1,.3):
        rho=1.2; kappa=.7
        M=np.eye(j)-eps*A; Q=rho*M
        s=np.zeros(j); s[[0,j-1]]=1
        a=np.linalg.inv(Q)[0,j-1]
        z=np.linalg.solve(Q,s)
        D=np.linalg.det(M)
        da=eps**(j-1)/(rho*D)
        actual_capacity=kappa*np.dot(z,z)/a
        ds=[1.,1.]
        for n in range(2,j+1): ds.append(ds[-1]-eps**2*ds[-2])
        y=np.array([(eps**i*ds[j-i-1]+eps**(j-1-i)*ds[i])/ds[j] for i in range(j)])
        formula_capacity=kappa*ds[j]*np.dot(y,y)/(rho*eps**(j-1))
        coeff=[]; walk=np.eye(j)
        for n in range(j-1+101):
            if n>=j-1 and (n-(j-1))%2==0: coeff.append((n+1,ds[j]*eps**(n-(j-1))*walk[0,j-1]))
            walk=walk@A
        mass=sum(v for _,v in coeff)
        def fmix(t): return sum(v*gamma.pdf(t,a=n,scale=1/rho) for n,v in coeff)
        tv=.5*quad(lambda t: abs(fmix(t)-gamma.pdf(t,a=j,scale=1/rho)),0,np.inf,epsabs=1e-9,limit=250)[0]
        max_density_error=max(abs(expm(-Q*t)[0,j-1]/a-fmix(t)) for t in (.1,1,j/rho,2*j/rho))
        assert abs(a-da)<=1e-10*abs(a)
        assert abs(actual_capacity-formula_capacity)<=1e-10*actual_capacity
        assert abs(mass-1)<1e-12
        assert tv<=1-D+1e-8
        assert 1-D<=(j-1)*eps**2+1e-8
        assert max_density_error<1e-8
        report['path_checks'].append({'j':j,'epsilon':eps,'TV':tv,'mixture_certificate':1-D,'simple_certificate':(j-1)*eps**2,'capacity':actual_capacity,'capacity_relative_formula_error':abs(actual_capacity-formula_capacity)/actual_capacity,'density_max_error':max_density_error})

L,U=.8,1.2; left,right=.9,1.1
rows=[]
for j in range(1,16):
    rho=min(U,max(L,j*math.log(right/left)/(right-left)))
    q=gamma.cdf(right,a=j,scale=1/rho)-gamma.cdf(left,a=j,scale=1/rho)
    grid=np.linspace(L,U,1001)
    gridmax=max(gamma.cdf(right,a=j,scale=1/grid)-gamma.cdf(left,a=j,scale=1/grid))
    assert q+1e-14>=gridmax
    rows.append({'shape':j,'optimal_rate':rho,'interval_probability':q})
J=math.ceil(U*right)
assert J==2
assert max(x['interval_probability'] for x in rows)==max(x['interval_probability'] for x in rows[:J])
report['rectangle_band_example']={'band':[L,U],'window':[left,right],'saturation_states':J,'rows':rows}

for eps in (.01,.05,.2,.5):
    rho=1.0; kappa=1.0
    Ctot=2*kappa*(1+eps)/(rho*eps*(1-eps))
    worst=0.
    for x in np.linspace(0,30,601):
        Fc=1-((1+eps)*math.exp(-(1-eps)*x)-(1-eps)*math.exp(-(1+eps)*x))/(2*eps)
        Fg=1-math.exp(-x)*(1+x)
        worst=max(worst,Fg-Fc)
        assert -1e-13<=Fg-Fc<=eps*eps+1e-13
    report['two_state_checks'].append({'epsilon':eps,'capacity':Ctot,'CDF_max_error_grid':worst,'CDF_certificate':eps*eps})
report['status']='PASS'
Path(__file__).with_suffix('.json').write_text(json.dumps(report,indent=2))
print(json.dumps({'status':report['status'],'path_checks':len(report['path_checks']),'band_saturation':J,'band_optimum':rows[1],'two_state_checks':report['two_state_checks']},indent=2))
