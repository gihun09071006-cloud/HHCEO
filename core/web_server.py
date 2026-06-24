from fastapi import FastAPI
from fastapi.responses import HTMLResponse
import aiosqlite
from core import database as db

app = FastAPI()

HTML = r"""<!DOCTYPE html>
<html lang="ko">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>DANTE CORPORATION</title>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
*{margin:0;padding:0;box-sizing:border-box}
body{background:#1a1a2e;display:flex;flex-direction:column;height:100vh;overflow:hidden;font-family:'Press Start 2P',monospace}

/* TOP BAR */
#topbar{background:#0d0d1f;border-bottom:2px solid #00ff41;padding:6px 16px;display:flex;align-items:center;gap:12px;flex-shrink:0;box-shadow:0 0 20px rgba(0,255,65,.15)}
#logo{font-size:11px;color:#ffd700;text-shadow:0 0 10px #ffd700;letter-spacing:2px}
.chip{font-size:6px;padding:3px 8px;border:1px solid #00ff41;color:#00ff41}
.chip.g{border-color:#ffd700;color:#ffd700}
.chip.c{border-color:#00b4d8;color:#00b4d8}
.chip.r{border-color:#ff6b35;color:#ff6b35}
#xpwrap{flex:1;max-width:160px}
#xplabel{font-size:5px;color:#2a4a2a;margin-bottom:2px}
#xpbg{height:8px;background:#111;border:1px solid #00ff41}
#xpfill{height:100%;background:#ffd700;box-shadow:0 0 6px #ffd700;transition:width .8s}
.blink{animation:bl 1s step-end infinite}
@keyframes bl{50%{opacity:0}}
.ldot{display:inline-block;width:7px;height:7px;background:#ff0055;border-radius:50%;margin-right:4px;animation:pu 1s ease-in-out infinite;box-shadow:0 0 6px #ff0055}
@keyframes pu{0%,100%{transform:scale(1)}50%{transform:scale(1.5);opacity:.5}}

/* MAIN */
#main{display:flex;flex:1;overflow:hidden}

/* LEFT PANEL */
#leftpanel{width:280px;background:#0a0a18;border-right:2px solid #1a1a3a;display:flex;flex-direction:column;flex-shrink:0}
#lptitle{font-size:7px;color:#00b4d8;padding:8px 10px;border-bottom:1px solid #1a1a3a;letter-spacing:2px}
#feed{flex:1;overflow-y:auto;padding:6px}
#feed::-webkit-scrollbar{width:3px}
#feed::-webkit-scrollbar-thumb{background:#00ff41}
.msg{margin-bottom:8px;padding:6px;background:#0d0d22;border-left:2px solid}
.msg-agent{font-size:6px;margin-bottom:3px}
.msg-text{font-size:5px;color:#4a6a5a;line-height:1.8}
.msg.CEO{border-color:#ffd700}.msg.CEO .msg-agent{color:#ffd700}
.msg.Research{border-color:#00b4d8}.msg.Research .msg-agent{color:#00b4d8}
.msg.Analysis{border-color:#9d4edd}.msg.Analysis .msg-agent{color:#9d4edd}
.msg.Finance{border-color:#06d6a0}.msg.Finance .msg-agent{color:#06d6a0}
.msg.Risk{border-color:#ff6b35}.msg.Risk .msg-agent{color:#ff6b35}
.msg.Execution{border-color:#ef233c}.msg.Execution .msg-agent{color:#ef233c}
.msg.Product{border-color:#ff85a1}.msg.Product .msg-agent{color:#ff85a1}
#projpanel{border-top:1px solid #1a1a3a;padding:8px}
.ptitle{font-size:6px;color:#00b4d8;margin-bottom:6px}
.prow{margin-bottom:8px}
.pname{font-size:5px;color:#ffd700;margin-bottom:3px}
.pbg{height:6px;background:#111;border:1px solid #1a1a3a}
.pbar{height:100%;transition:width 1s}
.ppct{font-size:4px;color:#2a2a4a;text-align:right;margin-top:1px}

/* CANVAS AREA */
#canvaswrap{flex:1;display:flex;align-items:stretch;position:relative;overflow:hidden}
#c{display:block;width:100%;height:100%}

/* TICKER */
#ticker{position:fixed;bottom:0;left:0;right:0;background:#07070f;border-top:1px solid #00ff41;padding:3px 10px;font-size:5px;color:#00ff41;overflow:hidden;white-space:nowrap}
#tkt{display:inline-block;animation:sc 40s linear infinite}
@keyframes sc{from{transform:translateX(100vw)}to{transform:translateX(-100%)}}
</style>
</head>
<body>

<div id="topbar">
  <span id="logo">⬛ DANTE CORP</span>
  <span style="font-size:6px;color:#ff0055"><span class="ldot"></span>LIVE</span>
  <span class="chip g" id="s-lv">LV.1</span>
  <span class="chip c" id="s-day">DAY 1</span>
  <span class="chip" id="s-ag">7 AGENTS</span>
  <span class="chip r" id="s-hp">HP 81</span>
  <div id="xpwrap">
    <div id="xplabel">XP 580/1000</div>
    <div id="xpbg"><div id="xpfill" style="width:58%"></div></div>
  </div>
  <span class="blink" style="font-size:8px;color:#00ff41">█</span>
</div>

<div id="main">
  <div id="leftpanel">
    <div id="lptitle">◈ ACTIVITY FEED</div>
    <div id="feed"></div>
    <div id="projpanel">
      <div class="ptitle">◈ PROJECTS</div>
      <div id="pc"></div>
    </div>
  </div>
  <div id="canvaswrap">
    <canvas id="c"></canvas>
  </div>
</div>

<div id="ticker"><span id="tkt">⬛ DANTE CORPORATION AUTONOMOUS AI OS v1.0 &nbsp;&nbsp;&nbsp; ◈ ALL SYSTEMS OPERATIONAL &nbsp;&nbsp;&nbsp; ◈ GROQ ENGINE ONLINE &nbsp;&nbsp;&nbsp; ◈ 7 AGENTS ACTIVE &nbsp;&nbsp;&nbsp; ◈ 2 PROJECTS IN PROGRESS &nbsp;&nbsp;&nbsp;</span></div>

<script>
const canvas = document.getElementById('c');
const ctx = canvas.getContext('2d');
ctx.imageSmoothingEnabled = false;

// --- Color palette ---
const C = {
  floor:'#c8956c', floorLine:'#b8844c', floorDark:'#b07840',
  wall:'#3a2818', wallTop:'#2a1c10',
  deskTop:'#a07040', deskEdge:'#704820',
  chair:'#3a5a8a', chairDark:'#2a4a7a',
  monitor:'#1a1a2e', screen:'#00b4d8',
  sofa:'#6a3a8a', sofaDark:'#4a2a6a',
  tableTop:'#6a4020', tableDark:'#3a2010',
  win:'#87ceeb', winFrame:'#5a4030',
  plant:'#2a7a2a', plantDark:'#1a5a1a', pot:'#c06030',
  book:['#cc4444','#44cc44','#4444cc','#cccc44','#cc44cc','#44cccc'],
};

const AGENT_COL = {
  CEO:'#ffd700', Research:'#00b4d8', Analysis:'#9d4edd',
  Finance:'#06d6a0', Risk:'#ff6b35', Execution:'#ef233c', Product:'#ff85a1'
};

// Room positions on canvas (will be scaled)
const ROOM_POS = {
  'Strategic Command Room':  {x:0.10, y:0.18},
  'Brainstorming Room':      {x:0.35, y:0.50},
  'Research Department':     {x:0.52, y:0.18},
  'Analysis Lab':            {x:0.73, y:0.18},
  'Finance Desk':            {x:0.10, y:0.75},
  'Meeting Room':            {x:0.35, y:0.75},
  'Development Room':        {x:0.60, y:0.75},
  'Risk Assessment Room':    {x:0.85, y:0.50},
};

// Agent state for animation
let agentStates = {};
let tick = 0;
let W, H;

function resize() {
  const wrap = document.getElementById('canvaswrap');
  W = wrap.clientWidth;
  H = wrap.clientHeight;
  canvas.width = W;
  canvas.height = H;
}
window.addEventListener('resize', resize);
resize();

// ---- DRAW FUNCTIONS ----

function fillRect(x,y,w,h,col){ctx.fillStyle=col;ctx.fillRect(x,y,w,h)}

function drawFloor(){
  fillRect(32,40,W-64,H-80,C.floor);
  ctx.strokeStyle=C.floorLine;ctx.lineWidth=1;ctx.globalAlpha=.35;
  for(let y=40;y<H-40;y+=20){ctx.beginPath();ctx.moveTo(32,y);ctx.lineTo(W-32,y);ctx.stroke();}
  ctx.globalAlpha=.1;
  for(let x=32;x<W-32;x+=60){ctx.beginPath();ctx.moveTo(x,40);ctx.lineTo(x,H-40);ctx.stroke();}
  ctx.globalAlpha=1;
}

function drawWalls(){
  fillRect(0,0,W,40,C.wallTop);
  fillRect(0,0,32,H,C.wall);
  fillRect(W-32,0,32,H,C.wall);
  fillRect(0,H-40,W,40,C.wall);
  // Windows
  const wpos=[0.12,0.28,0.44,0.60,0.76];
  wpos.forEach(p=>{
    const wx=W*p, wy=2, ww=W*0.1, wh=34;
    fillRect(wx,wy,ww,wh,C.winFrame);
    fillRect(wx+3,wy+3,ww-6,wh-6,C.win);
    ctx.strokeStyle=C.winFrame;ctx.lineWidth=1.5;
    ctx.beginPath();ctx.moveTo(wx+ww/2,wy+3);ctx.lineTo(wx+ww/2,wy+wh-3);ctx.stroke();
    ctx.beginPath();ctx.moveTo(wx+3,wy+wh/2);ctx.lineTo(wx+ww-3,wy+wh/2);ctx.stroke();
    // skyline
    ctx.fillStyle='rgba(20,20,50,.55)';
    const bx=wx+4;
    [[0,10,8],[10,6,6],[18,14,10],[32,8,6],[42,4,10]].forEach(([ox,bh,bw])=>{
      ctx.fillRect(bx+ox,wy+wh-3-bh,bw,bh);
    });
  });
}

function drawDesk(x,y,w,h){
  fillRect(x+3,y+3,w,h,'rgba(0,0,0,.25)');
  fillRect(x,y,w,h,C.deskTop);
  fillRect(x,y+h-5,w,5,C.deskEdge);
  fillRect(x+w-5,y,5,h,C.deskEdge);
}

function drawMonitor(x,y,scale=1){
  const sw=Math.floor(28*scale),sh=Math.floor(20*scale);
  fillRect(x+sw/2-3,y+sh,6,7,'#555');
  fillRect(x+sw/2-8,y+sh+6,16,3,'#444');
  fillRect(x,y,sw,sh,C.monitor);
  fillRect(x+2,y+2,sw-4,sh-4,C.screen);
  ctx.fillStyle='rgba(0,255,200,.5)';
  ctx.fillRect(x+4,y+6,Math.floor(sw*.3),1);
  ctx.fillRect(x+4,y+9,Math.floor(sw*.45),1);
  ctx.fillRect(x+4,y+12,Math.floor(sw*.25),1);
}

function drawChair(x,y,col='#3a5a8a'){
  fillRect(x-10,y-14,20,6,col);
  fillRect(x-9,y-8,18,16,col);
  ctx.fillStyle='rgba(0,0,0,.2)';ctx.fillRect(x-9,y-8,18,2);
  fillRect(x-12,y+8,5,5,'#222');fillRect(x+7,y+8,5,5,'#222');
}

function drawConferenceTable(x,y,w,h){
  fillRect(x+4,y+5,w,h,'rgba(0,0,0,.3)');
  fillRect(x,y,w,h,C.tableTop);
  fillRect(x+3,y+2,w-6,6,'rgba(255,255,255,.08)');
  fillRect(x+6,y+h-4,10,4,C.tableDark);
  fillRect(x+w-16,y+h-4,10,4,C.tableDark);
}

function drawBookshelf(x,y,w,h){
  fillRect(x,y,w,h,'#5a3a1a');
  for(let sy=y+6;sy<y+h-6;sy+=28){
    let bx=x+3;
    let bi=0;
    while(bx<x+w-3){
      const bw=Math.max(5,((bx*13+sy*7)%6)+5);
      const bh=22;
      ctx.fillStyle=C.book[(bi++)%C.book.length];
      ctx.fillRect(bx,sy+2,Math.min(bw,x+w-3-bx),bh);
      bx+=bw+1;
    }
    fillRect(x,sy+24,w,3,'#3a2010');
  }
}

function drawPlant(x,y){
  fillRect(x-8,y,16,16,C.pot);fillRect(x-6,y-2,12,4,C.pot);
  ctx.fillStyle=C.plant;ctx.beginPath();ctx.arc(x,y-10,12,0,Math.PI*2);ctx.fill();
  ctx.fillStyle=C.plantDark;ctx.beginPath();ctx.arc(x-8,y-14,8,0,Math.PI*2);ctx.fill();
  ctx.fillStyle='#3a9a3a';ctx.beginPath();ctx.arc(x+7,y-16,9,0,Math.PI*2);ctx.fill();
}

function drawSofa(x,y,w){
  fillRect(x+3,y+3,w,30,'rgba(0,0,0,.2)');
  fillRect(x,y-14,w,16,C.sofa);
  fillRect(x,y,w,28,C.sofa);
  fillRect(x,y,14,28,C.sofaDark);
  fillRect(x+w-14,y,14,28,C.sofaDark);
  fillRect(x+16,y+4,(w-32)/2-2,20,'#7a4a9a');
  fillRect(x+16+(w-32)/2+2,y+4,(w-32)/2-2,20,'#7a4a9a');
}

function drawTV(x,y,w=64,h=40){
  fillRect(x+2,y+2,w,h,'rgba(0,0,0,.4)');
  fillRect(x,y,w,h,'#1a1a1a');
  fillRect(x+3,y+3,w-6,h-6,'#0a0a14');
  // Chart
  const bars=[[6,12],[14,8],[22,16],[30,6],[38,18],[46,10],[54,14]];
  bars.forEach(([bx,bh])=>{
    ctx.fillStyle='#00ff4188';
    ctx.fillRect(x+bx,y+h-8-bh,6,bh);
  });
  ctx.strokeStyle='#ffd700';ctx.lineWidth=1.5;
  ctx.beginPath();
  [[6,10],[14,14],[22,6],[30,12],[38,4],[46,10],[54,8]].forEach(([bx,by],i)=>{
    i===0?ctx.moveTo(x+bx+3,y+h-8-by):ctx.lineTo(x+bx+3,y+h-8-by);
  });
  ctx.stroke();
}

function drawWaterCooler(x,y){
  fillRect(x-8,y,16,30,'#aaa');
  fillRect(x-6,y+4,12,20,'#4af');
  ctx.fillStyle='#6af';ctx.beginPath();ctx.arc(x,y,8,0,Math.PI*2);ctx.fill();
  fillRect(x-3,y+28,6,6,'#888');
}

function drawFurniture(){
  const sw=W-64, sh=H-80;
  const sx=32, sy=40;

  // CEO desk (top-left)
  drawDesk(sx+20,sy+20,Math.floor(sw*.18),Math.floor(sh*.2));
  drawMonitor(sx+28,sy+26,1.1);
  drawMonitor(sx+65,sy+26,1.1);
  drawChair(sx+Math.floor(sw*.09),sy+Math.floor(sh*.22),'#2a4a7a');

  // Conference table (center)
  const cw=Math.floor(sw*.3),ch=Math.floor(sh*.25);
  const cx=sx+Math.floor(sw*.25),cy=sy+Math.floor(sh*.35);
  drawConferenceTable(cx,cy,cw,ch);
  for(let i=0;i<3;i++){
    drawChair(cx+Math.floor(cw*.15)+i*Math.floor(cw*.3),cy-16,'#2a4a6a');
    drawChair(cx+Math.floor(cw*.15)+i*Math.floor(cw*.3),cy+ch+10,'#2a4a6a');
  }
  drawChair(cx-16,cy+Math.floor(ch*.5));
  drawChair(cx+cw+10,cy+Math.floor(ch*.5));

  // Research desks (top-center)
  drawDesk(sx+Math.floor(sw*.4),sy+20,Math.floor(sw*.13),Math.floor(sh*.18));
  drawMonitor(sx+Math.floor(sw*.42),sy+26);
  drawChair(sx+Math.floor(sw*.46),sy+Math.floor(sh*.2),'#1a4a6a');

  drawDesk(sx+Math.floor(sw*.56),sy+20,Math.floor(sw*.13),Math.floor(sh*.18));
  drawMonitor(sx+Math.floor(sw*.58),sy+26);
  drawChair(sx+Math.floor(sw*.62),sy+Math.floor(sh*.2),'#1a4a6a');

  // Dev desks (bottom-center/right)
  drawDesk(sx+Math.floor(sw*.4),sy+Math.floor(sh*.65),Math.floor(sw*.13),Math.floor(sh*.18));
  drawMonitor(sx+Math.floor(sw*.42),sy+Math.floor(sh*.67));
  drawChair(sx+Math.floor(sw*.46),sy+Math.floor(sh*.62),'#3a1a1a');

  drawDesk(sx+Math.floor(sw*.56),sy+Math.floor(sh*.65),Math.floor(sw*.13),Math.floor(sh*.18));
  drawMonitor(sx+Math.floor(sw*.58),sy+Math.floor(sh*.67));
  drawChair(sx+Math.floor(sw*.62),sy+Math.floor(sh*.62),'#3a1a1a');

  // Finance desk (bottom-left)
  drawDesk(sx+20,sy+Math.floor(sh*.6),Math.floor(sw*.15),Math.floor(sh*.2));
  drawMonitor(sx+28,sy+Math.floor(sh*.62));
  drawChair(sx+Math.floor(sw*.07),sy+Math.floor(sh*.57),'#1a4a3a');

  // Risk/analysis (right area)
  drawDesk(sx+Math.floor(sw*.75),sy+Math.floor(sh*.25),Math.floor(sw*.13),Math.floor(sh*.18));
  drawMonitor(sx+Math.floor(sw*.77),sy+Math.floor(sh*.27));
  drawChair(sx+Math.floor(sw*.81),sy+Math.floor(sh*.22),'#3a2a1a');

  // Bookshelf (right wall)
  drawBookshelf(W-58,44,22,Math.floor(sh*.4));
  drawBookshelf(W-58,sy+Math.floor(sh*.45),22,Math.floor(sh*.4));

  // TV (left wall)
  drawTV(36,sy+Math.floor(sh*.3),Math.floor(sw*.09),Math.floor(sh*.2));

  // Plants
  drawPlant(sx+Math.floor(sw*.22),sy+10);
  drawPlant(sx+Math.floor(sw*.22),sy+Math.floor(sh*.85));
  drawPlant(W-56,sy+Math.floor(sh*.85));

  // Sofa (bottom-left corner)
  drawSofa(sx+18,sy+Math.floor(sh*.78),Math.floor(sw*.15));

  // Water cooler
  drawWaterCooler(sx+Math.floor(sw*.35),sy+Math.floor(sh*.85));
}

// ---- AGENT SPRITE ----
function darken(hex,a=40){
  const r=Math.max(0,parseInt(hex.slice(1,3),16)-a);
  const g=Math.max(0,parseInt(hex.slice(3,5),16)-a);
  const b=Math.max(0,parseInt(hex.slice(5,7),16)-a);
  return `rgb(${r},${g},${b})`;
}

function drawAgent(agent, frame){
  const st = agentStates[agent.id];
  if(!st) return;
  const {x, y} = st.cur;
  const col = AGENT_COL[agent.type] || '#fff';
  const leg = Math.sin(frame * 0.18 + st.phase) * 4;
  const bob = Math.sin(frame * 0.09 + st.phase) * 1.5;
  const px = Math.round(x), py = Math.round(y + bob);

  // Shadow
  ctx.globalAlpha=.2;
  ctx.fillStyle='#000';ctx.beginPath();ctx.ellipse(px,py+22,12,5,0,0,Math.PI*2);ctx.fill();
  ctx.globalAlpha=1;

  // Legs
  fillRect(px-6,py+8,5,12+leg,darken(col,50));
  fillRect(px+1,py+8,5,12-leg,darken(col,50));
  // Body
  ctx.fillStyle=col;ctx.fillRect(px-9,py-4,18,14);
  // Arms
  fillRect(px-13,py-2,4,10-leg/2,darken(col,25));
  fillRect(px+9,py-2,4,10+leg/2,darken(col,25));
  // Head
  ctx.fillStyle='#f4c2a1';ctx.beginPath();ctx.arc(px,py-10,9,0,Math.PI*2);ctx.fill();
  // Hair
  ctx.fillStyle=darken(col,30);ctx.beginPath();ctx.arc(px,py-13,7.5,Math.PI,2*Math.PI);ctx.fill();
  // Eyes
  ctx.fillStyle='#222';ctx.fillRect(px-5,py-12,3,3);ctx.fillRect(px+2,py-12,3,3);

  // Name tag
  ctx.font='bold 9px "Press Start 2P",monospace';
  const tw=ctx.measureText(agent.name).width;
  ctx.fillStyle='rgba(0,0,0,.75)';ctx.fillRect(px-tw/2-5,py-34,tw+10,15);
  ctx.fillStyle=col;ctx.textAlign='center';ctx.fillText(agent.name,px,py-23);
  ctx.textAlign='left';
}

// ---- ANIMATION LOOP ----
function lerp(a,b,t){return a+(b-a)*t}

function updateAgents(agents){
  agents.forEach(a=>{
    if(!agentStates[a.id]){
      const rp = ROOM_POS[a.location]||{x:.5,y:.5};
      const tx=32+(W-64)*rp.x + (Math.random()-.5)*40;
      const ty=40+(H-80)*rp.y + (Math.random()-.5)*30;
      agentStates[a.id]={cur:{x:tx,y:ty},target:{x:tx,y:ty},phase:Math.random()*Math.PI*2};
    }
    const st=agentStates[a.id];
    const rp=ROOM_POS[a.location]||{x:.5,y:.5};
    st.target.x=32+(W-64)*rp.x+(Math.random()-.5)*40;
    st.target.y=40+(H-80)*rp.y+(Math.random()-.5)*30;
  });
}

let agentData=[];
let frameCount=0;

function loop(){
  requestAnimationFrame(loop);
  frameCount++;
  ctx.clearRect(0,0,W,H);
  ctx.fillStyle='#1a1a2e';ctx.fillRect(0,0,W,H);
  drawFloor();
  drawFurniture();
  drawWalls();

  agentData.forEach(a=>{
    const st=agentStates[a.id];
    if(!st) return;
    st.cur.x=lerp(st.cur.x,st.target.x,.018);
    st.cur.y=lerp(st.cur.y,st.target.y,.018);
  });
  // Draw agents sorted by y (depth)
  [...agentData].sort((a,b)=>{
    const ay=agentStates[a.id]?.cur.y||0;
    const by=agentStates[b.id]?.cur.y||0;
    return ay-by;
  }).forEach(a=>drawAgent(a,frameCount));
}

// ---- DATA FETCH ----
const AGENT_MSGS = {
  CEO:      ['전략 검토 중...','회의 소집 중...','보고서 작성 중...','목표 재설정 중...'],
  Research: ['시장 조사 중...','경쟁사 분석 중...','트렌드 스캔 중...','인사이트 도출 중...'],
  Analysis: ['데이터 모델링...','수익 시뮬레이션...','지표 계산 중...','패턴 분석 중...'],
  Finance:  ['재무 모델 갱신...','ROI 계산 중...','손익 분석 중...','예산 검토 중...'],
  Risk:     ['리스크 점검 중...','위협 모니터링...','리스크 매트릭스 갱신...'],
  Execution:['빌드 진행 중...','배포 준비 중...','코드 리뷰 중...','테스트 실행 중...'],
  Product:  ['UX 설계 중...','사용자 플로우 개선...','프로토타입 제작...'],
};

function addFeedMsg(agent){
  const msgs=AGENT_MSGS[agent.type]||['작업 중...'];
  const txt=msgs[Math.floor(Math.random()*msgs.length)];
  const feed=document.getElementById('feed');
  const div=document.createElement('div');
  div.className=`msg ${agent.type}`;
  div.innerHTML=`<div class="msg-agent">${agent.name} [${agent.type}]</div><div class="msg-text">${txt}</div>`;
  feed.insertBefore(div,feed.firstChild);
  while(feed.children.length>20) feed.removeChild(feed.lastChild);
}

let lastAgentCount=0;
async function fetchState(){
  try{
    const r=await fetch('/api/state');const d=await r.json();
    agentData=d.agents||[];
    updateAgents(agentData);
    // Feed messages
    if(agentData.length!==lastAgentCount || Math.random()<.3){
      const randomAgent=agentData[Math.floor(Math.random()*agentData.length)];
      if(randomAgent) addFeedMsg(randomAgent);
      lastAgentCount=agentData.length;
    }
    // Stats
    const c=d.company||{};
    document.getElementById('s-lv').textContent='LV.'+c.level;
    document.getElementById('s-day').textContent='DAY '+c.day;
    document.getElementById('s-hp').textContent='HP '+c.health;
    document.getElementById('s-ag').textContent=agentData.length+' AGENTS';
    const pct=Math.min(100,Math.round(parseInt(c.xp||0)/10));
    document.getElementById('xpfill').style.width=pct+'%';
    document.getElementById('xplabel').textContent='XP '+(c.xp||0)+'/1000';
    // Projects
    document.getElementById('pc').innerHTML=(d.projects||[]).map((p,i)=>`
      <div class="prow">
        <div class="pname">${p.id} ${p.name.substring(0,18)}</div>
        <div class="pbg"><div class="pbar" style="width:${p.progress}%;background:${i===0?'#00b4d8':'#9d4edd'};box-shadow:0 0 4px ${i===0?'#00b4d8':'#9d4edd'}"></div></div>
        <div class="ppct">${p.progress}% — ${p.status}</div>
      </div>`).join('');
  }catch(e){console.error(e)}
}

// Periodic feed messages even without data change
setInterval(()=>{
  if(agentData.length>0){
    const a=agentData[Math.floor(Math.random()*agentData.length)];
    if(a) addFeedMsg(a);
  }
},4000);

fetchState();
setInterval(fetchState,10000);
loop();
</script>
</body>
</html>"""


@app.get("/", response_class=HTMLResponse)
async def dashboard():
    return HTML


@app.get("/api/state")
async def api_state():
    agents = await db.get_all_agents()
    projects = await db.get_all_projects()
    level = await db.get_state("level")
    xp = await db.get_state("xp")
    health = await db.get_state("health_score")
    day = await db.get_state("day")
    events = []
    async with aiosqlite.connect("dante_corp.db") as conn:
        conn.row_factory = aiosqlite.Row
        async with conn.execute(
            "SELECT time, agent, event FROM event_log ORDER BY id DESC LIMIT 50"
        ) as cur:
            rows = await cur.fetchall()
            events = [dict(r) for r in reversed(rows)]
    return {
        "agents": agents,
        "projects": projects,
        "events": events,
        "company": {"level": level, "xp": xp, "health": health, "day": day},
    }
