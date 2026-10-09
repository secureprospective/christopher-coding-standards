"""Explicit synthetic module-specific decoder/validation/constructor/effect caller."""
from pathlib import Path
import json,os,platform,subprocess,hashlib
assert platform.node()=='claudeos' and os.getuid()==1000
root=Path.home()/'coding-standards-verification/bee-c9-2026-10-09';project=root/'project';os.chdir(project);c5=root.parent/'bee-c5-2026-10-08'
env=os.environ.copy();env.update(PATH=str(root/'tools/go/bin')+':'+str(root/'bin')+':'+str(c5/'bin')+':'+env['PATH'],GOENV='off',GOTOOLCHAIN='local',GOCACHE=str(root/'cache/go-build'),GOMODCACHE=str(root/'cache/go-mod'),GOPATH=str(root/'cache/gopath'),GOPROXY='https://proxy.golang.org',GOFLAGS='-mod=readonly',CI='1',NO_COLOR='1')
p=Path('internal/boundary/caller_test.go');p.parent.mkdir();p.write_text('''package boundary_test
import (
 "strings"
 "testing"
 "example.com/consumer/internal/playerid"
 "example.com/consumer/internal/schema"
)
// Explicit synthetic consumer callback; no persistence/authentication supplied.
func TestSyntheticDecoderConstructorEffect(t *testing.T) {
 var effects []playerid.PlayerID
 receive := func(payload string) {
  raw, err := schema.DecodePlayerRecord(strings.NewReader(payload)); if err != nil { return }
  if err := raw.Validate(); err != nil { return }
  id, err := playerid.New(raw.ID); if err != nil { return }
  effects = append(effects, id)
 }
 valid := `{"id":"99","name":"Chris","position":"QB"}`
 for _, bad := range []string{"null",valid+"{}",`{"id":"-99","name":"Chris","position":"QB"}`,`{"id":"99","name":"Chris","position":"QB","salary":"NaN"}`} { receive(bad) }
 if len(effects)!=0 { t.Fatal("C9 effect on invalid input") }
 receive(valid)
 if len(effects)!=1 || effects[0].String()!="0099" { t.Fatal("C9 canonical valid effect missing") }
}
''');subprocess.run(['gofmt','-w',str(p)],env=env,check=True)
rows=[]
def snap():return {p.relative_to(project).as_posix():hashlib.sha256(p.read_bytes()).hexdigest() for p in project.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.git','bin'])}
for label,args in [('uncached-synthetic-integration',['go','test','-race','-count=1','-v','./...']),('integration-source-lint',['make','lint']),('integration-source-format',['make','format-check'])]:
 before=snap();r=subprocess.run(args,env=env,stdin=subprocess.DEVNULL,capture_output=True,text=True,timeout=600);rows.append({'label':label,'argv':args,'status':r.returncode,'stdout':r.stdout,'stderr':r.stderr,'before':before,'after':snap()});(root/'results/integration.json').write_text(json.dumps(rows,indent=2)+'\n');print(label,r.returncode,flush=True);assert r.returncode==0 and before==snap(),(label,r.stdout+r.stderr)
prior=json.loads((root/'results/final-candidate.json').read_text());prior['files']={p.relative_to(project).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'text':p.read_text()} for p in project.rglob('*') if p.is_file() and not any(x in p.parts for x in ['.git','bin'])};(root/'results/final-candidate.json').write_text(json.dumps(prior,indent=2)+'\n')
