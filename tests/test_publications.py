import unittest,sys,tempfile,json,subprocess,os,time,urllib.request,urllib.error,socket
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
import publication_store as l
class LedgerTest(unittest.TestCase):
 def test_evidence_and_duplicates(self):
  d={'works':[{'id':'w','title':'作品'}],'publications':[{'id':'p','workId':'w','platform':'抖音','status':'published','verification':'verified','url':'https://www.douyin.com/video/1','evidence':'后台核实'}]}
  l.validate(d,set())
  d['publications'].append({**d['publications'][0],'id':'p2'})
  with self.assertRaises(ValueError):l.validate(d,set())
  d['publications']=d['publications'][:1];d['publications'][0]['evidence']=''
  with self.assertRaises(ValueError):l.validate(d,set())
 def test_import_preserves_and_is_idempotent(self):
  d={'works':[{'id':'w','title':'作品','topicId':'t','note':'保留'}],'publications':[],'revision':0}
  b={'works':[{'id':'w','title':'新标题'}]};l.merge(d,b);l.merge(d,b)
  self.assertEqual(len(d['works']),1);self.assertEqual(d['works'][0]['note'],'保留')
  with tempfile.TemporaryDirectory() as td:
   path=Path(td)/'publications.json';l.save(path,d);l.save(path,d)
   self.assertEqual(l.load(path)['revision'],2);self.assertEqual(len(list((Path(td)/'publication-backups').glob('*'))),1)
 def test_http_persistence_and_revision(self):
  with tempfile.TemporaryDirectory() as td:
   root=Path(__file__).resolve().parents[1];dest=Path(td)/'topics.json';dest.write_text(json.dumps({'topics':[], 'preferences':{}}));before=dest.read_text()
   sock=socket.socket();sock.bind(('127.0.0.1',0));port=sock.getsockname()[1];sock.close()
   p=subprocess.Popen([sys.executable,str(root/'server.py')],env={**os.environ,'STUDIO_DATA':str(dest),'STUDIO_PORT':str(port)},stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL)
   def req(path,body=None):
    r=urllib.request.Request('http://127.0.0.1:'+str(port)+path,data=json.dumps(body).encode() if body else None,headers={'Content-Type':'application/json'})
    return json.load(urllib.request.urlopen(r,timeout=5))
   try:
    for _ in range(100):
     try:d=req('/api/publications');break
     except OSError:time.sleep(.1)
    body={'works':[{'id':'w','title':'测试'}],'publications':[{'id':'p','workId':'w','platform':'X','status':'draft','verification':'pending'}]}
    result=req('/api/publications/import',body);self.assertEqual(len(result['publications']),1)
    result=req('/api/publications/import',body);self.assertEqual(len(result['publications']),1)
    with self.assertRaises(urllib.error.HTTPError) as e:req('/api/publications/save',{**body,'revision':0})
    self.assertEqual(e.exception.code,409);self.assertEqual(dest.read_text(),before)
    self.assertEqual(req('/api/publications')['revision'],2)
   finally:p.terminate();p.wait(timeout=10)
if __name__=='__main__':unittest.main()
