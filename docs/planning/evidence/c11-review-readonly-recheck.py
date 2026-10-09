"""Docs-only structural evidence, not an unbuilt adoption checker or product tests."""
from pathlib import Path
import hashlib,json,re,subprocess
root=Path('/home/chris/work/christopher-coding-standards');files=['docs/adoption-status.md','docs/INDEX.md','skills/adopt-coding-standards/SKILL.md','docs/planning/c11-tracking-decision.md','docs/planning/c11-scope.md'];text={p:(root/p).read_text() for p in files}
def structure(d):
 assert 'Tracking implementation is deferred' in d['docs/adoption-status.md'],'missing explicit deferral'
 assert 'adoption-status.md' in d['docs/INDEX.md'],'missing index route'
 assert '../../docs/adoption-status.md' in d['skills/adopt-coding-standards/SKILL.md'],'missing skill route'
 for s in ['Unknown/missing','Customized / review needed','Mixed bindings','No destructive update','not executed checker fixtures','No live consumers']:
  assert s in d['docs/adoption-status.md'],s
 assert 'do not build or enroll' in d['docs/planning/c11-tracking-decision.md'],'missing implementation boundary'
 assert 'still unselected' in d['docs/planning/c11-tracking-decision.md'],'missing unselected inputs'
structure(text);links=[]
for p,s in text.items():
 for url in re.findall(r'\[[^\]]*\]\(([^)]+)\)',s):
  if url.startswith(('http:','https:','#')):continue
  q=(root/p).parent/url.split('#')[0];assert q.exists(),(p,url);links.append({'source':p,'target':url})
negatives=[]
for label,path,old,new in [('missing-index-route','docs/INDEX.md','adoption-status.md','missing-status.md'),('missing-skill-route','skills/adopt-coding-standards/SKILL.md','../../docs/adoption-status.md','missing-status.md'),('missing-deferral','docs/adoption-status.md','Tracking implementation is deferred','Tracking implementation selected')]:
 d=text.copy();d[path]=d[path].replace(old,new)
 try:structure(d)
 except AssertionError as e:negatives.append({'label':label,'expected':'structural rejection','actual':str(e)})
 else:raise AssertionError('unexpected structural green '+label)
b=json.loads((root/'docs/planning/c11-baseline.json').read_text());owned=set(files+['HANDOFF.md']);protected=[r for r in b['files'] if r['path'] not in owned]
for r in protected:assert hashlib.sha256((root/r['path']).read_bytes()).hexdigest()==r['sha256'],r['path']
assert hashlib.sha256((root/'.project.yaml').read_bytes()).hexdigest()==b['unrelated_project_sha256'];assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()==b['base']
record={'base':b['base'],'source':[{'path':p,'sha256':hashlib.sha256((root/p).read_bytes()).hexdigest()} for p in files],'links':links,'in_memory_doc_negatives':negatives,'protected_count':len(protected),'operational_change':'none; only declared doc source changed against baseline','limits':'Local docs structure/link/routing/protected checks, no actual checker/runtime/consumer/network/enrollment/approval/containment tests. Manual examples are reporting judgments, not executable status fixtures.'};assert (root/'docs/planning/evidence/c11-doc-checks.json').read_text() == json.dumps(record,indent=2)+'\n', 'frozen record differs';print(json.dumps(record,indent=2))
