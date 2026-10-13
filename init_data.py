from pathlib import Path
import json
p=Path(__file__).resolve().parent/'data/topics.json'
p.parent.mkdir(exist_ok=True)
if not p.exists():
 p.write_text(json.dumps({'schemaVersion':1,'topics':[], 'preferences':{'voice':'','avoid':'','workflow':'','evidence':''},'updatedAt':None},ensure_ascii=False,indent=2))
print('数据目录已准备')
