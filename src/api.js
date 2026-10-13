export const priorities=['优先拍','备选','暂缓','待评估'];
export const priorityOf=t=>priorities.includes(t.priority)?t.priority:'待评估';
export const comparePriority=(a,b)=>priorities.indexOf(priorityOf(a))-priorities.indexOf(priorityOf(b))||(a.priorityOrder??999)-(b.priorityOrder??999);
export const states=['选题库','聊想法','写稿中','待拍','已拍'];
export const categories=['AI与工作','商业与产品','职场与沟通','成长与生活','关系与边界','哲学与思维'];
export async function request(path,body){const r=await fetch(path,{method:body?'POST':'GET',headers:body?{'Content-Type':'application/json'}:{},body:body?JSON.stringify(body):undefined});const d=await r.json();if(!r.ok)throw new Error(d.error||'连接失败');return d;}
export function newTopic(){return {id:'',revision:0,title:'',category:'成长与生活',status:'选题库',priority:'待评估',priorityReason:'',priorityNext:'',prioritySignal:'尚未评估',priorityOrder:999,original:'',hook:'',angle:'',notes:'',script:'',questions:[],evidence:[],related:[],history:[]};}
export function conversation(t,p){return `我们继续聊这个选题：${t.title}\n选题编号：${t.id}\n\n我的原话：\n${t.original}\n\n补充想法：\n${t.notes||'暂未补充'}\n\n候选开场：\n${t.hook}\n\n讨论方向：\n${t.angle}\n\n先聊的问题：\n${t.questions.join('\n')}\n\n参考资料：\n${t.evidence.map(e=>`${e.title}\n${e.statement}\n${e.limit||''}\n${e.url||''}`).join('\n\n')}\n\n写作偏好：${p.voice}\n少用：${p.avoid}\n先围绕我的经历和判断追问，一次一两个问题。结合来回对话再写口播，不要编造我的经历。将补充信息和稿件同步到本地创作工作台中这条选题。`;}
