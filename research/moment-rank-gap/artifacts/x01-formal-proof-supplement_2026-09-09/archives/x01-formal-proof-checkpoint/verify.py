#!/usr/bin/env python3
"""Replay the Lean development, pin versions, and reject proof placeholders.
No mathematical PASS is emitted without a successful Lean build and axiom audit.
Dependencies must first be installed using the README commands.
"""
from pathlib import Path
import hashlib,json,re,shutil,subprocess,sys
ROOT=Path(__file__).resolve().parent
OUT=ROOT/'run-results'
OUT.mkdir(exist_ok=True)
FILES=['MomentIslands.lean','Packing.lean','BandSharp.lean','FiniteBand.lean','Rounding.lean','X01.lean']
PIN='c44e0c8ee63ca166450922a373c7409c5d26b00b'
ALLOWED={'propext','Classical.choice','Quot.sound'}
record={'status':'NOT_RUN','scope':'Lean build and per-theorem axiom audit',
        'expected_lean':'4.19.0','expected_mathlib_commit':PIN,'sources':{},'commands':[]}
theorems=[]
def finish(status,reason,exitcode):
    record.update(status=status,reason=reason)
    (OUT/'verification.json').write_text(json.dumps(record,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps({'status':status,'reason':reason,'theorems':len(theorems)},ensure_ascii=False))
    raise SystemExit(exitcode)
for name in FILES:
    p=ROOT/name
    if not p.is_file(): finish('FAIL','Missing source: '+name,1)
    txt=p.read_text()
    names=re.findall(r'^(?:theorem|lemma)\s+([A-Za-z_][A-Za-z_0-9]*)',txt,re.M)
    theorems.extend('MomentIslands.'+n for n in names)
    record['sources'][name]={'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'theorems':len(names)}
    if re.search(r'\b(?:sorry|admit|native_decide)\b',txt) or re.search(r'^\s*(?:axiom|unsafe)\s',txt,re.M):
        finish('FAIL','Forbidden proof escape token: '+name,1)
if len(set(theorems))!=len(theorems): finish('FAIL','Duplicate theorem names',1)
record['static_audit']={'theorem_count':len(theorems),'placeholder_tokens':False,'new_axiom_declarations':False}
if not shutil.which('lake') or not shutil.which('lean'):
    finish('BLOCKED','Lean/Lake executables are not installed on PATH; no Lean theorem was checked.',2)
def run(args,logname):
    try:
        r=subprocess.run(args,cwd=ROOT,text=True,stdout=subprocess.PIPE,stderr=subprocess.STDOUT)
    except OSError as e: finish('BLOCKED',str(e),2)
    (OUT/logname).write_text(r.stdout)
    record['commands'].append({'argv':args,'exit_code':r.returncode,'log':logname})
    return r
v=run(['lake','env','lean','--version'],'lean-version.log')
if v.returncode or not re.search(r'\bversion 4\.19\.0\b',v.stdout):
    finish('FAIL','Lean version is unavailable or does not match 4.19.0.',1)
c=run(['git','-C','.lake/packages/mathlib','rev-parse','HEAD'],'mathlib-commit.log')
if c.returncode or c.stdout.strip()!=PIN:
    finish('FAIL','Mathlib checkout does not match the pinned commit; run the documented setup first.',1)
b=run(['lake','build'],'build.log')
if b.returncode: finish('FAIL','Lean build failed; inspect run-results/build.log.',1)
audit='import X01\n'+'\n'.join('#print axioms '+n for n in theorems)+'\n'
(ROOT/'Audit.lean').write_text(audit)
r=run(['lake','env','lean','Audit.lean'],'axioms.log')
if r.returncode: finish('FAIL','Lean axiom query failed.',1)
if 'sorryAx' in b.stdout+r.stdout: finish('FAIL','Lean reports a proof placeholder axiom.',1)
actual={}
for n in theorems:
    m=re.search(re.escape("'"+n+"'")+r'\s+depends on axioms:\s*\[([^\]]*)\]',r.stdout,re.S)
    if m:
        ax={a.strip() for a in m.group(1).split(',') if a.strip()}
    elif re.search(re.escape("'"+n+"'")+r'\s+does not depend on any axioms',r.stdout):
        ax=set()
    else: finish('FAIL','Missing axiom result for '+n,1)
    actual[n]=sorted(ax)
    if not ax<=ALLOWED: finish('FAIL','Unexpected axioms for '+n+': '+str(sorted(ax-ALLOWED)),1)
record['axioms']=actual
finish('PASS','Every listed theorem compiled under the pinned versions and passed the axiom audit.',0)
