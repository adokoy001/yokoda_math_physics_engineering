"""Exact rational Eq51 primal certificate: tau_cp^sos(H_(2/5)) = 3.

No numerical optimization, no floating-point assertions. PSD constraints
are verified through explicit outer-product decompositions with positive
rational coefficients. All original 36 minor constraints are checked.
"""
from pathlib import Path
from fractions import Fraction as F
import json
import numpy as np

HERE=Path(__file__).resolve().parent
U=np.array([[1,1,1],[1,1,-1],[1,-1,-1],[1,-1,1]],dtype=object)*F(1,2)
W=np.kron(U,U)
g=F(28,5);t=F(3)
A=U@np.diag([g,F(2),F(2)])@U.T
def e(i):
    v=np.zeros((9,1),dtype=object);v[i,0]=1;return v
def outer(v):return v@v.T
p=e(0);q1=e(4);q2=e(8);a=g*p+2*q1+2*q2
Y=outer(a)/3+F(4,3)*outer(q1-q2)
for i,j in [(1,3),(2,6)]:Y+=F(2,3)*g*outer(e(i)+e(j))
X=W@Y@W.T
assert np.array_equal(A.reshape(16,1,order='F'),W@a)
schur=Y-outer(a)/3
schur_sum=F(4,3)*outer(q1-q2)
for i,j in [(1,3),(2,6)]:schur_sum+=F(2,3)*g*outer(e(i)+e(j))
assert all(z==0 for z in (schur-schur_sum).ravel())

# Congruence of a positive outer-product sum proves A tensor A - X PSD.
upper=np.diag(np.kron([g,F(2),F(2)],[g,F(2),F(2)]))
upper_sum=(outer(g*p-2*q1)+outer(g*p-2*q2))/3
for i,j in [(1,3),(2,6)]:
    upper_sum+=g/F(3)*outer(e(i)+e(j))+g*outer(e(i)-e(j))
upper_sum+=4*outer(e(5))+4*outer(e(7))
assert all(z==0 for z in (upper-Y-upper_sum).ravel())

slacks=[]
for i in range(4):
    for j in range(4):
        slack=A[i,j]**2-X[i+4*j,i+4*j]
        assert slack>=0
        slacks.append(slack)
for i in range(4):
    for k in range(i+1,4):
        for j in range(4):
            for l in range(j+1,4):
                assert X[i+4*j,k+4*l]==X[i+4*l,k+4*j]

m=F(7,5);d=F(12,5);z=F(2,5)
assert m*m>z*(2*d-z)
assert m*m<=4*z*(d-z) # Do not claim a counterexample for the old weak test.
result=dict(
    rho='2/5',t='3',A=[[str(x) for x in row] for row in A],
    U=[[str(x) for x in row] for row in U],
    Y=[[str(x) for x in row] for row in Y],
    X=[[str(x) for x in row] for row in X],
    block_psd_by_outer_product_sum=True,
    upper_psd_by_outer_product_sum=True,
    all_36_original_minor_equalities_exact=True,
    diagonal_slack_values=sorted(set(str(x) for x in slacks)),
    strong_certificate_margin=str(m*m-z*(2*d-z)),
    weak_certificate_margin=str(m*m-4*z*(d-z)),
    exact_tau='3: feasible t=3 plus Fawzi-Parrilo ordinary-rank lower bound',
    status='Exact counterexample to inclusion for the strengthened test only; old-test general inclusion remains unresolved.')
(HERE/'round4_sdp_primal_exact.json').write_text(json.dumps(result,indent=2))
print(json.dumps({k:v for k,v in result.items() if k not in ['A','U','Y','X']},indent=2))
