"""Official owned Go/linter setup; ClaudeOS only, no bootstrap/global changes."""
from pathlib import Path
import json,os,platform,urllib.request,tarfile,hashlib,subprocess
assert platform.node()=='claudeos' and os.getuid()==1000
root=Path.home()/'coding-standards-verification/bee-c9-2026-10-09';root.mkdir()
for d in ['bin','downloads','tools','results','project','cache']:(root/d).mkdir()
records=[]
def fetch(url):
 d=json.load(urllib.request.urlopen(urllib.request.Request(url,headers={'User-Agent':'Bee-standards-C9'}),timeout=60));records.append({'url':url,'record':d});(root/'results/metadata.json').write_text(json.dumps(records,indent=2)+'\n');return d
versions=fetch('https://go.dev/dl/?mode=json');selected=[v for v in versions if v['version']=='go1.27.2'];assert len(selected)==1
asset=[a for a in selected[0]['files'] if a['filename']=='go1.27.2.linux-amd64.tar.gz'];assert len(asset)==1;asset=asset[0]
def download(url,name,expected):
 b=urllib.request.urlopen(url,timeout=180).read();digest=hashlib.sha256(b).hexdigest();assert digest==expected,(name,digest,expected);p=root/'downloads'/name;p.write_bytes(b);return p
p=download('https://go.dev/dl/'+asset['filename'],asset['filename'],asset['sha256'])
with tarfile.open(p) as t:t.extractall(root/'tools',filter='data')
release=fetch('https://api.github.com/repos/golangci/golangci-lint/releases/tags/v2.14.0');assets=[a for a in release['assets'] if a['name'].endswith('.tar.gz') and ('linux-amd64' in a['name'] or 'linux_amd64' in a['name'])];assert len(assets)==1;lint=assets[0];assert lint['digest'].startswith('sha256:');p=download(lint['browser_download_url'],lint['name'],lint['digest'].removeprefix('sha256:'))
with tarfile.open(p) as t:
 names=[m for m in t.getmembers() if m.isfile() and m.name.endswith('/golangci-lint')];assert len(names)==1;(root/'bin/golangci-lint').write_bytes(t.extractfile(names[0]).read())
(root/'bin/golangci-lint').chmod(0o755)
env=os.environ.copy();env.update(GOENV='off',GOTOOLCHAIN='local',GOCACHE=str(root/'cache/go-build'),GOMODCACHE=str(root/'cache/go-mod'),GOPATH=str(root/'cache/gopath'))
record={'host':platform.node(),'uid':os.getuid(),'go':subprocess.check_output([str(root/'tools/go/bin/go'),'version'],env=env,text=True).strip(),'golangci':subprocess.check_output([str(root/'bin/golangci-lint'),'version'],env=env,text=True).strip(),'go_archive_sha256':asset['sha256'],'linter_archive_sha256':lint['digest'],'linter_binary_sha256':hashlib.sha256((root/'bin/golangci-lint').read_bytes()).hexdigest(),'scope':'Official publisher hashes checked; not independent signature/approval or sandbox. Owned binaries/config/cache only. Go auto-toolchain disabled, no sudo/global/system/GUI/computer-use changes.'}
(root/'results/environment.json').write_text(json.dumps(record,indent=2)+'\n');print(json.dumps(record,indent=2))
