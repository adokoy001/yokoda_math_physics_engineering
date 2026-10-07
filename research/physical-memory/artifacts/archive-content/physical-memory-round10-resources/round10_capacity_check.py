"""Numerical cross-checks for analytically proved finite-capacity statements.
Not a proof; scipy/numpy are used solely for independent matrix calculations.
"""
import json
import math
from pathlib import Path
import numpy as np
from scipy.linalg import eigh

rng = np.random.default_rng(20261003)
worst = dict(moment_identity=0., spectral_identity=0., window_bound_ratio=0.,
             point_bound_ratio=0., tail_bound_ratio=0., residue_bound_ratio=0.)
for trial in range(300):
    n = int(rng.integers(1, 15))
    cap = np.exp(rng.uniform(-2, 2, n))
    left = rng.uniform(0, 2, n)
    right = rng.uniform(0, 2, n)
    edges = rng.uniform(0, 2, (n,n))
    edges = np.triu(edges * (rng.uniform(0,1,(n,n)) < .2), 1)
    edges += edges.T
    L = np.diag(edges.sum(axis=1)+left+right)-edges
    Q = L / np.sqrt(np.outer(cap,cap))
    lam, U = eigh(Q)
    u = left/np.sqrt(cap); v=right/np.sqrt(cap)
    r = (U.T@u)*(U.T@v)
    a = np.sum(r/lam)
    M = np.sum(r/lam**2)
    p = np.linalg.solve(L,left)
    delta = np.sum(cap*(2*p-1)**2)
    total = sum(cap)
    worst['moment_identity'] = max(worst['moment_identity'], abs(M-np.sum(cap*p*(1-p)))/max(1,abs(M)))
    worst['spectral_identity'] = max(worst['spectral_identity'], abs(total-4*M-delta)/max(1,total))
    worst['residue_bound_ratio'] = max(worst['residue_bound_ratio'], 4*np.sum(np.maximum(r,0)/lam**2)/total)
    for t in [.1, 1, 10]:
        h = np.sum(r*np.exp(-lam*t))
        tail = np.sum(r*np.exp(-lam*t)/lam)
        worst['point_bound_ratio'] = max(worst['point_bound_ratio'], h*math.e**2*t*t/total)
        worst['tail_bound_ratio'] = max(worst['tail_bound_ratio'], tail*4*math.e*t/total)
    q = np.exp(-.9*lam)-np.exp(-1.1*lam)
    D = np.sum(r*q/lam)
    B_w = .10899633216645743
    worst['window_bound_ratio'] = max(worst['window_bound_ratio'], 4*D/(total*B_w))

# A positive finite one-state network attaining the exact total-budget optimum.
lo, hi = 2/1.1, 2/.9
for _ in range(90):
    rate = (lo+hi)/2
    der = (1-.9*rate)*math.exp(-.9*rate)-(1-1.1*rate)*math.exp(-1.1*rate)
    if der > 0: lo=rate
    else: hi=rate
rate=(lo+hi)/2
budget=1.; kappa=1.
star_g=budget*rate/2
dynamic_a=budget*rate/4
direct=kappa-dynamic_a
q=math.exp(-.9*rate)-math.exp(-1.1*rate)
D=dynamic_a*q
assert direct>0
assert worst['moment_identity']<1e-11
assert worst['spectral_identity']<1e-11
assert all(worst[k]<=1+1e-10 for k in ['window_bound_ratio','point_bound_ratio','tail_bound_ratio','residue_bound_ratio'])
max_two_pole_error=0.
for _ in range(100):
    alpha=math.exp(rng.uniform(-1,1)); beta=alpha+math.exp(rng.uniform(-1,1))
    A=math.exp(rng.uniform(-1,1)); B0=A*rng.uniform(.01,1)
    cap=np.array([2*A/alpha**2]*2)
    g=A*(beta-alpha)/alpha**2
    left=np.array([(A+math.sqrt(A*B0))/alpha,(A-math.sqrt(A*B0))/alpha])
    right=left[::-1]
    L=np.diag(left+right+g)-np.array([[0.,g],[g,0.]])
    Q=L/np.sqrt(np.outer(cap,cap))
    lam,U=eigh(Q)
    residues=(U.T@(left/np.sqrt(cap)))*(U.T@(right/np.sqrt(cap)))
    err=max(np.max(np.abs(lam-[alpha,beta])), np.max(np.abs(residues-[A,-B0])))
    max_two_pole_error=max(max_two_pole_error,float(err))
assert max_two_pole_error<1e-11
# A finite 2-state improvement when the capacity budget is larger.
comparison_budget=5.
comparison_kappa=1.
comparison_capacity=np.array([2.5,2.5])
comparison_left=np.array([15/4,0.])
comparison_right=np.array([0.,15/4])
comparison_internal=15/8
comparison_L=np.diag(comparison_left+comparison_right+comparison_internal)-np.array([[0.,comparison_internal],[comparison_internal,0.]])
comparison_Q=comparison_L/np.sqrt(np.outer(comparison_capacity,comparison_capacity))
comparison_rates,comparison_U=eigh(comparison_Q)
comparison_residues=(comparison_U.T@(comparison_left/np.sqrt(comparison_capacity)))*(comparison_U.T@(comparison_right/np.sqrt(comparison_capacity)))
comparison_q=lambda x: math.exp(-.9*x)-math.exp(-1.1*x)
comparison_D=float(np.sum(comparison_residues*(np.exp(-.9*comparison_rates)-np.exp(-1.1*comparison_rates))/comparison_rates))
single_rate=math.log(1.1/.9)/.2
single_D=comparison_q(single_rate)
single_C=4/single_rate
assert np.max(np.abs(comparison_rates-[1.5,3.]))<1e-12
assert np.max(np.abs(comparison_residues-[45/16,-45/16]))<1e-12
assert abs(float(np.sum(comparison_residues/comparison_rates))+1/16-1)<1e-12
assert single_C<=comparison_budget and comparison_D>single_D
result={'status':'PASS','random_networks':300,'worst':worst,
        'two_pole_constructions':100, 'two_pole_max_error':max_two_pole_error,
        'sharp_window_example':{'interval':[.9,1.1], 'capacity_budget':budget,
        'total_static_conductance':kappa, 'balanced_boundary_conductance_each':star_g,
        'internal_capacity':budget, 'direct_conductance':direct,
        'rate':rate, 'dynamic_static_conductance':dynamic_a,
        'optimal_window_signal':D, 'critical_capacity_budget':4*kappa/rate},
        'finite_two_state_improvement':{
        'interval':[.9,1.1], 'capacity_budget':comparison_budget,
        'total_static_conductance':comparison_kappa,
        'two_state_capacities':comparison_capacity.tolist(),
        'two_state_left_conductances':comparison_left.tolist(),
        'two_state_right_conductances':comparison_right.tolist(),
        'two_state_internal_conductance':comparison_internal,
        'two_state_direct_conductance':1/16,
        'two_state_rates':comparison_rates.tolist(),
        'two_state_residues':comparison_residues.tolist(),
        'two_state_dynamic_static_conductance':15/16,
        'two_state_window_signal':comparison_D,
        'optimal_one_state_rate':single_rate,
        'optimal_one_state_capacity_used':single_C,
        'optimal_one_state_window_signal':single_D,
        'relative_gain':comparison_D/single_D-1,
        'global_two_state_optimality_claimed':False}}
Path(__file__).with_suffix('.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps(result,ensure_ascii=False,indent=2))
