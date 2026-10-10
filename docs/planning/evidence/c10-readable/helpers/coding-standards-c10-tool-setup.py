"""Task-owned binary-wheel Python reference, publisher-hash checked; ClaudeOS only."""
from pathlib import Path
import os,platform,json,subprocess,hashlib,urllib.request
assert platform.node()=='claudeos' and os.getuid()==1000
root=Path.home()/'coding-standards-verification/bee-c10-2026-10-09';download=root/'downloads';download.mkdir();(root/'project with spaces').mkdir();(root/'cache').mkdir()
env=os.environ.copy();env.update(PIP_CONFIG_FILE='/dev/null',PIP_CACHE_DIR=str(root/'cache/pip'),PIP_INDEX_URL='https://pypi.org/simple',PIP_DISABLE_PIP_VERSION_CHECK='1',XDG_CACHE_HOME=str(root/'cache/xdg'),XDG_CONFIG_HOME=str(root/'cache/config'),PYTHONNOUSERSITE='1')
versions={'ruff':'0.16.0','mypy':'2.3.0','pydantic':'2.14.0','pytest':'9.1.1','pytest-cov':'7.1.0','pip-audit':'2.10.1','mutmut':'3.8.0'}
r=subprocess.run(['python3','-m','venv',str(root/'venv')],env=env,capture_output=True,text=True,check=True);python=root/'venv/bin/python'
r=subprocess.run([str(python),'-m','pip','download','--only-binary=:all:','--dest',str(download),*[f'{k}=={v}' for k,v in versions.items()]],env=env,capture_output=True,text=True);(root/'results/download.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
records=[];lines=[]
for wheel in sorted(download.glob('*.whl')):
 name,version,*_=wheel.name.split('-');url=f'https://pypi.org/pypi/{name}/{version}/json';metadata=json.load(urllib.request.urlopen(url,timeout=60));assets=[a for a in metadata['urls'] if a['filename']==wheel.name];assert len(assets)==1;digest=hashlib.sha256(wheel.read_bytes()).hexdigest();assert digest==assets[0]['digests']['sha256'];lines.append(f'{name}=={version} --hash=sha256:{digest}');records.append({'url':url,'name':name,'version':version,'filename':wheel.name,'sha256':digest,'publisher_asset':assets[0]})
lock='# Selected Linux x86_64 / CPython3.13 reference wheel graph. Not universal platform locks.\n'+'\n'.join(lines)+'\n';(root/'results/requirements-reference.lock').write_text(lock);(root/'results/wheel-verification.json').write_text(json.dumps(records,indent=2)+'\n')
r=subprocess.run([str(python),'-m','pip','install','--no-index','--find-links',str(download),'--require-hashes','-r',str(root/'results/requirements-reference.lock')],env=env,capture_output=True,text=True);(root/'results/install.log').write_text(r.stdout+r.stderr);assert r.returncode==0,r.stderr
versions_actual={}
for name in ['ruff','mypy','pytest','pip-audit']:
 r=subprocess.run([str(root/'venv/bin'/name),'--version'],env=env,capture_output=True,text=True,check=True);versions_actual[name]=r.stdout+r.stderr
for args in [['mutmut','--help'],['mutmut','run','--help'],['mutmut','results','--help'],['mutmut','junitxml','--help']]:
 r=subprocess.run([str(root/'venv/bin'/args[0]),*args[1:]],env=env,capture_output=True,text=True);(root/'results'/('-'.join(args[:-1])+'-help.json')).write_text(json.dumps({'argv':args,'status':r.returncode,'stdout':r.stdout,'stderr':r.stderr},indent=2)+'\n')
record={'host':platform.node(),'uid':os.getuid(),'python':platform.python_version(),'versions':versions_actual,'pydantic':subprocess.check_output([str(python),'-c','import pydantic; print(pydantic.__version__)'],env=env,text=True).strip(),'scope':'Owned venv/cache and binary wheels only; each selected wheel SHA matches publisher PyPI metadata then offline hash-required install. Not independent signature/approval, sandbox, pristine VM or all platforms. No sudo/global/system/GUI/identity changes.'};(root/'results/environment.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
