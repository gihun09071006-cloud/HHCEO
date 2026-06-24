import os
from telegram import Update, InlineKeyboardButton, InlineKeyboardMarkup
from telegram.ext import (
    Application, CommandHandler, CallbackQueryHandler,
    ContextTypes, MessageHandler, filters
)
from core import database as db

CHAIRMAN_CHAT_ID = int(os.environ.get("CHAIRMAN_CHAT_ID", "0"))


def get_app(token: str) -> Application:
    app = Application.builder().token(token).build()
    app.add_handler(CommandHandler("start", cmd_start))
    app.add_handler(CommandHandler("status", cmd_status))
    app.add_handler(CommandHandler("agents", cmd_agents))
    app.add_handler(CommandHandler("projects", cmd_projects))
    app.add_handler(CommandHandler("decisions", cmd_decisions))
    app.add_handler(CommandHandler("report", cmd_report))
    app.add_handler(CallbackQueryHandler(handle_decision_callback))
    app.add_handler(MessageHandler(filters.TEXT & ~filters.COMMAND, handle_message))
    return app


async def cmd_start(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text(
        "🏢 *DANTE CORPORATION* 온라인\n\n"
        "사용 가능한 명령어:\n"
        "/status — 회사 현황\n"
        "/agents — 에이전트 현황\n"
        "/projects — 프로젝트 현황\n"
        "/decisions — 미결 결정사항\n"
        "/report — 최신 보고서",
        parse_mode="Markdown"
    )


async def cmd_status(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    level = await db.get_state("level")
    xp = await db.get_state("xp")
    health = await db.get_state("health_score")
    day = await db.get_state("day")
    agents = await db.get_all_agents()
    projects = await db.get_all_projects()

    text = (
        f"🏢 *DANTE CORPORATION*\n"
        f"━━━━━━━━━━━━━━━━━━━━\n"
        f"📅 Day {day}\n"
        f"⭐ Level {level} — Startup\n"
        f"💪 XP: {xp}/1000\n"
        f"❤️ Health: {health}/100\n"
        f"🤖 에이전트: {len(agents)}명\n"
        f"📁 프로젝트: {len(projects)}개 진행 중"
    )
    await update.message.reply_text(text, parse_mode="Markdown")


async def cmd_agents(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    agents = await db.get_all_agents()
    lines = ["🤖 *에이전트 현황*\n━━━━━━━━━━━━━━━━━━━━"]
    for a in agents:
        lines.append(f"*{a['name']}* [{a['type']}]\n📍 {a['location']}\n🔧 {a['current_task']}\n")
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_projects(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    projects = await db.get_all_projects()
    lines = ["📁 *프로젝트 현황*\n━━━━━━━━━━━━━━━━━━━━"]
    for p in projects:
        bar = "█" * (p['progress'] // 10) + "░" * (10 - p['progress'] // 10)
        lines.append(
            f"*{p['id']}* {p['name']}\n"
            f"상태: `{p['status']}`  진척: {p['progress']}%\n"
            f"[{bar}]\n"
            f"🎯 목표: {p['revenue_target']}\n"
            f"🗓 런치: {p['target_launch']}\n"
        )
    await update.message.reply_text("\n".join(lines), parse_mode="Markdown")


async def cmd_decisions(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    decisions = await db.get_pending_decisions()
    if not decisions:
        await update.message.reply_text("✅ 미결 결정사항 없음")
        return

    for d in decisions:
        keyboard = [
            [
                InlineKeyboardButton("✅ APPROVE", callback_data=f"APPROVE|{d['id']}"),
                InlineKeyboardButton("⏸ HOLD", callback_data=f"HOLD|{d['id']}"),
                InlineKeyboardButton("❌ REJECT", callback_data=f"REJECT|{d['id']}"),
            ]
        ]
        markup = InlineKeyboardMarkup(keyboard)
        await update.message.reply_text(
            f"⚠️ *결정 필요: {d['id']}*\n\n"
            f"*{d['title']}*\n\n"
            f"{d['description']}\n\n"
            f"추천: {d['recommended_by']}",
            reply_markup=markup,
            parse_mode="Markdown"
        )


async def cmd_report(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    async with __import__('aiosqlite').connect("dante_corp.db") as conn:
        conn.row_factory = __import__('aiosqlite').Row
        async with conn.execute(
            "SELECT * FROM reports ORDER BY id DESC LIMIT 1"
        ) as cur:
            row = await cur.fetchone()
    if not row:
        await update.message.reply_text("아직 보고서가 없습니다.")
        return
    content = dict(row)["content"]
    # 텔레그램 메시지 길이 제한으로 분할
    for i in range(0, len(content), 4000):
        await update.message.reply_text(content[i:i+4000])


async def handle_decision_callback(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    query = update.callback_query
    await query.answer()
    action, decision_id = query.data.split("|")
    await db.resolve_decision(decision_id, action)
    await db.log_event("CHAIRMAN", f"결정 {decision_id}: {action}")

    emoji = {"APPROVE": "✅", "HOLD": "⏸", "REJECT": "❌"}[action]
    await query.edit_message_text(
        f"{emoji} *{action}* — {decision_id}\n회장님 결정이 반영되었습니다.",
        parse_mode="Markdown"
    )


async def handle_message(update: Update, ctx: ContextTypes.DEFAULT_TYPE):
    text = update.message.text.strip().upper()
    if text in ("APPROVE", "HOLD", "REJECT", "TERMINATE"):
        await update.message.reply_text(
            f"명령어 '{text}' 수신.\n/decisions 에서 특정 결정사항에 적용하세요."
        )
    else:
        await update.message.reply_text(
            "사용 가능한 명령어: /status /agents /projects /decisions /report"
        )


async def send_to_chairman(app: Application, text: str):
    if CHAIRMAN_CHAT_ID == 0:
        return
    for i in range(0, len(text), 4000):
        await app.bot.send_message(
            chat_id=CHAIRMAN_CHAT_ID,
            text=text[i:i+4000]
        )
