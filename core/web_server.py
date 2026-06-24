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
<title>DANTE CORPORATION OS v1.0</title>
<link href="https://fonts.googleapis.com/css2?family=Press+Start+2P&display=swap" rel="stylesheet">
<style>
*{box-sizing:border-box;margin:0;padding:0}
body{background:#050510;color:#00ff41;font-family:'Press Start 2P',cursive;font-size:8px;overflow-x:hidden;padding-bottom:24px}
body::after{content:'';position:fixed;top:0;left:0;right:0;bottom:0;background:repeating-linear-gradient(0deg,transparent,transparent 2px,rgba(0,0,0,.13) 2px,rgba(0,0,0,.13) 4px);pointer-events:none;z-index:9999}

/* HEADER */
#hdr{padding:10px 14px;border-bottom:2px solid #00ff41;display:flex;align-items:center;gap:10px;background:#07070f;flex-wrap:wrap;box-shadow:0 0 30px rgba(0,255,65,.08)}
#logo{font-size:13px;color:#ffd700;text-shadow:0 0 12px #ffd700,0 0 24px #ffd700;letter-spacing:2px;white-space:nowrap}
.chip{padding:3px 7px;border:1px solid #00ff41;font-size:6px;white-space:nowrap}
.chip.g{border-color:#ffd700;color:#ffd700}
.chip.c{border-color:#00b4d8;color:#00b4d8}
.chip.r{border-color:#ff6b35;color:#ff6b35}
#xpw{flex:1;min-width:120px;max-width:180px}
#xpl{font-size:5px;color:#2a4a2a;margin-bottom:3px}
#xpbg{height:9px;background:#111122;border:1px solid #00ff41;position:relative}
#xpf{height:100%;background:#ffd700;box-shadow:0 0 8px #ffd700;transition:width .8s ease}
.blink{animation:bl 1s step-end infinite}
@keyframes bl{50%{opacity:0}}
.live-dot{display:inline-block;width:7px;height:7px;background:#ff0055;border-radius:50%;margin-right:4px;animation:pulse 1s ease-in-out infinite;box-shadow:0 0 6px #ff0055;vertical-align:middle}
@keyframes pulse{0%,100%{transform:scale(1);opacity:1}50%{transform:scale(1.5);opacity:.5}}

/* LAYOUT */
#wrap{display:grid;grid-template-columns:1fr 300px;gap:10px;padding:10px;min-height:calc(100vh - 54px)}

/* OFFICE */
#office{display:flex;flex-direction:column;gap:10px}
.sec-title{font-size:8px;color:#00b4d8;letter-spacing:2px;text-shadow:0 0 8px #00b4d8;margin-bottom:6px}
#ogrid{display:grid;grid-template-columns:repeat(4,1fr);grid-template-rows:repeat(2,140px);gap:8px;flex:1}
.room{padding:8px;border:2px solid #111128;background:#080816;display:flex;flex-direction:column;gap:5px;position:relative;transition:border-color .4s,box-shadow .4s;overflow:hidden}
.room.on{border-color:#00ff41;box-shadow:inset 0 0 24px rgba(0,255,65,.04),0 0 12px rgba(0,255,65,.08)}
.rname{font-size:5px;color:#223322;letter-spacing:1px;border-bottom:1px solid #111128;padding-bottom:3px;transition:color .4s}
.room.on .rname{color:#00ff41;border-bottom-color:#1a3a1a}
.rico{font-size:18px;opacity:.18;position:absolute;bottom:6px;right:6px}
.sprites{display:flex;flex-wrap:wrap;gap:3px;flex:1}
.sp{width:30px;height:30px;display:flex;flex-direction:column;align-items:center;justify-content:center;gap:1px;border:1px solid;cursor:pointer;position:relative;animation:bob 2s ease-in-out infinite}
.sp:hover::after{content:attr(data-tip);position:absolute;bottom:34px;left:0;background:#0a0a1a;border:1px solid #00ff41;padding:4px 6px;font-size:5px;color:#00ff41;white-space:nowrap;z-index:200;pointer-events:none}
@keyframes bob{0%,100%{transform:translateY(0)}50%{transform:translateY(-3px)}}
.sp-ico{font-size:10px}
.sp-nm{font-size:4px}
.CEO{background:rgba(255,215,0,.12);border-color:#ffd700;color:#ffd700}
.Research{background:rgba(0,180,216,.12);border-color:#00b4d8;color:#00b4d8}
.Analysis{background:rgba(157,78,221,.12);border-color:#9d4edd;color:#9d4edd}
.Finance{background:rgba(6,214,160,.12);border-color:#06d6a0;color:#06d6a0}
.Risk{background:rgba(255,107,53,.12);border-color:#ff6b35;color:#ff6b35}
.Execution{background:rgba(239,35,60,.12);border-color:#ef233c;color:#ef233c}
.Product{background:rgba(255,133,161,.12);border-color:#ff85a1;color:#ff85a1}

/* PROJECTS */
#pbox{padding:10px;border:2px solid #111128;background:#080816}
.prj{margin-bottom:12px}
.prj-hdr{display:flex;justify-content:space-between;margin-bottom:3px}
.prj-nm{font-size:7px;color:#ffd700}
.prj-st{font-size:5px;padding:2px 5px;border:1px solid}
.PLANNING{border-color:#00b4d8;color:#00b4d8}
.RESEARCH{border-color:#9d4edd;color:#9d4edd}
.BUILDING{border-color:#ffd700;color:#ffd700}
.ACTIVE{border-color:#00ff41;color:#00ff41}
.prj-sub{font-size:5px;color:#2a2a4a;margin-bottom:4px}
.pbg{height:8px;background:#111122;border:1px solid #1a1a3a}
.pbar{height:100%;transition:width 1.2s ease}
.p0{background:#00b4d8;box-shadow:0 0 6px #00b4d8}
.p1{background:#9d4edd;box-shadow:0 0 6px #9d4edd}
.ppct{font-size:5px;color:#2a2a4a;text-align:right;margin-top:2px}

/* RIGHT */
#rp{display:flex;flex-direction:column;gap:10px;overflow-y:auto}
#abx{padding:10px;border:2px solid #111128;background:#080816}
.arow{display:flex;align-items:flex-start;gap:7px;padding:5px 0;border-bottom:1px solid #0c0c1e}
.adot{width:7px;height:7px;border:1px solid;flex-shrink:0;margin-top:2px}
.anm{font-size:6px}
.atsk{font-size:5px;color:#2a2a4a;margin-top:2px;line-height:1.6}
#elog{padding:10px;border:2px solid #111128;background:#050510;flex:1}
#elist{height:220px;overflow-y:auto;display:flex;flex-direction:column-reverse}
#elist::-webkit-scrollbar{width:3px}
#elist::-webkit-scrollbar-thumb{background:#00ff41}
.le{padding:3px 0;border-bottom:1px solid #0a0a16;animation:fin .3s ease}
@keyframes fin{from{opacity:0;transform:translateX(-8px)}to{opacity:1}}
.lt{color:#1a3a1a}
.la{color:#00b4d8}
.lx{color:#2a3a2a}

/* TICKER */
#ticker{position:fixed;bottom:0;left:0;right:0;background:#07070f;border-top:1px solid #00ff41;padding:4px 12px;font-size:5px;color:#00ff41;overflow:hidden;white-space:nowrap;z-index:100}
#tkt{display:inline-block;animation:scroll 35s linear infinite}
@keyframes scroll{from{transform:translateX(100vw)}to{transform:translateX(-100%)}}
</style>
</head>
<body>

<div id="hdr">
  <span id="logo">⬛ DANTE CORP</span>
  <span style="font-size:7px;color:#ff0055"><span class="live-dot"></span>LIVE</span>
  <span class="chip g" id="s-lv">LV.1</span>
  <span class="chip c" id="s-day">DAY 1</span>
  <span class="chip" id="s-ag">7 AGENTS</span>
  <span class="chip r" id="s-hp">HP 81</span>
  <div id="xpw">
    <div id="xpl">XP 580/1000</div>
    <div id="xpbg"><div id="xpf" style="width:58%"></div></div>
  </div>
  <span class="blink" style="color:#00ff41">█</span>
</div>

<div id="wrap">
  <div id="office">
    <div class="sec-title">◈ DANTE HQ — METAVERSE OFFICE</div>
    <div id="ogrid">
      <div class="room" id="r-Strategic_Command_Room"><div class="rname">STRATEGIC CMD</div><div class="sprites" id="s-Strategic_Command_Room"></div><span class="rico">🎯</span></div>
      <div class="room" id="r-Brainstorming_Room"><div class="rname">BRAINSTORM</div><div class="sprites" id="s-Brainstorming_Room"></div><span class="rico">💡</span></div>
      <div class="room" id="r-Research_Department"><div class="rname">RESEARCH DEPT</div><div class="sprites" id="s-Research_Department"></div><span class="rico">🔭</span></div>
      <div class="room" id="r-Analysis_Lab"><div class="rname">ANALYSIS LAB</div><div class="sprites" id="s-Analysis_Lab"></div><span class="rico">📊</span></div>
      <div class="room" id="r-Finance_Desk"><div class="rname">FINANCE DESK</div><div class="sprites" id="s-Finance_Desk"></div><span class="rico">💰</span></div>
      <div class="room" id="r-Meeting_Room"><div class="rname">MEETING ROOM</div><div class="sprites" id="s-Meeting_Room"></div><span class="rico">📋</span></div>
      <div class="room" id="r-Development_Room"><div class="rname">DEV ROOM</div><div class="sprites" id="s-Development_Room"></div><span class="rico">⚙️</span></div>
      <div class="room" id="r-Risk_Assessment_Room"><div class="rname">RISK ROOM</div><div class="sprites" id="s-Risk_Assessment_Room"></div><span class="rico">🛡️</span></div>
    </div>

    <div id="pbox">
      <div class="sec-title">◈ ACTIVE PROJECTS</div>
      <div id="pc"></div>
    </div>
  </div>

  <div id="rp">
    <div id="abx">
      <div class="sec-title">◈ AGENT ROSTER</div>
      <div id="al"></div>
    </div>
    <div id="elog">
      <div class="sec-title">◈ EVENT LOG <span class="blink">_</span></div>
      <div id="elist"></div>
    </div>
  </div>
</div>

<div id="ticker"><span id="tkt">⬛ DANTE CORPORATION AUTONOMOUS AI BUSINESS OS v1.0 &nbsp;&nbsp;&nbsp; ◈ ALL SYSTEMS OPERATIONAL &nbsp;&nbsp;&nbsp; ◈ 7 AGENTS ACTIVE &nbsp;&nbsp;&nbsp; ◈ 2 PROJECTS IN PROGRESS &nbsp;&nbsp;&nbsp; ◈ GROQ LLM ENGINE ONLINE &nbsp;&nbsp;&nbsp;</span></div>

<script>
const ICONS={CEO:'★',Research:'◉',Analysis:'▲',Finance:'◆',Risk:'⬡',Execution:'⚡',Product:'◎'};

function roomKey(loc){return loc.replace(/ /g,'_')}

function renderAgents(agents){
  document.querySelectorAll('.room').forEach(r=>{r.classList.remove('on');r.querySelector('.sprites').innerHTML=''});
  agents.forEach(a=>{
    const key=roomKey(a.location);
    const sc=document.getElementById('s-'+key);
    const rc=document.getElementById('r-'+key);
    if(!sc||!rc)return;
    rc.classList.add('on');
    const delay=(Math.random()*2).toFixed(1);
    sc.insertAdjacentHTML('beforeend',
      `<div class="sp ${a.type}" style="animation-delay:${delay}s" data-tip="${a.name} | ${a.current_task.substring(0,40)}">
        <span class="sp-ico">${ICONS[a.type]||'?'}</span>
        <span class="sp-nm">${a.name.substring(0,4)}</span>
      </div>`);
  });
  document.getElementById('s-ag').textContent=agents.length+' AGENTS';
  const al=document.getElementById('al');
  al.innerHTML=agents.map(a=>`
    <div class="arow">
      <div class="adot ${a.type}"></div>
      <div>
        <div class="anm ${a.type}">${a.name} <span style="color:#1a1a3a">[${a.type}]</span></div>
        <div class="atsk">${a.current_task.substring(0,42)}...</div>
      </div>
    </div>`).join('');
}

function renderProjects(ps){
  document.getElementById('pc').innerHTML=ps.map((p,i)=>`
    <div class="prj">
      <div class="prj-hdr"><span class="prj-nm">${p.id}</span><span class="prj-st ${p.status}">${p.status}</span></div>
      <div class="prj-sub">${p.name.substring(0,32)}</div>
      <div class="pbg"><div class="pbar p${i}" style="width:${p.progress}%"></div></div>
      <div class="ppct">${p.progress}% ◈ ${p.revenue_target}</div>
    </div>`).join('');
}

function renderCompany(c){
  document.getElementById('s-lv').textContent='LV.'+c.level;
  document.getElementById('s-day').textContent='DAY '+c.day;
  document.getElementById('s-hp').textContent='HP '+c.health;
  const pct=Math.min(100,Math.round(parseInt(c.xp)/10));
  document.getElementById('xpf').style.width=pct+'%';
  document.getElementById('xpl').textContent='XP '+c.xp+'/1000';
}

let lastLen=0;
function renderLog(evs){
  if(evs.length===lastLen)return;
  lastLen=evs.length;
  document.getElementById('elist').innerHTML=
    evs.slice(-40).reverse().map(e=>`
      <div class="le" style="font-size:6px">
        <span class="lt">[${e.time}]</span>
        <span class="la"> ${e.agent}</span>
        <span class="lx"> ${e.event.substring(0,44)}</span>
      </div>`).join('');
}

async function refresh(){
  try{
    const r=await fetch('/api/state');
    const d=await r.json();
    renderAgents(d.agents||[]);
    renderProjects(d.projects||[]);
    renderCompany(d.company||{});
    renderLog(d.events||[]);
  }catch(e){console.error(e)}
}

refresh();
setInterval(refresh,8000);
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
