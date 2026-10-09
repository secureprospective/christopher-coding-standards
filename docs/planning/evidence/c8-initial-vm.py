"""C8 assembly/checks; execute only on operator-authorized ClaudeOS."""
from pathlib import Path
import json,os,platform,subprocess,hashlib,sys
assert platform.node()=='claudeos' and os.getuid()==1000
root=Path.home()/'coding-standards-verification/bee-c8-2026-10-09';project=root/'project';assert root.is_dir();os.chdir(project)
inputs=json.load(sys.stdin);(root/'results/source-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
c5=root.parent/'bee-c5-2026-10-08';c4=root.parent/'bee-c4-2026-10-08'
env=os.environ.copy();env.update(PATH=str(root/'bin')+':'+str(c5/'bin')+':'+env['PATH'],NPM_CONFIG_USERCONFIG=str(root/'config/npmrc'),NPM_CONFIG_GLOBALCONFIG=str(root/'config/global-npmrc'),NPM_CONFIG_CACHE=str(root/'cache/npm'),XDG_CACHE_HOME=str(root/'cache/xdg'),XDG_DATA_HOME=str(root/'cache/data'),XDG_CONFIG_HOME=str(root/'config/xdg'),BUN_INSTALL_CACHE_DIR=str(root/'cache/bun'),PRE_COMMIT_HOME=str(root/'cache/pre-commit'),CI='1',NO_COLOR='1')
for n in ['npmrc','global-npmrc']:(root/'config'/n).write_text('')
for name,text in inputs['overlay'].items():
 name=name.removeprefix('examples/')
 if name in ['package.json.snippet','Makefile.snippet']:continue
 p=Path(name);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
Path('Makefile').write_text(inputs['overlay']['Makefile.snippet'])
# Preserve actual protected exports; adapt only the test API import, not case bodies/oracles.
p=Path('server/src/schemas');p.mkdir(parents=True,exist_ok=True)
(p/'example.ts').write_text(inputs['schema'])
assert inputs['schema_tests'].count('"vitest"')==1
(p/'example.test.ts').write_text(inputs['schema_tests'].replace('"vitest"','"bun:test"'))
b=json.loads(inputs['base_package']);o=json.loads(inputs['overlay']['package.json.snippet'])
b.pop('pnpm');b['scripts']={k:v for k,v in b['scripts'].items() if k not in ['preinstall','mutation-test','mutation-test:full','test:coverage']};b['devDependencies']={k:v for k,v in b['devDependencies'].items() if k not in ['vitest','@vitest/coverage-v8'] and not k.startswith('@stryker-mutator/')}
for k in ['scripts','devDependencies','dependencies']:b.setdefault(k,{}).update(o[k])
for k in ['type','packageManager','engines']:b[k]=o[k]
b.update(name='bee-c8-fixture',version='0.0.0',private=True);Path('package.json').write_text(json.dumps(b,indent=2)+'\n')
rows=[]
def snap():return {p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in Path('.').rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','.git'])}
def run(label,args,code=0,marker=None,unchanged=True,timeout=300):
 before=snap();r=subprocess.run(args,env=env,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=timeout);after=snap();matched=r.returncode==code and (marker is None or marker in r.stdout+r.stderr) and (not unchanged or before==after)
 rows.append({'label':label,'argv':args,'status':r.returncode,'expected':code,'diagnostic':marker,'stdout':r.stdout,'stderr':r.stderr,'before':before,'after':after,'source_unchanged_required':unchanged,'matched':matched});(root/'results/checks.json').write_text(json.dumps(rows,indent=2)+'\n');print(label,r.returncode,matched,flush=True);assert matched,(label,(r.stdout+r.stderr)[-7000:]);return r
run('initialize-bun-lock',['bun','install'],unchanged=False,timeout=600)
run('frozen-bun-install',['bun','install','--frozen-lockfile'])
run('audit',['bun','audit','--json'])
run('format-assembled-source',['bun','run','format'],unchanged=False)
run('actual-default-checks',['make','check-all'])
for label,args in [('optional-import-profile',['make','check-deps']),('optional-line-inventory',['make','check-file-length']),('optional-component-profile',['make','check-components'])]:run(label,args)
p=Path('server/src/type-probe.ts');p.write_text('export const value: number = "bad";\n');run('intended-type',['make','typecheck'],2,'TS2322');p.unlink()
p=Path('server/src/lint-probe.ts');p.write_text('export const value: any = 1;\n');run('intended-lint',['make','lint'],2,'noExplicitAny');p.unlink()
p=Path('server/src/assertion-probe.test.ts');p.write_text('import { expect, test } from "bun:test";\ntest("C8 intended assertion", () => { expect(1).toBe(2); });\n');run('intended-assertion',['make','test'],2,'C8 intended assertion');p.unlink()
p=Path('server/src/components/bad-component.ts');p.write_text('export interface Bad { move(): void }\n');run('intended-component-method',['make','check-components'],2,'method signature');p.unlink()
p=Path('server/src/systems/bad-system.ts');p.write_text('import "../db/schema";\nexport const value = 1;\n');run('intended-import-layer',['make','check-deps'],2,'simulate-systems-no-db-network');p.unlink()
for name,target in [('cycle-a','cycle-b'),('cycle-b','cycle-a')]:Path('server/src/shared/'+name+'.ts').write_text('import "./'+target+'";\nexport const value = 1;\n')
run('intended-cycle-profile',['make','check-deps'],2,'no-circular')
for n in ['cycle-a','cycle-b']:Path('server/src/shared/'+n+'.ts').unlink()
p=Path('server/src/long.ts');p.write_text('// meaningful counting fixture\n'*311);run('long-file-is-inventory-not-quota',['bun','scripts/check-file-length.ts',str(p)],marker='311 physical lines');p.unlink()
run('restored-default-checks',['make','check-all']);run('restored-import-profile',['make','check-deps']);run('restored-component-profile',['make','check-components'])
# Missing/empty/out-of-scope selections are not quietly green.
run('component-out-of-scope',['bun','scripts/check-component-purity.ts','server/src/ecs/world.ts'],1,'Not a component source path')
empty=root/'empty';empty.mkdir(exist_ok=True)
r=subprocess.run(['bun',str(project/'scripts/check-component-purity.ts')],cwd=empty,env=env,capture_output=True,text=True);rows.append({'label':'component-missing-tree','argv':['bun',str(project/'scripts/check-component-purity.ts')],'cwd':str(empty),'status':r.returncode,'expected':1,'diagnostic':'No component files selected','stdout':r.stdout,'stderr':r.stderr});assert r.returncode==1 and 'No component files selected' in r.stdout+r.stderr
(root/'results/checks.json').write_text(json.dumps(rows,indent=2)+'\n')
for label,args in [('git-init',['git','init']),('fixture-name',['git','config','user.name','Bee verification fixture']),('fixture-email',['git','config','user.email','fixture@example.invalid']),('actual-hook-install',[str(c4/'venv/bin/pre-commit'),'install'])]:run(label,args,unchanged=False)
Path('.gitignore').write_text('node_modules/\n')
p=Path('server/src/space name.ts');p.write_text('export const value: any = 1;\n');run('actual-read-only-hook-reject',[str(c4/'venv/bin/pre-commit'),'run','biome-ci','--files',str(p)],1,'noExplicitAny');p.unlink()
run('stage-final-clean',['git','add','.'],unchanged=False)
run('restored-actual-hook',[str(c4/'venv/bin/pre-commit'),'run','biome-ci','--all-files'])
run('ordinary-clean-hook-commit',['git','commit','-m','fixture: verify Bun examples and hooks'],unchanged=False,timeout=600)
record={'versions':{c:subprocess.check_output([c,'--version'],env=env,text=True).strip() for c in ['bun','node','npm']},'files':{p.as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'text':p.read_text()} for p in Path('.').rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','.git'])},'scope':'Bun reference/shared schema15cases/ECS6/checker4. Optional import/syntax/line profile only, not mandatory architecture/purity/quotas or application safety. No live game/service/hosted/deployed execution.'}
(root/'results/final.json').write_text(json.dumps(record,indent=2)+'\n')
