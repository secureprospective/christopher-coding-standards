"""Copy current own source to a fresh space-path reference; no repo/worktree moves."""
from pathlib import Path
import json,os,platform,subprocess,hashlib
assert platform.node()=='claudeos' and os.getuid()==1000
root=Path.home()/'coding-standards-verification/bee-c9-2026-10-09';project=root/'project';space=root/'project with spaces';space.mkdir(exist_ok=True);c5=root.parent/'bee-c5-2026-10-08';c4=root.parent/'bee-c4-2026-10-08'
env=os.environ.copy();env.update(PATH=str(root/'tools/go/bin')+':'+str(root/'bin')+':'+str(c5/'bin')+':'+env['PATH'],GOENV='off',GOTOOLCHAIN='local',GOCACHE=str(root/'cache/go-build'),GOMODCACHE=str(root/'cache/go-mod'),GOPATH=str(root/'cache/gopath'),GOPROXY='https://proxy.golang.org',GOFLAGS='-mod=readonly',PRE_COMMIT_HOME=str(root/'cache/pre-commit'),XDG_CACHE_HOME=str(root/'cache/xdg'),XDG_CONFIG_HOME=str(root/'cache/config'),CI='1',NO_COLOR='1')
files=[p for p in project.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.git','bin'])]
for p in files:q=space/p.relative_to(project);q.parent.mkdir(parents=True,exist_ok=True);q.write_bytes(p.read_bytes())
rows=[]
def snap(cwd):return {p.relative_to(cwd).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in cwd.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.git','bin'])}
def run(label,args,cwd=space,unchanged=True):
 before=snap(cwd);r=subprocess.run(args,cwd=cwd,env=env,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=600);after=snap(cwd);rows.append({'label':label,'argv':args,'cwd':str(cwd),'status':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'before':before,'after':after,'unchanged_required':unchanged});(root/'results/spaces.json').write_text(json.dumps(rows,indent=2)+'\n');print(label,r.returncode,flush=True);assert r.returncode==0 and (not unchanged or before==after),(label,r.stdout+r.stderr)
run('current-quoted-analyzer',['make','ifaceguard'],project)
for label,args in [('space-lint',['make','lint']),('space-format',['make','format-check']),('space-analyzer',['make','ifaceguard']),('space-uncached-race',['go','test','-race','-count=1','-v','./...']),('space-build',['make','build']),('space-inventory',['make','bloat'])]:run(label,args)
run('stage-final-current-sdk',['git','add','.'],project,False);run('current-final-hooks',[str(c4/'venv/bin/pre-commit'),'run','--all-files'],project)
prior=json.loads((root/'results/final-candidate.json').read_text());prior['files']={p.relative_to(project).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'text':p.read_text()} for p in project.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.git','bin'])};(root/'results/final-candidate.json').write_text(json.dumps(prior,indent=2)+'\n')
