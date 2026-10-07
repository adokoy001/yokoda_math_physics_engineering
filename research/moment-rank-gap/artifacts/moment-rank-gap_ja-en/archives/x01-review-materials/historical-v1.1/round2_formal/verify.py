#!/usr/bin/env python3
"""Run the unmodified Lean kernel with a pinned Mathlib checkout.

Example for this workspace:
  python3 verify.py --lean-root ../formal_env/lean-4.19.0-linux \
    --mathlib-root ../formal_env/mathlib4 \
    --compat-library ../formal_env/proc_self_compat.so

On a standard Lean/Lake installation use the three commands in README.md.
"""
import argparse
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

p = argparse.ArgumentParser()
p.add_argument('--lean-root', type=Path, required=True)
p.add_argument('--mathlib-root', type=Path, required=True)
p.add_argument('--compat-library', type=Path)
args = p.parse_args()
out = Path(__file__).resolve().parent
source = out / 'MomentIslands.lean'
leanroot = args.lean_root.resolve()
mathlib = args.mathlib_root.resolve()
env = os.environ.copy()
env['PATH'] = str(leanroot / 'bin') + os.pathsep + env.get('PATH', '')
if args.compat_library:
    env['LD_PRELOAD'] = str(args.compat_library.resolve())

def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def run(command, cwd):
    r = subprocess.run(command, cwd=cwd, env=env, text=True,
                       stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    return {'command': [str(x) for x in command], 'cwd': str(cwd),
            'exit_code': r.returncode, 'output': r.stdout}

version = run([str(leanroot / 'bin/lean'), '--version'], out)
commit = run(['git', 'rev-parse', 'HEAD'], mathlib)
command = [str(leanroot / 'bin/lake'), 'env', 'lean', '--root=' + str(out),
           '-o', str(out / 'MomentIslands.olean'), str(source)]
result = run(command, mathlib)
source_text = source.read_text(encoding='utf-8')
axiom_audit = {
    'theorem_declarations': len(re.findall(r'^theorem\s+', source_text, re.M)),
    'axiom_print_commands': len(re.findall(r'^#print axioms\s+', source_text, re.M)),
    'sorry_axiom_in_output': 'sorryAx' in result['output'],
    'new_axiom_declarations': bool(re.search(r'^\s*axiom\s+', source_text, re.M)),
    'placeholder_tokens': bool(re.search(r'\b(?:sorry|admit)\b', source_text)),
}
passed = (result['exit_code'] == 0 and not axiom_audit['sorry_axiom_in_output']
          and not axiom_audit['new_axiom_declarations']
          and not axiom_audit['placeholder_tokens']
          and axiom_audit['theorem_declarations'] == axiom_audit['axiom_print_commands'])
attempt = len(list(out.glob('lean-attempt-*.log'))) + 1
log = out / f'lean-attempt-{attempt:02d}.log'
log.write_text(result['output'], encoding='utf-8')
(out / 'lean-check.log').write_text(result['output'], encoding='utf-8')
record = {
    'status': 'PASS' if passed else 'FAIL',
    'lean_version': version,
    'mathlib_commit': commit,
    'proof_check': result,
    'axiom_audit': axiom_audit,
    'source_sha256': sha(source),
    'lean_binary_sha256': sha(leanroot / 'bin/lean'),
    'lean_shared_library_sha256': sha(leanroot / 'lib/lean/libleanshared.so'),
    'runtime_compatibility': {
        'used': bool(args.compat_library),
        'scope': 'Only readlink(/proc/<getpid()>/exe) is resolved as /proc/self/exe.',
        'lean_kernel_modified': False,
        'source_sha256': sha(out / 'proc_self_compat.c')
    },
}
(out / 'verification.json').write_text(
    json.dumps(record, indent=2, ensure_ascii=False) + '\n', encoding='utf-8')
print(version['output'], end='')
print(result['output'], end='')
print('Exit code:', result['exit_code'])
sys.exit(0 if passed else 1)
