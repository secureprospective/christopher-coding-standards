"""Assemble and exercise C7 shipped Astro composition on authorized ClaudeOS."""
from pathlib import Path
import json,os,platform,subprocess,hashlib,urllib.request
assert platform.node()=='claudeos' and os.getuid()==1000
root=Path.home()/'coding-standards-verification/bee-c7-2026-10-09';root.mkdir()
for d in ['project with spaces','results','config','cache']:(root/d).mkdir()
inputs=json.load(__import__('sys').stdin)
(root/'results/source-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n')
project=root/'project with spaces';os.chdir(project)
c5=root.parent/'bee-c5-2026-10-08';c4=root.parent/'bee-c4-2026-10-08'
env=os.environ.copy();env.update(PATH=str(c5/'bin')+':'+env['PATH'],NPM_CONFIG_USERCONFIG=str(root/'config/npmrc'),NPM_CONFIG_GLOBALCONFIG=str(root/'config/global-npmrc'),NPM_CONFIG_CACHE=str(root/'cache/npm'),XDG_CACHE_HOME=str(root/'cache/xdg'),XDG_DATA_HOME=str(root/'cache/data'),XDG_CONFIG_HOME=str(root/'config/xdg'),COREPACK_HOME=str(root/'cache/corepack'),PRE_COMMIT_HOME=str(root/'cache/pre-commit'),ASTRO_TELEMETRY_DISABLED='1',CI='1',NO_COLOR='1')
for n in ['npmrc','global-npmrc']:(root/'config'/n).write_text('')
metadata=[]
for name,v in [('astro','7.3.8'),('@astrojs/check','0.9.10'),('prettier','3.9.9'),('prettier-plugin-astro','1.1.0'),('@astrojs/react','7.0.1'),('react','19.3.0'),('react-dom','19.3.0'),('@types/react','19.3.0'),('@types/react-dom','19.3.0')]:
 u='https://registry.npmjs.org/'+name.replace('/','%2f')+'/'+v;d=json.load(urllib.request.urlopen(u,timeout=45));assert d['name']==name and d['version']==v;metadata.append({'url':u,'record':d})
(root/'results/metadata.json').write_text(json.dumps(metadata,indent=2)+'\n')
for name in ['biome.json','vitest.config.ts','stryker.config.mjs','Makefile','scripts/check-package-manager.mjs','src/schemas/example.ts','src/schemas/example.test.ts']:
 p=Path(name);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(inputs['base'][name])
Path('Makefile').write_text(Path('Makefile').read_text()+'\n'+inputs['overlay']['Makefile.snippet'])
for name in ['tsconfig.json','.prettierrc.json','README.md']:Path(name).write_text(inputs['overlay'][name])
Path('.pre-commit-config.yaml').write_text(inputs['base']['.pre-commit-config.yaml']+'\n'+inputs['overlay']['.pre-commit-config.yaml.snippet'])
b=json.loads(inputs['base']['package.json.snippet']);o=json.loads(inputs['overlay']['package.json.snippet']);b.update(name='bee-c7-fixture',version='0.0.0',private=True)
for k in ['scripts','devDependencies','dependencies']:b.setdefault(k,{}).update(o[k])
b['type']=o['type'];Path('package.json').write_text(json.dumps(b,indent=2)+'\n')
biome=json.loads(Path('biome.json').read_text());biome['files']['includes']+=['!**/*.astro','!**/.astro'];Path('biome.json').write_text(json.dumps(biome,indent=2)+'\n')
Path('astro.config.mjs').write_text('import { defineConfig } from "astro/config";\n\nexport default defineConfig({});\n')
Path('src/pages').mkdir(parents=True)
page='''---
const title: string = "Astro <safe>";
const count: number = 2;
---
<html lang="en"><head><title>{title}</title></head><body><h1>{title}</h1><p>Count {count}</p></body></html>
'''
Path('src/pages/index.astro').write_text(page)
rows=[]
def snap():return {p.as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in Path('.').rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','dist','.astro','.git'])}
def check(label,argv,code=0,marker=None,unchanged=True,timeout=300):
 before=snap();r=subprocess.run(argv,env=env,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=timeout);after=snap();matched=r.returncode==code and (marker is None or marker in r.stdout+r.stderr) and (not unchanged or before==after)
 rows.append({'label':label,'argv':argv,'cwd':str(project),'status':r.returncode,'expected':code,'diagnostic':marker,'stdout':r.stdout,'stderr':r.stderr,'before':before,'after':after,'source_unchanged_required':unchanged,'matched':matched});(root/'results/checks.json').write_text(json.dumps(rows,indent=2)+'\n');print(label,r.returncode,matched,flush=True);assert matched,(label,(r.stdout+r.stderr)[-8000:])
 return r
check('initialize-reviewed-lock',['pnpm','install','--store-dir',str(root/'cache/pnpm-store'),'--reporter=append-only'],unchanged=False,timeout=600)
check('frozen-install',['pnpm','install','--frozen-lockfile','--store-dir',str(root/'cache/pnpm-store'),'--reporter=append-only'])
check('audit',['pnpm','audit','--json'])
check('format-assembled-config',['pnpm','exec','biome','format','--write','.'],unchanged=False)
check('format-astro-initial',['make','format-astro'],unchanged=False)
for label,args in [('non-react-lint',['make','lint']),('non-react-format',['make','lint-astro']),('non-react-typecheck',['make','typecheck']),('non-react-tests',['make','test']),('non-react-build',['pnpm','run','build'])]:check(label,args)
html=Path('dist/index.html').read_text();assert 'Count 2' in html and 'Astro &lt;safe&gt;' in html;rows.append({'label':'non-react-render-observation','title_escaped':True,'count_rendered':True,'html':html,'html_sha256':hashlib.sha256(html.encode()).hexdigest()});(root/'results/checks.json').write_text(json.dumps(rows,indent=2)+'\n')
assert Path('.astro/types.d.ts').exists()
(root/'results/non-react-snapshot.json').write_text(json.dumps({'files':{p.as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'text':p.read_text()} for p in Path('.').rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','dist','.git'])}},indent=2)+'\n')
for n in ['base','strict','strictest']:
 p=Path('node_modules/astro/tsconfigs')/(n+'.json');(root/'results'/('preset-'+n+'.json')).write_bytes(p.read_bytes())
probe=Path('src/pages/type-probe.astro');probe.write_text('---\nconst value: number = "bad";\n---\n<p>{value}</p>\n');check('intended-frontmatter-type',['pnpm','run','typecheck'],1,'2322');probe.unlink()
probe=Path('src/schemas/type-probe.test.ts');probe.write_text('export const value: number = "bad";\n');check('tests-typechecked',['pnpm','run','typecheck'],1,'2322');probe.unlink()
check('wrong-manager',['npm','run','preinstall'],1,'Use the pnpm version declared')
probe=Path('src/pages/space name.astro');probe.write_text('---\nconst   title="probe"\n---\n<p>{title}</p>\n');check('intended-astro-format',['make','lint-astro'],2,'Code style issues')
check('git-init',['git','init'],unchanged=False);check('git-identity-name',['git','config','user.name','Bee verification fixture'],unchanged=False);check('git-identity-email',['git','config','user.email','fixture@example.invalid'],unchanged=False)
Path('.gitignore').write_text('node_modules/\ndist/\n.astro/\n')
check('install-actual-hooks',[str(c4/'venv/bin/pre-commit'),'install'],unchanged=False)
check('stage-space-file',['git','add','--',str(probe)],unchanged=False)
check('read-only-astro-hook',[str(c4/'venv/bin/pre-commit'),'run','prettier-astro','--files',str(probe)],1,'Code style issues')
check('deliberate-format-astro',['make','format-astro'],unchanged=False);check('restored-astro-hook',[str(c4/'venv/bin/pre-commit'),'run','prettier-astro','--files',str(probe)])
# Optional React is a separately selected, checked composition, not default JSX enablement.
m=json.loads(Path('package.json').read_text());m['dependencies'].update({'@astrojs/react':'7.0.1','react':'19.3.0','react-dom':'19.3.0'});m['devDependencies'].update({'@types/react':'19.3.0','@types/react-dom':'19.3.0'});Path('package.json').write_text(json.dumps(m,indent=2)+'\n')
# This source file is JSONC; add only the two explicit options at a stable actual property.
s=Path('tsconfig.json').read_text();assert s.count('"noImplicitOverride": true,')==1;s=s.replace('"noImplicitOverride": true,','"noImplicitOverride": true,\n    "jsx": "react-jsx",\n    "jsxImportSource": "react",');Path('tsconfig.json').write_text(s)
Path('astro.config.mjs').write_text('import react from "@astrojs/react";\nimport { defineConfig } from "astro/config";\n\nexport default defineConfig({ integrations: [react()] });\n')
Path('src/components').mkdir();Path('src/components/Counter.tsx').write_text('export function Counter({ count }: { count: number }) {\n  return <p>React count {count}</p>;\n}\n')
Path('src/pages/react.astro').write_text('---\nimport { Counter } from "../components/Counter";\n---\n<Counter count={2} />\n')
check('react-lock-init',['pnpm','install','--store-dir',str(root/'cache/pnpm-store'),'--reporter=append-only'],unchanged=False,timeout=600)
check('react-frozen-install',['pnpm','install','--frozen-lockfile','--store-dir',str(root/'cache/pnpm-store'),'--reporter=append-only'])
check('react-audit',['pnpm','audit','--json'])
check('react-format-config',['pnpm','exec','biome','check','--write','.'],unchanged=False)
check('react-format-pages',['make','format-astro'],unchanged=False)
for label,args in [('react-lint',['make','lint']),('react-format',['make','lint-astro']),('react-types',['make','typecheck']),('react-tests',['make','test']),('react-build',['pnpm','run','build'])]:check(label,args)
html=Path('dist/react/index.html').read_text();assert 'React count 2' in __import__('re').sub(r'<!--.*?-->','',html);rows.append({'label':'react-render-observation','count_rendered':True,'html':html,'html_sha256':hashlib.sha256(html.encode()).hexdigest()});(root/'results/checks.json').write_text(json.dumps(rows,indent=2)+'\n')
p=Path('src/pages/react.astro');original=p.read_bytes();p.write_text(p.read_text().replace('count={2}','count="bad"'));check('intended-react-prop',['pnpm','run','typecheck'],1,'2322');p.write_bytes(original)
check('restored-react-types',['make','typecheck']);check('restored-react-format',['make','lint-astro'])
Path('src/schemas/assertion-probe.test.ts').write_text('import { expect, it } from "vitest";\nit("C7 intended assertion", () => { expect(1).toBe(2); });\n');check('intended-assertion',['make','test'],2,'C7 intended assertion');Path('src/schemas/assertion-probe.test.ts').unlink();check('restored-tests',['make','test'])
check('stage-final-clean',['git','add','.'],unchanged=False)
check('ordinary-clean-hook-commit',['git','commit','-m','fixture: verify Astro integration hooks'],unchanged=False,timeout=600)
record={'versions':{c:subprocess.check_output([c,'--version'],env=env,text=True).strip() for c in ['node','npm','pnpm']},'files':{p.as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'text':p.read_text()} for p in Path('.').rglob('*') if p.is_file() and not any(x in p.parts for x in ['node_modules','dist','.git'])},'scope':'Synthetic Astro non-React and optional React render/type/format/Node-test composition. No browser/hydration/E2E/deploy/hosted enforcement. Task-owned config/cache; pnpm/native scanner/precommit reuse verified C5/C4 tools.'}
(root/'results/final.json').write_text(json.dumps(record,indent=2)+'\n')
