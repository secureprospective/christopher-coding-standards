"""Final uncached/rule-specific C9 observations; ClaudeOS only."""
from pathlib import Path
import json,os,platform,subprocess,hashlib
assert platform.node()=='claudeos' and os.getuid()==1000
root=Path.home()/'coding-standards-verification/bee-c9-2026-10-09';project=root/'project';os.chdir(project);c5=root.parent/'bee-c5-2026-10-08';c4=root.parent/'bee-c4-2026-10-08'
env=os.environ.copy();env.update(PATH=str(root/'tools/go/bin')+':'+str(root/'bin')+':'+str(c5/'bin')+':'+env['PATH'],GOENV='off',GOTOOLCHAIN='local',GOCACHE=str(root/'cache/go-build'),GOMODCACHE=str(root/'cache/go-mod'),GOPATH=str(root/'cache/gopath'),GOPROXY='https://proxy.golang.org',GOFLAGS='-mod=readonly',PRE_COMMIT_HOME=str(root/'cache/pre-commit'),XDG_CACHE_HOME=str(root/'cache/xdg'),XDG_CONFIG_HOME=str(root/'cache/config'),CI='1',NO_COLOR='1')
rows=[]
def snap():return {p.relative_to(project).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in project.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.git','bin'])}
def run(label,args,code=0,marker=None,cwd=None):
 before=snap();r=subprocess.run(args,cwd=cwd or project,env=env,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=600);after=snap();rows.append({'label':label,'argv':args,'cwd':str(cwd or project),'status':r.returncode,'expected':code,'diagnostic':marker,'stdout':r.stdout,'stderr':r.stderr,'before':before,'after':after});(root/'results/supplement.json').write_text(json.dumps(rows,indent=2)+'\n');print(label,r.returncode,flush=True);assert r.returncode==code and (marker is None or marker in r.stdout+r.stderr) and before==after,(label,(r.stdout+r.stderr)[-6000:]);return r
p=Path('internal/negative/violating.go');p.parent.mkdir();p.write_bytes((root/'results/violating.go').read_bytes());r=run('formatted-exact-errcheck-fixture',['make','lint'],2,'Error return value is not checked (errcheck)');assert '* errcheck: 1' in r.stdout and '* gofmt:' not in r.stdout
run('formatted-analyzer-fixture',['make','ifaceguard'],2,'uses the empty interface');p.unlink();p.parent.rmdir()
run('uncached-race-verbose',['go','test','-race','-count=1','-v','./...'])
run('uncached-tool-regressions',['go','test','-count=1','-v','./...'],cwd=project/'tools/ifaceguard')
for label,args in [('final-module-verify',['go','mod','verify']),('final-lint',['make','lint']),('final-format',['make','format-check']),('final-vet',['make','vet']),('final-build',['make','build']),('final-analyzer',['make','ifaceguard']),('actual-all-files-clean-hooks',[str(c4/'venv/bin/pre-commit'),'run','--all-files'])]:run(label,args)
run('final-tool-module-verify',['go','mod','verify'],cwd=project/'tools/ifaceguard')
scanner=hashlib.sha256((c5/'bin/gitleaks').read_bytes()).hexdigest();assert scanner=='88f91962aa2f93ac6ab281d553b9e125f5197bbbce38f9f2437f7299c32e5509'
record={'versions':{'go':subprocess.check_output(['go','version'],env=env,text=True).strip(),'golangci':subprocess.check_output(['golangci-lint','version'],env=env,text=True).strip()},'native_scanner_sha256':scanner,'files':{p.relative_to(project).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'text':p.read_text()} for p in project.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.git','bin'])},'formatted_negative':{'sha256':hashlib.sha256((root/'results/violating.go').read_bytes()).hexdigest(),'text':(root/'results/violating.go').read_text()},'scope':'Final uncached reference/analyzer tests, sole formatted errcheck diagnostic, restored clean checks/actual installed all-files hooks. Original unformatted fixture had actual errcheck plus gofmt; not concealed.'}
(root/'results/final-supplement.json').write_text(json.dumps(record,indent=2)+'\n')
