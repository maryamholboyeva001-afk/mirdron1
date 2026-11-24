import html
import logging
import re
from datetime import datetime
from zoneinfo import ZoneInfo

from aiogram import Bot
from aiogram.exceptions import TelegramBadRequest

from config import STICKERS, TIMEZONE

log = logging.getLogger(__name__)
ID_RE = re.compile(r"^[A-Za-z0-9\-]{3,20}$")


def esc(text) -> str:
    return html.escape(str(text or ""))


def now_time() -> str:
    return datetime.now(ZoneInfo(TIMEZONE)).strftime("%d.%m.%Y %H:%M")


def parse_coords(text: str):
    """'41.31, 69.24' -> (41.31, 69.24) yoki None."""
    m = re.match(r"^\s*(-?\d{1,3}(?:\.\d+)?)\s*[,; ]\s*(-?\d{1,3}(?:\.\d+)?)\s*$", text or "")
    if not m:
        return None
    lat, lon = float(m.group(1)), float(m.group(2))
    if -90 <= lat <= 90 and -180 <= lon <= 180:
        return lat, lon
    return None


async def send_sticker(bot: Bot, chat_id: int, key: str) -> None:
    """Agar .env da stiker file_id berilgan bo'lsa yuboradi."""
    fid = STICKERS.get(key)
    if not fid:
        return
    try:
        await bot.send_sticker(chat_id, fid)
    except TelegramBadRequest as e:
        log.warning("Stiker yuborilmadi (%s): %s", key, e)


def device_text(flag) -> str:
    return "✅ Bor" if flag else "❌ Yo'q"
