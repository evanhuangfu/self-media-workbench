"""Independent, evidence-aware publication ledger; callers hold server.LOCK."""
import json, os, uuid
from pathlib import Path
from datetime import datetime, timezone
from urllib.parse import urlparse
PLATFORMS=['抖音','小红书','哔哩哔哩','YouTube','X','视频号','公众号','LinkedIn']
STATUSES=['published','draft','scheduled','unknown','unpublished']
def timestamp(): return datetime.now(timezone.utc).isoformat()
def load(path):
 return json.loads(path.read_text()) if path.exists() else {'schemaVersion':1,'revision':0,'works':[],'publications':[],'coverage':[]}
def validate(d,topic_ids):
 works=d['works']; pubs=d['publications']
 if len({w['id'] for w in works})!=len(works):raise ValueError('作品编号重复')
 ids={w['id'] for w in works}
 for w in works:
  if not w.get('title','').strip():raise ValueError('请填写作品名称')
  if w.get('topicId') and w['topicId'] not in topic_ids:raise ValueError('关联选题不存在')
 seen=set();urls=set()
 for p in pubs:
  if p['id'] in seen:raise ValueError('发布编号重复')
  seen.add(p['id'])
  if p.get('workId') not in ids:raise ValueError('发布记录未关联作品')
  if p.get('platform') not in PLATFORMS or p.get('status') not in STATUSES:raise ValueError('平台或发布状态无效')
  if p.get('verification') not in ['verified','pending']:raise ValueError('核实状态无效')
  u=p.get('url','')
  if u and (urlparse(u).scheme not in ['http','https'] or not urlparse(u).netloc):raise ValueError('作品链接格式错误')
  if u:
   key=(p['platform'],u.rstrip('/'))
   if key in urls:raise ValueError('同一平台作品链接重复，请编辑原记录')
   urls.add(key)
  if p.get('publishedAt'):
   dt=datetime.fromisoformat(p['publishedAt'].replace('Z','+00:00'))
   if dt.tzinfo is None:raise ValueError('发布时间须包含时区')
  if p['status']=='published' and p['verification']=='verified' and (not u or not p.get('evidence')):raise ValueError('确认已发需作品链接与核实依据')
def save(path,d):
 path.parent.mkdir(parents=True,exist_ok=True)
 if path.exists():
  backup=path.parent/'publication-backups';backup.mkdir(exist_ok=True)
  (backup/(datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'.json')).write_text(path.read_text())
  for p in sorted(backup.glob('*.json'))[:-30]:p.unlink()
 d['revision']=d.get('revision',0)+1;d['updatedAt']=timestamp()
 tmp=path.with_suffix('.tmp');tmp.write_text(json.dumps(d,ensure_ascii=False,indent=2));os.replace(tmp,path)
def merge(d,b):
 for field in ['works','publications']:
  old={x['id']:x for x in d[field]}
  for x in b.get(field,[]):old[x['id']]={**old.get(x['id'],{}),**x}
  d[field]=list(old.values())
 if 'coverage' in b:d['coverage']=b['coverage']
 return d
