import asyncio
import os
import uvicorn
from dotenv import load_dotenv
from core.database import init_db
from core.scheduler import create_scheduler
from core.telegram_bot import get_app, send_to_chairman
from core.web_server import app as web_app

load_dotenv()

TELEGRAM_TOKEN = os.environ["TELEGRAM_BOT_TOKEN"]
PORT = int(os.environ.get("PORT", 8080))


async def main():
    print("🏢 DANTE CORPORATION — 시스템 부팅 중...")

    await init_db()
    print("✅ 데이터베이스 초기화 완료")

    tg_app = get_app(TELEGRAM_TOKEN)
    await tg_app.initialize()
    await tg_app.start()
    print("✅ 텔레그램 봇 온라인")

    async def send_report(text: str):
        await send_to_chairman(tg_app, text)

    scheduler = create_scheduler(send_report)
    scheduler.start()
    print("✅ 스케줄러 가동 — 매일 09:00 KST 에이전트 사이클 실행")

    # 웹 대시보드
    config = uvicorn.Config(web_app, host="0.0.0.0", port=PORT, log_level="warning")
    server = uvicorn.Server(config)
    print(f"✅ 픽셀 대시보드 → http://0.0.0.0:{PORT}")

    await send_to_chairman(
        tg_app,
        "🏢 *DANTE CORPORATION*\n\n"
        "✅ 시스템 온라인\n"
        "🤖 7명 에이전트 가동 중\n"
        "📁 프로젝트 2개 진행 중\n"
        f"🖥 대시보드 접속 가능\n\n"
        "매일 09:00 KST 일일 보고서 전송.\n"
        "/decisions 로 미결 사항 확인."
    )

    print("🚀 DANTE CORPORATION 완전 가동!")

    await tg_app.updater.start_polling(drop_pending_updates=True)

    try:
        await server.serve()
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
