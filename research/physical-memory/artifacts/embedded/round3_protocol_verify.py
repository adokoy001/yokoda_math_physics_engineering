"""Verify self-convolution heating and the improved CP3 certificate.
No external datasets. NumPy + SciPy; fixed random seed. Numerical checks
support implementation only; exact proofs are in the accompanying HTML.
"""
from pathlib import Path
import json
import numpy as np
from numpy.polynomial.legendre import leggauss
from scipy.linalg import expm
from scipy.optimize import brentq

HERE=Path(__file__).resolve().parent
rng=np.random.default_rng(202609203)
gx,gw=leggauss(28)
def quad(a,b):return (a+b)/2+(b-a)*gx/2,(b-a)*gw/2
def mf(V,values):return (V*values)@V.T
def triangular_rate(t,T):return np.where(t<T,t,2*T-t)/T**2

err_ramp=err_power=err_gram=err_heatrows=0.; min_factor=1.
for r in range(1,13):
    for rep in range(4):
        n=5
        w=rng.uniform(0,.5,(r,r));w=(w+w.T)/2;np.fill_diagonal(w,0)
        B=rng.uniform(.05,.7,(r,n))
        Q=np.diag(w.sum(1)+B.sum(1))-w
        direct=rng.uniform(0,.5,(n,n));direct=(direct+direct.T)/2;np.fill_diagonal(direct,0)
        direct=np.diag(direct.sum(1))-direct
        Lbb=direct+np.diag(B.sum(0));K=Lbb-B.T@np.linalg.solve(Q,B)
        err_heatrows=max(err_heatrows,float(np.max(abs(K.sum(1)))))
        ev,V=np.linalg.eigh(Q)
        T=float(rng.uniform(.1,.7));h=float(rng.uniform(.1,.9));tau=float(rng.uniform(.05,.8))
        tm1,wm1=quad(0,T);tm2,wm2=quad(T,2*T)
        ts=np.r_[tm1,tm2];mu=np.r_[wm1,wm2]*triangular_rate(ts,T)
        win1,ww=quad(2*T+tau,2*T+tau+h)
        win2,_=quad(2*T+tau+h,2*T+tau+2*h)
        def residual(t):
            spectral=np.sum(mu[:,None]*np.exp(-(t-ts[:,None])*ev[None,:]),axis=0)/ev
            return B.T@mf(V,spectral)@B
        D=sum(weight*((K+residual(a))-(K+residual(b))) for weight,a,b in zip(ww,win1,win2))
        Ah=mf(V,-np.expm1(-ev*h)/ev);AT=mf(V,-np.expm1(-ev*T)/(ev*T))
        F=expm(-Q*tau/2)@AT@Ah@B
        target=B.T@mf(V,np.exp(-ev*tau)*(-np.expm1(-ev*T)/(ev*T))**2*(-np.expm1(-ev*h)/ev)**2)@B
        err_ramp=max(err_ramp,float(np.max(abs(D-target))))
        err_gram=max(err_gram,float(np.max(abs(F.T@F-target))))
        min_factor=min(min_factor,float(F.min()))
        # The same Q is a grounded conductance matrix for a power-driven system.
        # B is now an overlapping nonnegative spatial input, with matched B.T readout.
        Kp=B.T@np.linalg.solve(Q,B)
        Dp=sum(weight*((Kp-residual(b))-(Kp-residual(a))) for weight,a,b in zip(ww,win1,win2))
        err_power=max(err_power,float(np.max(abs(Dp-target))))

def bound(d,z):
    zz=min(z,d/2)
    return 4*zz*(d-zz)
violations=0;worst=-float('inf')
for _ in range(3000):
    F=rng.exponential(1,(3,4));F[rng.random((3,4))<.3]=0
    H=F.T@F;m=min(H[0,1],H[1,2],H[2,3],H[3,0]);z=max(H[0,2],H[1,3]);d=max(H.diagonal())
    margin=m*m-bound(d,z)
    worst=max(worst,float(margin))
    violations+=margin>1e-10
assert not violations
delta=5-2*np.sqrt(6)
lam=.25;total_rise=1.;T=total_rise/2;tau=.1
x=brentq(lambda x:np.exp(x)-2*x-1,.1,3);h=x/lam
linear_a=np.exp(-lam*tau)*(-np.expm1(-lam*total_rise)/(lam*total_rise))*(-np.expm1(-lam*h))**2
smooth_a=np.exp(-lam*tau)*(-np.expm1(-lam*T)/(lam*T))**2*(-np.expm1(-lam*h))**2
result=dict(seed=202609203,physical_graphs=48,hidden_counts=list(range(1,13)),
            max_triangular_ramp_window_error=err_ramp,max_gram_error=err_gram,
            min_factor_entry=min_factor,max_power_input_window_error=err_power,
            max_kron_rowsum_error=err_heatrows,cp3_factor_checks=3000,
            cp3_inequality_violations=int(violations),max_cp3_inequality_margin=worst,
            improved_delta=delta,uniform_rho_threshold=3-2*np.sqrt(2),
            design=dict(lam=lam,total_rise=total_rise,tau=tau,h=h,
                linear_ramp_coefficient=linear_a,linear_ramp_error_floor=delta*linear_a/(2*h),
                quadratic_ramp_coefficient=smooth_a,quadratic_ramp_error_floor=delta*smooth_a/(2*h)),
            scope='Synthetic numerical checks; no experimental measurement or optimality claim.')
assert max(err_ramp,err_gram,err_power,err_heatrows)<1e-10
(HERE/'round3-protocol-results.json').write_text(json.dumps(result,indent=2))
print(json.dumps(result,indent=2))
