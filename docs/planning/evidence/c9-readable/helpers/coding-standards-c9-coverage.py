"""Actual below-floor and tool-error coverage probes on authorized ClaudeOS."""
from pathlib import Path
import json,os,platform,subprocess,hashlib
assert platform.node()=='claudeos' and os.getuid()==1000
root=Path.home()/'coding-standards-verification/bee-c9-2026-10-09';project=root/'project';os.chdir(project);c5=root.parent/'bee-c5-2026-10-08'
env=os.environ.copy();env.update(PATH=str(root/'tools/go/bin')+':'+str(root/'bin')+':'+str(c5/'bin')+':'+env['PATH'],GOENV='off',GOTOOLCHAIN='local',GOCACHE=str(root/'cache/go-build'),GOMODCACHE=str(root/'cache/go-mod'),GOPATH=str(root/'cache/gopath'),GOPROXY='https://proxy.golang.org',GOFLAGS='-mod=readonly',CI='1',NO_COLOR='1')
rows=[]
def snap():return {p.relative_to(project).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in project.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.git','bin'])}
def run(label,args,code=0,marker=None,variables=None):
 before=snap();r=subprocess.run(args,env=variables or env,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=600);rows.append({'label':label,'argv':args,'status':r.returncode,'expected':code,'diagnostic':marker,'stdout':r.stdout,'stderr':r.stderr,'before':before,'after':snap(),'declared_outputs':['coverage.out','coverage-summary.txt']});(root/'results/coverage.json').write_text(json.dumps(rows,indent=2)+'\n');print(label,r.returncode,flush=True);assert r.returncode==code and (marker is None or marker in r.stdout+r.stderr),(label,(r.stdout+r.stderr)[-4000:])
p=Path('internal/schema/coverage_probe.go');p.write_text('package schema\nfunc CoverageProbe(value int) int {\n'+''.join(f'if value == {i} {{ return {i+1} }}\n' for i in range(60))+'return -1\n}\n')
run('actual-uncovered-source-floor',['make','test-coverage'],2,'< threshold 80.0%');p.unlink()
folder=root/'coverage-failing-bin';folder.mkdir();real=root/'tools/go/bin/go';(folder/'go').write_text('#!/bin/sh\nif [ "$1" = tool ] && [ "$2" = cover ]; then printf "C9 intended cover-tool failure\\n" >&2; exit 7; fi\nexec "'+str(real)+'" "$@"\n');(folder/'go').chmod(0o755);e=env.copy();e['PATH']=str(folder)+':'+env['PATH'];run('coverage-tool-fails-closed',['make','test-coverage'],2,'C9 intended cover-tool failure',e)
run('restored-coverage',['make','test-coverage']);run('final-format',['make','format-check']);run('final-lint',['make','lint'])
prior=json.loads((root/'results/final-supplement.json').read_text());prior['files']={p.relative_to(project).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'text':p.read_text()} for p in project.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.git','bin'])};(root/'results/final-candidate.json').write_text(json.dumps(prior,indent=2)+'\n')
