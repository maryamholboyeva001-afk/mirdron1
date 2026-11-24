"""SQLite bilan ishlash (aiosqlite)."""
from datetime import datetime
from zoneinfo import ZoneInfo

import aiosqlite

from config import DB_PATH, TIMEZONE

SCHEMA = """
CREATE TABLE IF NOT EXISTS scooters (
    scooter_id TEXT PRIMARY KEY,
    tg_id INTEGER UNIQUE,
    full_name TEXT,
    username TEXT,
    model TEXT NOT NULL,
    has_device INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);
CREATE TABLE IF NOT EXISTS alerts (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    admin_id INTEGER NOT NULL,
    target TEXT NOT NULL,
    lat REAL NOT NULL,
    lon REAL NOT NULL,
    danger_time TEXT NOT NULL,
    ok INTEGER NOT NULL DEFAULT 0,
    fail INTEGER NOT NULL DEFAULT 0,
    created_at TEXT NOT NULL
);
"""


def now_str() -> str:
    return datetime.now(ZoneInfo(TIMEZONE)).strftime("%d.%m.%Y %H:%M")


async def init_db() -> None:
    async with aiosqlite.connect(DB_PATH) as db:
        await db.executescript(SCHEMA)
        await db.commit()


async def _one(query: str, args: tuple = ()):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(query, args) as cur:
            return await cur.fetchone()


async def _all(query: str, args: tuple = ()):
    async with aiosqlite.connect(DB_PATH) as db:
        db.row_factory = aiosqlite.Row
        async with db.execute(query, args) as cur:
            return await cur.fetchall()


async def _exec(query: str, args: tuple = ()) -> int:
    async with aiosqlite.connect(DB_PATH) as db:
        cur = await db.execute(query, args)
        await db.commit()
        return cur.lastrowid


# ---------- foydalanuvchilar ----------
async def get_by_tg(tg_id: int):
    return await _one("SELECT * FROM scooters WHERE tg_id = ?", (tg_id,))


async def get_by_sid(scooter_id: str):
    return await _one("SELECT * FROM scooters WHERE scooter_id = ? COLLATE NOCASE", (scooter_id,))


async def create_scooter(scooter_id, tg_id, full_name, username, model, has_device):
    await _exec(
        "INSERT INTO scooters (scooter_id, tg_id, full_name, username, model, has_device, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?)",
        (scooter_id, tg_id, full_name, username, model, int(has_device), now_str()),
    )


async def link_scooter(scooter_id, tg_id, full_name, username):
    await _exec(
        "UPDATE scooters SET tg_id = ?, full_name = ?, username = ? WHERE scooter_id = ?",
        (tg_id, full_name, username, scooter_id),
    )


async def unlink_tg(tg_id: int):
    await _exec("UPDATE scooters SET tg_id = NULL WHERE tg_id = ?", (tg_id,))


async def set_model(tg_id: int, model: str):
    await _exec("UPDATE scooters SET model = ? WHERE tg_id = ?", (model, tg_id))


async def set_device(tg_id: int, has_device: bool):
    await _exec("UPDATE scooters SET has_device = ? WHERE tg_id = ?", (int(has_device), tg_id))


async def all_linked():
    return await _all("SELECT * FROM scooters WHERE tg_id IS NOT NULL ORDER BY created_at DESC")


async def linked_page(page: int, size: int):
    return await _all(
        "SELECT * FROM scooters WHERE tg_id IS NOT NULL ORDER BY created_at DESC LIMIT ? OFFSET ?",
        (size, page * size),
    )


async def count_linked() -> int:
    row = await _one("SELECT COUNT(*) AS c FROM scooters WHERE tg_id IS NOT NULL")
    return row["c"]


async def stats() -> dict:
    total = await count_linked()
    dev = (await _one(
        "SELECT COUNT(*) AS c FROM scooters WHERE tg_id IS NOT NULL AND has_device = 1"))["c"]
    alerts = (await _one("SELECT COUNT(*) AS c FROM alerts"))["c"]
    models = await _all(
        "SELECT model, COUNT(*) AS c FROM scooters WHERE tg_id IS NOT NULL GROUP BY model ORDER BY c DESC"
    )
    return {"users": total, "with_dev": dev, "without_dev": total - dev,
            "alerts": alerts, "models": [(m["model"], m["c"]) for m in models]}


# ---------- ogohlantirishlar ----------
async def log_alert(admin_id, target, lat, lon, danger_time, ok, fail):
    await _exec(
        "INSERT INTO alerts (admin_id, target, lat, lon, danger_time, ok, fail, created_at)"
        " VALUES (?, ?, ?, ?, ?, ?, ?, ?)",
        (admin_id, target, lat, lon, danger_time, ok, fail, now_str()),
    )


async def last_alerts(limit: int = 10):
    return await _all("SELECT * FROM alerts ORDER BY id DESC LIMIT ?", (limit,))
