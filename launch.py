from pathlib import Path
import subprocess,sys,time,urllib.request,json
root=Path(__file__).resolve().parent
url='http://127.0.0.1:19826'
def ready():
 try:
  with urllib.request.urlopen(url+'/api/data',timeout=1) as r:return json.loads(r.read()).get('schemaVersion')==1
 except Exception:return False
if not ready():
 subprocess.run([sys.executable,str(root/'init_data.py')],check=True)
 log=open(root/'data/server.log','a')
 subprocess.Popen([sys.executable,str(root/'server.py')],cwd=root,stdin=subprocess.DEVNULL,stdout=log,stderr=log,start_new_session=True)
 for _ in range(30):
  if ready():break
  time.sleep(.2)
if not ready():raise SystemExit('工作台未能启动，请查看 data/server.log')
if '--no-open' not in sys.argv:__import__('webbrowser').open(url)
print(url)
