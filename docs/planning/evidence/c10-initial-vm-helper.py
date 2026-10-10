"""Actual Python reference on authorized ClaudeOS, no Beelink product execution."""
from pathlib import Path
import os,platform,json,subprocess,hashlib,sys
assert platform.node()=='claudeos' and os.getuid()==1000
root=Path.home()/'coding-standards-verification/bee-c10-2026-10-09';project=root/'project with spaces';os.chdir(project);inputs=json.load(sys.stdin);(root/'results/source-inputs.json').write_text(json.dumps(inputs,indent=2)+'\n');c4=root.parent/'bee-c4-2026-10-08';c5=root.parent/'bee-c5-2026-10-08'
env=os.environ.copy();env.update(PATH=str(root/'venv/bin')+':'+str(c5/'bin')+':'+env['PATH'],PIP_CONFIG_FILE='/dev/null',PIP_CACHE_DIR=str(root/'cache/pip'),PIP_INDEX_URL='https://pypi.org/simple',PIP_DISABLE_PIP_VERSION_CHECK='1',XDG_CACHE_HOME=str(root/'cache/xdg'),XDG_CONFIG_HOME=str(root/'cache/config'),PRE_COMMIT_HOME=str(root/'cache/pre-commit'),PYTHONNOUSERSITE='1',CI='1',NO_COLOR='1')
for name,text in inputs.items():
 if name=='README.md':continue
 if name=='pyproject.toml.snippet':name='pyproject.toml'
 elif name=='Makefile.snippet':name='Makefile'
 elif name.startswith('schema/'):name='src/'+name
 p=Path(name);p.parent.mkdir(parents=True,exist_ok=True);p.write_text(text)
rows=[]
def snap():return {p.relative_to(project).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in project.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.git','.mypy_cache','.ruff_cache','.pytest_cache','mutants','__pycache__'])}
def run(label,args,code=0,marker=None,unchanged=True,timeout=300):
 before=snap();r=subprocess.run(args,env=env,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=timeout);after=snap();matched=r.returncode==code and (marker is None or marker in r.stdout+r.stderr) and (not unchanged or before==after);rows.append({'label':label,'argv':args,'status':r.returncode,'expected':code,'diagnostic':marker,'stdout':r.stdout,'stderr':r.stderr,'before':before,'after':after,'unchanged_required':unchanged,'matched':matched});(root/'results/checks.json').write_text(json.dumps(rows,indent=2)+'\n');print(label,r.returncode,matched,flush=True);assert matched,(label,(r.stdout+r.stderr)[-8000:]);return r
run('resolved-install-check',['python','-m','pip','check'])
run('deliberate-reference-format',['make','fmt'],unchanged=False)
run('default-lint',['make','lint']);run('default-format',['make','format-check']);run('typed-src-and-tests',['make','typecheck']);run('actual-reference-tests',['make','test']);run('actual-reference-coverage',['make','test-coverage'],unchanged=False);run('actual-reference-graph-audit',['make','sca'],timeout=600)
run('configured-mutation-cli',['mutmut','run','--help'])
p=Path('src/schema/pydantic_typing_probe.py');p.write_text('from schema.example import RawPlayerRecord\nbad = RawPlayerRecord(id=42, name="Chris", position="QB")\n');run('intended-plugin-ctor-typing',['make','typecheck'],2,'[arg-type]');p.unlink()
p=Path('src/security_probe.py');p.write_text('def insecure(value: str) -> object:\n    return eval(value)\n');run('intended-security-diagnostic',['make','lint'],2,'S307');p.unlink()
p=Path('tests/test_assertion_probe.py');p.write_text('def test_c10_intended_failure() -> None:\n    assert False, "C10 intended assertion"\n');run('intended-assertion',['make','test'],2,'C10 intended assertion');p.unlink()
p=Path('src/format_probe.py');p.write_text('def format_probe( )->str:return "probe"\n');run('intended-read-only-format',['make','format-check'],2,'Would reformat');p.unlink()
# Actual default discovery absence, not a passing empty test runner.
p=Path('tests/test_example.py');saved=p.read_bytes();p.unlink();run('default-missing-tests',['make','test'],2,'no tests ran');p.write_bytes(saved)
run('restored-lint',['make','lint']);run('restored-format',['make','format-check']);run('restored-types',['make','typecheck']);run('restored-tests',['make','test']);run('restored-coverage',['make','test-coverage'],unchanged=False)
for label,args in [('git-init',['git','init']),('fixture-name',['git','config','user.name','Bee verification fixture']),('fixture-email',['git','config','user.email','fixture@example.invalid']),('hook-install',[str(c4/'venv/bin/pre-commit'),'install'])]:run(label,args,unchanged=False)
p=Path('src/hook_probe.py');p.write_text('import os\n');run('actual-read-only-ruff-hook',[str(c4/'venv/bin/pre-commit'),'run','ruff-check','--files',str(p)],1,'F401');p.unlink()
p=Path('src/hook_probe.py');p.write_text('def format_probe( )->str:return "probe"\n');run('actual-read-only-format-hook',[str(c4/'venv/bin/pre-commit'),'run','ruff-format-check','--files',str(p)],1,'Would reformat');p.unlink()
p=Path('src/schema/hook_typing_probe.py');p.write_text('from schema.example import RawPlayerRecord\nbad = RawPlayerRecord(id=42, name="Chris", position="QB")\n');run('actual-plugin-hook-reject',[str(c4/'venv/bin/pre-commit'),'run','mypy-project','--files',str(p)],1,'[arg-type]');p.unlink()
Path('.gitignore').write_text('.coverage\n.mypy_cache/\n.ruff_cache/\n.pytest_cache/\n__pycache__/\nmutants/\n')
run('stage-clean-reference',['git','add','.'],unchanged=False);run('ordinary-clean-hooks-commit',['git','commit','-m','fixture: verify Python reference hooks'],unchanged=False,timeout=600)
record={'files':{p.relative_to(project).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'text':p.read_text()} for p in project.rglob('*') if p.is_file() and p.suffix!='.pyc' and not any(x in p.parts for x in ['.git','.mypy_cache','.ruff_cache','.pytest_cache','__pycache__','mutants']) and p.name!='.coverage'},'scope':'Selected Python3.13/Linux venv/graph/schema/typed ctor/tests/hooks; not authenticated approval/containment/auth/persistence/full scanning/all platforms or mandatory mutation.'};(root/'results/final.json').write_text(json.dumps(record,indent=2)+'\n')
