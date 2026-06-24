from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.cron import CronTrigger
from . import database as db
from ..agents import ARIA, NEXUS, VECTOR, LEDGER, SENTINEL, FORGE, PRISM
from datetime import datetime
import asyncio


async def run_daily_cycle(send_report_fn):
    """매일 09:00 KST 실행되는 전사 에이전트 루틴"""
    projects = await db.get_all_projects()
    agents = await db.get_all_agents()
    pending = await db.get_pending_decisions()

    day = int(await db.get_state("day")) + 1
    await db.set_state("day", str(day))

    await db.log_event("SYSTEM", f"Day {day} 일일 사이클 시작")

    # 에이전트 동시 실행
    aria = ARIA()
    nexus = NEXUS()
    vector = VECTOR()
    ledger = LEDGER()
    sentinel = SENTINEL()
    forge = FORGE()
    prism = PRISM()

    results = await asyncio.gather(
        aria.run_daily(projects, agents, pending),
        nexus.run_daily(projects),
        vector.run_daily(projects),
        ledger.run_daily(projects),
        sentinel.run_daily(projects),
        forge.run_daily(projects),
        prism.run_daily(projects),
        return_exceptions=True
    )

    labels = ["ARIA/CEO", "NEXUS/Research", "VECTOR/Analysis",
              "LEDGER/Finance", "SENTINEL/Risk", "FORGE/Execution", "PRISM/Product"]

    agent_outputs = {}
    for label, result in zip(labels, results):
        if isinstance(result, Exception):
            agent_outputs[label] = f"⚠️ 오류: {str(result)}"
        else:
            agent_outputs[label] = result

    # ARIA가 최종 보고서 합성
    synthesis_context = f"""
Day {day} 전 에이전트 보고 요약:

{chr(10).join(f'[{k}]: {v[:300]}...' for k, v in agent_outputs.items())}

위 보고를 바탕으로 회장님께 보낼 일일 보고서를 작성하세요.
형식:
- 오늘의 핵심 진척 사항 (3줄)
- 각 프로젝트 상태
- 주요 리스크
- 회장님 결정 필요 사항 (있을 경우)
- 내일 계획
"""
    final_report = aria.think(synthesis_context)

    report_text = f"""
━━━━━━━━━━━━━━━━━━━━━━━━
🏢 DANTE CORPORATION
📅 Day {day} 일일 보고서
⏰ {datetime.now().strftime('%Y-%m-%d %H:%M')} KST
━━━━━━━━━━━━━━━━━━━━━━━━

{final_report}

━━━━━━━━━━━━━━━━━━━━━━━━
📊 에이전트 상세 보고
━━━━━━━━━━━━━━━━━━━━━━━━

""" + "\n\n".join(f"[{k}]\n{v}" for k, v in agent_outputs.items())

    await db.save_report(day, report_text)
    await db.log_event("ARIA", f"Day {day} 보고서 생성 완료 → 회장님 전송")

    await send_report_fn(report_text)


def create_scheduler(send_report_fn) -> AsyncIOScheduler:
    scheduler = AsyncIOScheduler(timezone="Asia/Seoul")

    # 매일 오전 9시 일일 보고
    scheduler.add_job(
        run_daily_cycle,
        CronTrigger(hour=9, minute=0, timezone="Asia/Seoul"),
        args=[send_report_fn],
        id="daily_cycle",
        name="Daily Agent Cycle"
    )

    return scheduler
