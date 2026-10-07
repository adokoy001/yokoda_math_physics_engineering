"""Deterministic illustrative design calculation; no experimental data."""
import json
from pathlib import Path
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import brentq

HERE=Path(__file__).resolve().parent
lam,T,tau=.25,1.,.1
delta=(2*np.sqrt(7)-5)/3
x=brentq(lambda x:np.exp(x)-2*x-1,.1,3)
h=x/lam
phi=-np.expm1(-lam*T)/(lam*T)
A=np.exp(-lam*tau)*phi*(-np.expm1(-lam*h))**2
numbers=dict(lam=lam,ramp_duration=T,post_hold_delay=tau,window_width=h,
             coefficient=A,delta=delta,integrated_certificate_radius=delta*A,
             uniform_gain_error_lower_bound=delta*A/(2*h),optimal_lambda_h=x,
             total_end_time=T+tau+2*h)
(HERE/'finite-window-design.json').write_text(json.dumps(numbers,indent=2))
plt.rcParams.update({'font.family':'DejaVu Sans','font.size':10,'axes.spines.top':False,
                     'axes.spines.right':False,'svg.fonttype':'none'})
fig,ax=plt.subplots(1,2,figsize=(10.8,3.8),layout='constrained')
t=np.linspace(0,14,500)
response=3+2*lam*phi*np.exp(-lam*t)
ax[0].plot(t,response,color='#087f8c',lw=2)
ax[0].axhline(3,color='#718184',ls='--',lw=1,label='Unknown steady term K11')
ax[0].axvspan(tau,tau+h,color='#148b83',alpha=.15,label='First integral (+)')
ax[0].axvspan(tau+h,tau+2*h,color='#d79542',alpha=.18,label='Second integral (-)')
ax[0].set(xlabel='Time after ramp ends (s)',ylabel='Boundary gain R11 (W/K)',
          title='Two windows cancel the steady term',xlim=(0,14),ylim=(2.98,3.47))
ax[0].legend(fontsize=8,loc='upper right',frameon=False)
hs=np.linspace(.03,14,500)
bound=1e3*delta*np.exp(-lam*tau)*phi*(-np.expm1(-lam*hs))**2/(2*hs)
ax[1].plot(hs,bound,color='#087f8c',lw=2)
ax[1].scatter([h],[numbers['uniform_gain_error_lower_bound']*1e3],color='#bd7b29',zorder=5)
ax[1].annotate(f'h = {h:.3f} s\n{numbers["uniform_gain_error_lower_bound"]*1e3:.3f} mW/K',
               (h,numbers['uniform_gain_error_lower_bound']*1e3),xytext=(7.5,3.1),
               arrowprops={'arrowstyle':'->','color':'#596c6e'},fontsize=9)
ax[1].set(xlabel='Width of each window h (s)',ylabel='Certified error floor (mW/K)',
          title='A guaranteed floor, not the optimum error',ylim=(0,5),xlim=(0,14))
for a in ax:a.grid(alpha=.15)
fig.savefig(HERE/'finite-window.svg')
fig.savefig(HERE/'finite-window.png',dpi=140)
print(json.dumps(numbers,indent=2))
