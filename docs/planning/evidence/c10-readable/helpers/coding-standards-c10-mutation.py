"""Actual selected mutmut3 report and source-integrity checks; ClaudeOS only."""
from pathlib import Path
import os,platform,json,subprocess,hashlib
assert platform.node()=='claudeos' and os.getuid()==1000
root=Path.home()/'coding-standards-verification/bee-c10-2026-10-09';project=root/'project with spaces';os.chdir(project);c5=root.parent/'bee-c5-2026-10-08'
env=os.environ.copy();env.update(PATH=str(root/'venv/bin')+':'+str(c5/'bin')+':'+env['PATH'],XDG_CACHE_HOME=str(root/'cache/xdg'),XDG_CONFIG_HOME=str(root/'cache/config'),PIP_CONFIG_FILE='/dev/null',PIP_CACHE_DIR=str(root/'cache/pip'),PYTHONNOUSERSITE='1',CI='1',NO_COLOR='1')
rows=[]
def snap():return {p.relative_to(project).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in project.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.git','.mypy_cache','.ruff_cache','.pytest_cache','mutants','__pycache__'])}
for label,args in [('actual-mutation-report',['make','mutation-report']),('actual-mutation-all-results',['mutmut','results','--all','true']),('actual-mutation-export',['mutmut','export-cicd-stats']),('restored-lint',['make','lint']),('restored-format',['make','format-check']),('restored-types',['make','typecheck']),('restored-tests',['make','test'])]:
 before=snap();r=subprocess.run(args,env=env,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=1200);after=snap();rows.append({'label':label,'argv':args,'status':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'before':before,'after':after,'source_unchanged':before==after,'scope':'Mutants/cache/reports expected separately; status0 tool completion is not all-killed or approval.'});(root/'results/mutation.json').write_text(json.dumps(rows,indent=2)+'\n');print(label,r.returncode,flush=True);assert r.returncode==0 and before==after,(label,(r.stdout+r.stderr)[-7000:])
records={p.relative_to(project).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'text':p.read_text()} for p in (project/'mutants').rglob('*') if p.is_file() and p.suffix in ['.json','.py','.toml','.meta']};(root/'results/mutation-files.json').write_text(json.dumps(records,indent=2)+'\n')
