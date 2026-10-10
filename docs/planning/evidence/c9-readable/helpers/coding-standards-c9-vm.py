"""C9 copied Go reference and analyzer; authorized ClaudeOS only."""
from pathlib import Path
import json,os,platform,subprocess,hashlib,sys
assert platform.node()=='claudeos' and os.getuid()==1000
root=Path.home()/'coding-standards-verification/bee-c9-2026-10-09';project=root/'project';os.chdir(project);inputs=json.load(sys.stdin)
(root/'results/source-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
c5=root.parent/'bee-c5-2026-10-08';c4=root.parent/'bee-c4-2026-10-08'
env=os.environ.copy();env.update(PATH=str(root/'tools/go/bin')+':'+str(root/'bin')+':'+str(c5/'bin')+':'+env['PATH'],GOENV='off',GOTOOLCHAIN='local',GOCACHE=str(root/'cache/go-build'),GOMODCACHE=str(root/'cache/go-mod'),GOPATH=str(root/'cache/gopath'),GOPROXY='https://proxy.golang.org',GOFLAGS='-mod=readonly',PRE_COMMIT_HOME=str(root/'cache/pre-commit'),XDG_CACHE_HOME=str(root/'cache/xdg'),XDG_CONFIG_HOME=str(root/'cache/config'),CI='1',NO_COLOR='1')
for name,text in inputs['overlay'].items():
 if name=='Makefile.snippet':name='Makefile'
 elif name=='bloat.sh':name='scripts/bloat.sh'
 elif name.startswith(('schema/','playerid/')):name='internal/'+name
 p=Path(name);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
Path('go.mod').write_text('module example.com/consumer\n\ngo 1.26.0\n')
rows=[]
def snap():return {p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in project.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.git','bin'])}
def run(label,args,code=0,marker=None,unchanged=True,cwd=None,extra=None,timeout=300):
 before=snap();e=env.copy();e.update(extra or {});r=subprocess.run(args,cwd=cwd or project,env=e,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=timeout);after=snap();matched=r.returncode==code and (marker is None or marker in r.stdout+r.stderr) and (not unchanged or before==after)
 rows.append({'label':label,'argv':args,'cwd':str(cwd or project),'status':r.returncode,'expected':code,'diagnostic':marker,'stdout':r.stdout,'stderr':r.stderr,'before':before,'after':after,'unchanged_required':unchanged,'matched':matched});(root/'results/checks.json').write_text(json.dumps(rows,indent=2)+'\n');print(label,r.returncode,matched,flush=True);assert matched,(label,(r.stdout+r.stderr)[-8000:]);return r
run('config-verify',['golangci-lint','config','verify'])
run('main-module-initialize',['go','mod','tidy'],unchanged=False,extra={'GOFLAGS':''})
run('main-module-verify',['go','mod','verify'])
run('tool-module-initialize',['go','mod','tidy'],cwd=project/'tools/ifaceguard',unchanged=False,extra={'GOFLAGS':''})
run('tool-module-verify',['go','mod','verify'],cwd=project/'tools/ifaceguard')
files=[str(p) for p in project.rglob('*.go')];run('format-copied-go',['gofmt','-w',*files],unchanged=False)
run('clean-lint',['make','lint'],timeout=600)
run('clean-format',['make','format-check'])
run('clean-vet',['make','vet'])
run('actual-race-tests',['make','test'],timeout=600)
run('coverage-floor',['make','test-coverage'],unchanged=False,timeout=600)
run('generic-build',['make','build'])
run('tool-regressions',['go','test','-v','./...'],cwd=project/'tools/ifaceguard',timeout=600)
run('optional-analyzer-clean',['make','ifaceguard'],timeout=600)
run('inventory-clean',['make','bloat'])
# Exact published negative, not a suppressed fixture or a convenient arbitrary error.
p=Path('internal/negative/violating.go');p.parent.mkdir();p.write_text(inputs['violating'])
run('actual-errcheck-fixture',['make','lint'],2,'errcheck')
run('actual-analyzer-fixture',['make','ifaceguard'],2,'uses the empty interface',timeout=600)
p.unlink();p.parent.rmdir()
p=Path('internal/playerid/bypass.go');p.write_text('package playerid\nvar bypass = PlayerID("99")\n');run('intended-string-conversion',['make','build'],2,'cannot convert');p.unlink()
p=Path('internal/schema/assertion_test.go');p.write_text('package schema\nimport "testing"\nfunc TestC9IntendedFailure(t *testing.T) { t.Fatal("C9 intended assertion") }\n');run('intended-assertion',['make','test'],2,'C9 intended assertion');p.unlink()
p=Path('internal/schema/format_probe.go');p.write_text('package schema\nfunc FormatProbe( )string{return "probe"}\n');run('intended-format',['make','format-check'],2,'FormatProbe');p.unlink()
run('invalid-coverage-threshold',['make','test-coverage','COVERAGE_THRESHOLD=101'],2,'coverage: invalid',unchanged=False,timeout=600)
# Optional analyzer declared allow is not authenticated approval.
p=Path('internal/playerid/allow.go');p.write_text('package playerid\n//ifaceguard:allow deliberate generic boundary in disposable fixture\nfunc Allowed(v any) any { return v }\n');run('actual-analyzer-allow',['make','ifaceguard'],timeout=600);p.unlink()
run('restored-lint',['make','lint'],timeout=600);run('restored-format',['make','format-check']);run('restored-race',['make','test'],timeout=600);run('restored-coverage',['make','test-coverage'],unchanged=False,timeout=600);run('restored-build',['make','build'])
p=Path('internal/space name\nfile.go');p.write_text('package inventory\n// counted path\n');run('inventory-space-newline',['make','bloat'],marker='2 physical lines');p.unlink()
empty=root/'empty';empty.mkdir();run('inventory-missing-source',['bash',str(project/'scripts/bloat.sh')],1,'no Go production files',cwd=empty)
# Show traversal errors are failures, not implicit empty green.
fail=root/'failing-bin';fail.mkdir();(fail/'find').write_text('#!/bin/sh\nprintf "C9 intended traversal failure\\n" >&2\nexit 7\n');(fail/'find').chmod(0o755);run('inventory-traversal-failure',['make','bloat'],2,'C9 intended traversal failure',extra={'PATH':str(fail)+':'+env['PATH']})
for label,args in [('git-init',['git','init']),('fixture-name',['git','config','user.name','Bee verification fixture']),('fixture-email',['git','config','user.email','fixture@example.invalid']),('actual-hook-install',[str(c4/'venv/bin/pre-commit'),'install'])]:run(label,args,unchanged=False)
Path('.gitignore').write_text('coverage.out\ncoverage-summary.txt\ntools/ifaceguard/bin/\n')
p=Path('internal/schema/hook_probe.go');p.write_text('package schema\nimport "os"\nfunc HookProbe() { _, _ = os.Open("missing") }\n');run('actual-linter-hook-reject',[str(c4/'venv/bin/pre-commit'),'run','golangci-lint','--files',str(p)],1,'errcheck',timeout=600);p.unlink()
run('stage-current-clean',['git','add','.'],unchanged=False)
run('ordinary-clean-hook-commit',['git','commit','-m','fixture: verify Go reference hooks'],unchanged=False,timeout=600)
record={'versions':{'go':subprocess.check_output(['go','version'],env=env,text=True).strip(),'golangci':subprocess.check_output(['golangci-lint','version'],env=env,text=True).strip()},'files':{p.relative_to(project).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'text':p.read_text()} for p in project.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.git','bin'])},'scope':'Synthetic selected Go/schema/ID/caller/analyzer/race/coverage/hook reference; no deployed/hosted/live consumer/authorization/race-freedom/universal safety. Task-owned Go1.27.2/linter2.14 and disabled automatic SDK download.'}
(root/'results/final.json').write_text(json.dumps(record,indent=2)+'\n')
