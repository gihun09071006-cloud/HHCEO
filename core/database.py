import aiosqlite
import json
import os
from datetime import datetime

DB_PATH = os.environ.get("DB_PATH", "/data/dante_corp.db")


async def init_db():
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript("""
            CREATE TABLE IF NOT EXISTS agents (
                id TEXT PRIMARY KEY,
                name TEXT,
                type TEXT,
                location TEXT,
                current_task TEXT,
                xp INTEGER DEFAULT 0,
                updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS projects (
                id TEXT PRIMARY KEY,
                name TEXT,
                status TEXT,
                priority TEXT,
                owner TEXT,
                target_launch TEXT,
                revenue_target TEXT,
                progress INTEGER DEFAULT 0,
                created_at TEXT,
                updated_at TEXT
            );

            CREATE TABLE IF NOT EXISTS decisions (
                id TEXT PRIMARY KEY,
                title TEXT,
                description TEXT,
                recommended_by TEXT,
                status TEXT DEFAULT 'PENDING',
                chairman_response TEXT,
                created_at TEXT,
                resolved_at TEXT
            );

            CREATE TABLE IF NOT EXISTS opportunities (
                id TEXT PRIMARY KEY,
                title TEXT,
                score REAL,
                status TEXT,
                description TEXT,
                created_at TEXT
            );

            CREATE TABLE IF NOT EXISTS event_log (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT,
                agent TEXT,
                event TEXT,
                created_at TEXT
            );

            CREATE TABLE IF NOT EXISTS reports (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                day INTEGER,
                content TEXT,
                sent_at TEXT
            );

            CREATE TABLE IF NOT EXISTS company_state (
                key TEXT PRIMARY KEY,
                value TEXT
            );
        """)
        await db.commit()

        # 초기 회사 상태
        defaults = {
            "level": "1",
            "level_name": "Startup",
            "xp": "580",
            "health_score": "81",
            "day": "1",
            "treasury": "0",
        }
        for k, v in defaults.items():
            await db.execute(
                "INSERT OR IGNORE INTO company_state (key, value) VALUES (?, ?)", (k, v)
            )

        # 초기 에이전트
        agents = [
            ("Agent-01", "ARIA", "CEO", "Strategic Command Room", "전체 작전 총괄", 150),
            ("Agent-02", "NEXUS", "Research", "Research Department", "시장 조사 진행 중", 120),
            ("Agent-03", "VECTOR", "Analysis", "Analysis Lab", "수익 모델링 진행 중", 110),
            ("Agent-04", "LEDGER", "Finance", "Finance Desk", "재무 로드맵 작성 중", 100),
            ("Agent-05", "SENTINEL", "Risk", "Risk Assessment Room", "ToS 모니터링 중", 100),
            ("Agent-06", "FORGE", "Execution", "Development Room", "MVP 아키텍처 설계 중", 0),
            ("Agent-07", "PRISM", "Product", "Development Room", "UX 설계 중", 0),
        ]
        for a in agents:
            await db.execute(
                "INSERT OR IGNORE INTO agents (id,name,type,location,current_task,xp,updated_at) VALUES (?,?,?,?,?,?,?)",
                (*a, datetime.now().isoformat())
            )

        # 초기 프로젝트
        projects = [
            ("PRJ-001", "LinkedIn AI Ghost Engine", "PLANNING", "FAST_CASH",
             "FORGE", "2026-07-14", "$2,000 MRR (3개월)", 20),
            ("PRJ-002", "DANTE Marketplace", "RESEARCH", "PRIMARY_VENTURE",
             "ARIA", "2026-09-30", "$120,000 ARR (1년)", 10),
        ]
        for p in projects:
            await db.execute(
                "INSERT OR IGNORE INTO projects (id,name,status,priority,owner,target_launch,revenue_target,progress,created_at,updated_at) VALUES (?,?,?,?,?,?,?,?,?,?)",
                (*p, datetime.now().isoformat(), datetime.now().isoformat())
            )

        await db.commit()


async def get_state(key: str) -> str:
    async with aiosqlite.connect(DB_PATH) as db:
        async with db.execute("SELECT value FROM company_state WHERE key=?", (key,)) as cur:
            row = await cur.fetchone()
            return row[0] if row else ""


async def set_state(key: str, value: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR REPLACE INTO company_state (key, value) VALUES (?,?)", (key, value)
        )
        await db.commit()


async def get_all_agents() -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM agents") as cur:
            return [dict(r) for r in await cur.fetchall()]


async def get_all_projects() -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute("SELECT * FROM projects") as cur:
            return [dict(r) for r in await cur.fetchall()]


async def get_pending_decisions() -> list:
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(
            "SELECT * FROM decisions WHERE status='PENDING' ORDER BY created_at DESC"
        ) as cur:
            return [dict(r) for r in await cur.fetchall()]


async def resolve_decision(decision_id: str, response: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE decisions SET status=?, chairman_response=?, resolved_at=? WHERE id=?",
            (response, response, datetime.now().isoformat(), decision_id)
        )
        await db.commit()


async def add_decision(decision_id: str, title: str, description: str, recommended_by: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT OR IGNORE INTO decisions (id,title,description,recommended_by,status,created_at) VALUES (?,?,?,?,?,?)",
            (decision_id, title, description, recommended_by, "PENDING", datetime.now().isoformat())
        )
        await db.commit()


async def log_event(agent: str, event: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO event_log (time, agent, event, created_at) VALUES (?,?,?,?)",
            (datetime.now().strftime("%H:%M"), agent, event, datetime.now().isoformat())
        )
        await db.commit()


async def save_report(day: int, content: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "INSERT INTO reports (day, content, sent_at) VALUES (?,?,?)",
            (day, content, datetime.now().isoformat())
        )
        await db.commit()


async def update_agent(agent_id: str, location: str, task: str):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE agents SET location=?, current_task=?, updated_at=? WHERE id=?",
            (location, task, datetime.now().isoformat(), agent_id)
        )
        await db.commit()


async def update_project_status(project_id: str, status: str, progress: int):
    async with aiosqlite.connect(DB_PATH) as db:
        await db.execute(
            "UPDATE projects SET status=?, progress=?, updated_at=? WHERE id=?",
            (status, progress, datetime.now().isoformat(), project_id)
        )
        await db.commit()
