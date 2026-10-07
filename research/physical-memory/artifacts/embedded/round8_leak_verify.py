import json
from pathlib import Path
import numpy as np
rng=np.random.default_rng(829)

def check(F,n,theta=1.0):
    D=F.T@F; m=F.shape[1]-n; r=F.shape[0]
    S=D[:n,n:].sum(); AU=D[:n,:n].sum(); AV=D[n:,n:].sum()
    WU=D[:n,:n].sum()-np.trace(D[:n,:n]); WV=D[n:,n:].sum()-np.trace(D[n:,n:])
    # Explicit nonnegative sums avoid cancellation for sparse limiting tests.
    WU=sum(D[i,j] for i in range(n) for j in range(n) if i!=j)
    WV=sum(D[i,j] for i in range(n,n+m) for j in range(n,n+m) if i!=j)
    W=theta*WU+WV/theta
    a=np.sqrt(theta)*F[:,:n].sum(axis=1); b=F[:,n:].sum(axis=1)/np.sqrt(theta)
    I=np.square(a-b).sum()
    B=np.sort(D[:n,n:].ravel())[::-1][:r].sum()
    rhs=B+W+np.sqrt(I*W)
    error=(S-rhs)/max(1,S)
    assert error<2e-12,(F,n,theta,error)
    old=np.sqrt(np.trace(D[:n,:n])*WV)+np.sqrt(np.trace(D[n:,n:])*WU)+np.sqrt(WU*WV)
    return {'S':float(S),'B_r':float(B),'W':float(W),'I':float(I),'new_penalty':float(W+np.sqrt(I*W)),'old_penalty':float(old),'relative_violation':float(error)}

maxviol=-1.;count=0
for trial in range(5000):
    n=int(rng.integers(1,10));m=int(rng.integers(1,10));r=int(rng.integers(1,15))
    F=np.exp(rng.uniform(-7,7,(r,n+m)))*(rng.random((r,n+m))<rng.uniform(.05,1))
    theta=float(np.exp(rng.uniform(-7,7)))
    x=check(F,n,theta);maxviol=max(maxviol,x['relative_violation']);count+=1

sharp=[]
for n in [2,3,5,10,20]:
    # n factors; U is coordinate-aligned, V is uniform. Every row is balanced.
    F=np.column_stack((np.eye(n),np.ones((n,n))/n))
    x=check(F,n);x['n']=n;assert abs(x['S']-x['B_r']-x['W'])<1e-10
    sharp.append(x)

physical=[]
for n in [2,3,5,10]:
    lam=.7;c0=1.3;h=.9;t=.2
    F=np.column_stack((np.sqrt(c0)*np.eye(n),np.sqrt(c0)*np.ones((n,n))/n))
    v=F.sum(axis=1);C=np.diag(v*v);g=lam*v[:,None]*F
    LII=np.diag(g.sum(axis=1));LBB=np.diag(g.sum(axis=0));LIB=-g
    K=LBB-LIB.T@np.linalg.solve(LII,LIB)
    H=F.T@F
    Htarget=c0*np.block([[np.eye(n),np.ones((n,n))/n],[np.ones((n,n))/n,np.eye(n)]])
    Ktarget=lam*c0*np.block([[np.eye(n),-np.ones((n,n))/n],[-np.ones((n,n))/n,np.eye(n)]])
    max_cross=0.
    for omega in [0,.1,.7,2,100]:
        s=1j*omega
        Y=LBB-LIB.T@np.linalg.solve(s*C+LII,LIB)
        Ytar=Ktarget+s*lam/(s+lam)*Htarget
        max_cross=max(max_cross,float(np.max(np.abs(Y[:n,n:]-Ytar[:n,n:]))))
    assert max_cross<1e-12
    kV=-K[n:,n:]+np.diag(np.diag(K[n:,n:]))
    assert np.max(np.abs(kV-(np.ones((n,n))-np.eye(n))*lam*c0/n))<1e-12
    physical.append({'n':n,'r':n,'cross_transfer_max_error':max_cross,'within_V_steady_leak':float(lam*c0/n),'total_capacity':float(np.trace(C))})

out={'cases':count,'max_relative_violation':maxviol,'sharp_family':sharp,'physical_family':physical,'interpretation':'Finite checks support implementation; analytic proof is primary. Not a novelty certificate.'}
Path(__file__).with_suffix('.json').write_text(json.dumps(out,indent=2))
print(json.dumps(out,indent=2))
