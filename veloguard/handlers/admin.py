"""/panel — admin paneli va xavf ogohlantirishlarini yuborish."""
import asyncio
import logging
import math

from aiogram import F, Bot, Router
from aiogram.exceptions import TelegramForbiddenError, TelegramRetryAfter, TelegramBadRequest
from aiogram.filters import BaseFilter, Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message, ReplyKeyboardRemove

import db
import keyboards as kb
import texts as t
from config import ADMIN_IDS, PAGE_SIZE, SEND_DELAY
from states import AlertFlow
from utils import esc, now_time, parse_coords, send_sticker

log = logging.getLogger(__name__)


class IsAdmin(BaseFilter):
    async def __call__(self, event) -> bool:
        return bool(event.from_user and event.from_user.id in ADMIN_IDS)


router = Router()
router.message.filter(IsAdmin())
router.callback_query.filter(IsAdmin())


@router.message(Command("panel"))
async def cmd_panel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(t.PANEL, reply_markup=kb.panel_kb())


@router.callback_query(F.data == "noop")
async def noop(call: CallbackQuery):
    await call.answer()


@router.callback_query(F.data == "adm:back")
async def back(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.edit_text(t.PANEL, reply_markup=kb.panel_kb())
    await call.answer()


@router.callback_query(F.data == "adm:close")
async def close(call: CallbackQuery):
    await call.message.delete()
    await call.answer()


@router.callback_query(F.data == "adm:cancel")
async def cancel(call: CallbackQuery, state: FSMContext):
    await state.clear()
    await call.message.answer(t.CANCELLED, reply_markup=ReplyKeyboardRemove())
    await call.message.answer(t.PANEL, reply_markup=kb.panel_kb())
    await call.answer()


# ---------- statistika, tarix, ro'yxat ----------
@router.callback_query(F.data == "adm:stats")
async def stats(call: CallbackQuery):
    s = await db.stats()
    models = "\n".join(f"• {esc(m)}: <b>{c}</b>" for m, c in s["models"]) or "—"
    await call.message.edit_text(
        t.STATS.format(users=s["users"], with_dev=s["with_dev"], without_dev=s["without_dev"],
                       alerts=s["alerts"], models=models),
        reply_markup=kb.back_panel_kb())
    await call.answer()


@router.callback_query(F.data == "adm:history")
async def history(call: CallbackQuery):
    rows = await db.last_alerts(10)
    if not rows:
        text = t.NO_HISTORY
    else:
        text = t.HISTORY_TITLE + "".join(
            t.HISTORY_LINE.format(created=r["created_at"], target=esc(r["target"]),
                                  ok=r["ok"], fail=r["fail"], time=esc(r["danger_time"]))
            for r in rows)
    await call.message.edit_text(text, reply_markup=kb.back_panel_kb())
    await call.answer()


@router.callback_query(F.data.startswith("ul:"))
async def users_list(call: CallbackQuery):
    page = int(call.data.split(":")[1])
    total = await db.count_linked()
    if not total:
        await call.message.edit_text(t.NO_USERS, reply_markup=kb.back_panel_kb())
        await call.answer()
        return
    pages = math.ceil(total / PAGE_SIZE)
    page = max(0, min(page, pages - 1))
    rows = await db.linked_page(page, PAGE_SIZE)
    text = t.USERS_LIST_TITLE.format(page=page + 1, pages=pages, total=total)
    for i, r in enumerate(rows, start=page * PAGE_SIZE + 1):
        text += t.USER_LINE.format(n=i, dev="📡" if r["has_device"] else "🚫",
                                   sid=esc(r["scooter_id"]), model=esc(r["model"]),
                                   name=esc(r["full_name"]))
    await call.message.edit_text(text, reply_markup=kb.users_list_kb(page, pages))
    await call.answer()


# ---------- ogohlantirish: kimga? ----------
async def _ask_location(msg_target, state: FSMContext, target_label: str, target_ids):
    await state.update_data(target_label=target_label, target_ids=target_ids)
    await state.set_state(AlertFlow.location)
    await msg_target.answer(t.ASK_LOCATION, reply_markup=kb.cancel_kb())


@router.callback_query(F.data == "alert:all")
async def alert_all(call: CallbackQuery, state: FSMContext):
    users = await db.all_linked()
    if not users:
        await call.answer(t.NO_USERS, show_alert=True)
        return
    await call.message.delete()
    await _ask_location(call.message, state, t.TARGET_ALL, [u["tg_id"] for u in users])
    await call.answer()


async def _show_picker(call: CallbackQuery, page: int):
    total = await db.count_linked()
    if not total:
        await call.answer(t.NO_USERS, show_alert=True)
        return
    pages = math.ceil(total / PAGE_SIZE)
    page = max(0, min(page, pages - 1))
    rows = await db.linked_page(page, PAGE_SIZE)
    await call.message.edit_text(t.PICK_USER.format(page=page + 1, pages=pages),
                                 reply_markup=kb.pick_kb(rows, page, pages))
    await call.answer()


@router.callback_query(F.data == "alert:pick")
async def alert_pick(call: CallbackQuery):
    await _show_picker(call, 0)


@router.callback_query(F.data.startswith("pkp:"))
async def alert_pick_page(call: CallbackQuery):
    await _show_picker(call, int(call.data.split(":")[1]))


@router.callback_query(F.data.startswith("pk:"))
async def alert_picked(call: CallbackQuery, state: FSMContext):
    tg_id = int(call.data.split(":")[1])
    row = await db.get_by_tg(tg_id)
    if not row:
        await call.answer(t.USER_NOT_FOUND, show_alert=True)
        return
    await call.message.delete()
    label = t.TARGET_ONE.format(sid=esc(row["scooter_id"]), name=esc(row["full_name"]))
    await _ask_location(call.message, state, label, [tg_id])
    await call.answer()


@router.callback_query(F.data == "alert:find")
async def alert_find(call: CallbackQuery, state: FSMContext):
    await state.set_state(AlertFlow.find_id)
    await call.message.edit_text(t.ASK_FIND_ID)
    await call.answer()


@router.message(AlertFlow.find_id, F.text)
async def alert_find_got(message: Message, state: FSMContext):
    row = await db.get_by_sid(message.text.strip())
    if not row or not row["tg_id"]:
        await message.answer(t.USER_NOT_FOUND)
        return
    label = t.TARGET_ONE.format(sid=esc(row["scooter_id"]), name=esc(row["full_name"]))
    await _ask_location(message, state, label, [row["tg_id"]])


# ---------- joylashuv, vaqt, tasdiq ----------
@router.message(AlertFlow.location, F.location)
async def got_location(message: Message, state: FSMContext):
    await state.update_data(lat=message.location.latitude, lon=message.location.longitude)
    await state.set_state(AlertFlow.time)
    await message.answer("📍 Joylashuv qabul qilindi ✅", reply_markup=ReplyKeyboardRemove())
    await message.answer(t.ASK_TIME, reply_markup=kb.time_kb())


@router.message(AlertFlow.location, F.text)
async def got_location_text(message: Message, state: FSMContext):
    if message.text == kb.BTN_CANCEL:
        await state.clear()
        await message.answer(t.CANCELLED, reply_markup=ReplyKeyboardRemove())
        await message.answer(t.PANEL, reply_markup=kb.panel_kb())
        return
    coords = parse_coords(message.text)
    if not coords:
        await message.answer(t.BAD_LOCATION)
        return
    await state.update_data(lat=coords[0], lon=coords[1])
    await state.set_state(AlertFlow.time)
    await message.answer("📍 Joylashuv qabul qilindi ✅", reply_markup=ReplyKeyboardRemove())
    await message.answer(t.ASK_TIME, reply_markup=kb.time_kb())


async def _show_confirm(msg: Message, state: FSMContext, danger_time: str):
    await state.update_data(danger_time=danger_time)
    await state.set_state(AlertFlow.confirm)
    d = await state.get_data()
    await msg.answer(t.CONFIRM.format(target=d["target_label"], lat=d["lat"], lon=d["lon"],
                                      time=esc(danger_time)), reply_markup=kb.confirm_kb())


@router.callback_query(AlertFlow.time, F.data == "time:now")
async def time_now(call: CallbackQuery, state: FSMContext):
    await call.message.delete()
    await _show_confirm(call.message, state, now_time())
    await call.answer()


@router.message(AlertFlow.time, F.text)
async def got_time(message: Message, state: FSMContext):
    text = message.text.strip()
    if not text or len(text) > 50:
        await message.answer(t.BAD_TIME)
        return
    await _show_confirm(message, state, text)


async def _deliver(bot: Bot, tg_id: int, sid: str, lat, lon, danger_time) -> bool:
    for _ in range(3):
        try:
            await send_sticker(bot, tg_id, "alert")
            await bot.send_message(tg_id, t.DANGER.format(sid=esc(sid), time=esc(danger_time)))
            await bot.send_location(tg_id, lat, lon)
            return True
        except TelegramRetryAfter as e:
            await asyncio.sleep(e.retry_after)
        except (TelegramForbiddenError, TelegramBadRequest):
            return False
        except Exception as e:  # noqa: BLE001
            log.warning("Yuborishda xato %s: %s", tg_id, e)
            return False
    return False


@router.callback_query(AlertFlow.confirm, F.data == "send:yes")
async def send_alert(call: CallbackQuery, state: FSMContext):
    d = await state.get_data()
    await state.clear()
    await call.message.edit_text(t.SENDING)
    ok = fail = 0
    for tg_id in d["target_ids"]:
        row = await db.get_by_tg(tg_id)
        if not row:
            fail += 1
            continue
        if await _deliver(call.bot, tg_id, row["scooter_id"], d["lat"], d["lon"], d["danger_time"]):
            ok += 1
        else:
            fail += 1
        await asyncio.sleep(SEND_DELAY)
    await db.log_alert(call.from_user.id, d["target_label"], d["lat"], d["lon"],
                       d["danger_time"], ok, fail)
    await send_sticker(call.bot, call.from_user.id, "done")
    await call.message.edit_text(t.SENT_REPORT.format(ok=ok, fail=fail),
                                 reply_markup=kb.back_panel_kb())
    await call.answer("🎉")
