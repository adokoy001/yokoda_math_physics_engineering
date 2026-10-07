"""Exact rational checks for the Fawzi--Parrilo H_rho lower bound.

No SDP solver and no floating-point arithmetic in the assertions below.
The accompanying notes give the proof for all rho >= 0; this file checks
the coefficient identity, a rational dual certificate at rho=1/4, and a
separate explicit feasible CP3 upper comparator for distance to H0.
Requires only Python and numpy (arrays are dtype=object, Fraction entries).
"""
from fractions import Fraction as F
from pathlib import Path
import json
import numpy as np

HERE=Path(__file__).resolve().parent
U=np.array([[1,1,1],[1,1,-1],[1,-1,-1],[1,-1,1]],dtype=object)*F(1,2)
W=np.kron(U,U)
assert np.array_equal(U.T@U,np.eye(3,dtype=object))

def unit(i,n=9):
    e=np.zeros((n,1),dtype=object);e[i,0]=1;return e

def minor_matrix(n,i,k,j,l):
    """trace(E X) = X_(ij,kl) - X_(il,kj), column-major pairs."""
    E=np.zeros((n*n,n*n),dtype=object)
    for a,b,c in [(i+n*j,k+n*l,F(1,2)),(i+n*l,k+n*j,F(-1,2))]:
        E[a,b]+=c;E[b,a]+=c
    return E

# D0 weights directed cycle entries by 1 and directed opposite entries by 2.
D0=np.zeros((16,16),dtype=object)
for i in range(4):
    for j in range(4):
        D0[i+4*j,i+4*j]=0 if i==j else 2 if (i-j)%4==2 else 1
p=unit(0);q=unit(4)+unit(8)
skew=[unit(i)-unit(j) for i,j in [(1,3),(2,6),(5,7)]]
M0=p@p.T+q@q.T+sum((u@u.T for u in skew),np.zeros((9,9),dtype=object))
# The discrepancy consists of three compressed principal-minor equations.
identity=W.T@D0@W-M0+minor_matrix(3,0,1,0,1)+minor_matrix(3,0,2,0,2)+2*minor_matrix(3,1,2,1,2)
assert all(x==0 for x in identity.ravel())

# Explicit rational dual at rho=1/4. The upper-PSD multiplier is zero;
# that constraint is used first to justify exact facial reduction.
rho=F(1,4);g=4+4*rho;C=8*((1+rho)**2+rho**2)
v=(g*p+4*q)/C
k=(g*g+16)/(C*C)
M=k*M0
w=4*p-g*q
# Block dual [[1,-v^T],[-v,M]] is PSD from this explicit outer-product sum.
res=M-v@v.T-(w@w.T)/(C*C)-k*sum((u@u.T for u in skew),np.zeros((9,9),dtype=object))
assert all(x==0 for x in res.ravel())

# Multipliers for Eq51 minor equations, in exactly the loop order below.
mult=[3,1,-2,2,-1,1,1,2,1,1,0,-1,-2,1,3,-1,1,-2,
      2,1,-1,3,1,2,-1,0,1,1,2,1,1,-1,-2,2,1,3]
stationarity=W.T@(k*D0)@W-M
z=0
for i in range(4):
    for kk in range(i+1,4):
        for j in range(4):
            for l in range(j+1,4):
                stationarity+=(k*F(mult[z],4))*(W.T@minor_matrix(4,i,kk,j,l)@W)
                z+=1
assert all(x==0 for x in stationarity.ravel())
a=g*p+2*q
dual_value=2*(v.T@a)[0,0]-k*C
assert dual_value==F(41,13)>3

results=dict(
    coefficient_identity_exact=True,
    dual_stationarity_exact=True,
    dual_psd_by_explicit_outer_product_sum=True,
    rho=str(rho),
    proved_lower_bound=str(dual_value),
    general_proved_lower_bound='max(3,(4+4*rho+2*rho**2)/(1+2*rho+2*rho**2)) for rho>=0',
    general_equality_to_SDP_optimum_proven=False,
    original_minor_multipliers_in_units_k_over_4=mult)

# Existing local fit, rounded to an exact decimal nonnegative factor.
G=[['1.22610739','0','0','0.97599645'],
   ['0.54770813','1.46670004','0.35908992','0'],
   ['0','0.21323097','1.29740221','0.92236352']]
Gr=np.array([[F(x) for x in row] for row in G],dtype=object)
H0=np.array([[2,1,0,1],[1,2,1,0],[0,1,2,1],[1,0,1,2]],dtype=object)
error=max(abs(x) for x in (Gr.T@Gr-H0).ravel())
assert error==F(196676472519291,10**15)<F('0.19667648')
results['explicit_cp3_upper_factor_decimal']=G
results['explicit_cp3_upper_error_exact']=str(error)
results['explicit_cp3_upper_is_global_optimum']=False
(HERE/'round3_sdp_exact_certificate.json').write_text(json.dumps(results,indent=2))
print(json.dumps(results,indent=2))
