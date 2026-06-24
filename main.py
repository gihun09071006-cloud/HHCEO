import asyncio
import os
from dotenv import load_dotenv
from core.database import init_db
from core.scheduler import create_scheduler
from core.telegram_bot import get_app, send_to_chairman

load_dotenv()

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]


async def main():
    print("🏢 DANTE CORPORATION — 시스템 부팅 중...")

    # DB 초기화
    await init_db()
    print("✅ 데이터베이스 초기화 완료")

    # 텔레그램 봇
    tg_app = get_app(TELEGRAM_TOKEN)
    await tg_app.initialize()
    await tg_app.start()
    print("✅ 텔레그램 봇 온라인")

    # 보고서 전송 함수
    async def send_report(text: str):
        await send_to_chairman(tg_app, text)

    # 스케줄러
    scheduler = create_scheduler(send_report)
    scheduler.start()
    print("✅ 스케줄러 가동 — 매일 09:00 KST 에이전트 사이클 실행")

    # 시작 알림
    await send_to_chairman(
        tg_app,
        "🏢 *DANTE CORPORATION*\n\n"
        "✅ 시스템 온라인\n"
        "🤖 7명 에이전트 가동 중\n"
        "📁 프로젝트 2개 진행 중\n\n"
        "매일 09:00 KST 일일 보고서가 전송됩니다.\n"
        "/decisions 로 미결 사항을 확인하세요."
    )

    print("🚀 DANTE CORPORATION 완전 가동!")

    # 텔레그램 폴링 시작 (메인 루프)
    await tg_app.updater.start_polling(drop_pending_updates=True)

    # 종료 대기
    try:
        await asyncio.Event().wait()
    except (KeyboardInterrupt, SystemExit):
        pass
    finally:
        scheduler.shutdown()
        await tg_app.updater.stop()
        await tg_app.stop()
        await tg_app.shutdown()
        print("DANTE CORPORATION 종료.")


if __name__ == "__main__":
    asyncio.run(main())
