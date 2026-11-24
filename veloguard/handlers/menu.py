"""Foydalanuvchi menyusi, sozlamalar va SOS."""
from aiogram import F, Router
from aiogram.filters import Command
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import db
import keyboards as kb
import texts as t
from config import ADMIN_IDS, MODELS, SUPPORT_CONTACT
from states import Sos
from utils import device_text, esc, now_time, send_sticker

router = Router()


async def _user(message: Message):
    row = await db.get_by_tg(message.from_user.id)
    if not row:
        await message.answer(t.NEED_LOGIN)
    return row


@router.message(Command("panel"))
async def panel_denied(message: Message):
    # Adminlar admin routerida tutiladi, bu yerga faqat oddiy foydalanuvchi tushadi.
    await message.answer(t.NO_ACCESS)


@router.message(Command("menu"))
async def cmd_menu(message: Message):
    if await _user(message):
        await message.answer(t.MENU_TITLE, reply_markup=kb.main_menu())


@router.message(F.text == kb.BTN_STATUS)
async def status(message: Message):
    row = await _user(message)
    if not row:
        return
    state = t.STATE_FULL if row["has_device"] else t.STATE_LIMITED
    await send_sticker(message.bot, message.chat.id, "protected")
    await message.answer(t.STATUS.format(
        sid=esc(row["scooter_id"]), model=esc(row["model"]),
        device=device_text(row["has_device"]), state=state, date=esc(row["created_at"])))


@router.message(F.text == kb.BTN_SCOOTER)
async def my_scooter(message: Message):
    row = await _user(message)
    if row:
        await message.answer(t.MY_SCOOTER.format(
            sid=esc(row["scooter_id"]), model=esc(row["model"]),
            device=device_text(row["has_device"])))


@router.message(F.text == kb.BTN_HELP)
async def help_(message: Message):
    await message.answer(t.HELP.format(support=esc(SUPPORT_CONTACT)))


@router.message(F.text == kb.BTN_ABOUT)
async def about(message: Message):
    await message.answer(t.ABOUT)


# ---------- sozlamalar ----------
@router.message(F.text == kb.BTN_SETTINGS)
async def settings(message: Message):
    if await _user(message):
        await message.answer(t.SETTINGS, reply_markup=kb.settings_kb())


@router.callback_query(F.data == "set:model")
async def set_model_menu(call: CallbackQuery):
    await call.message.edit_text(t.CHOOSE_MODEL, reply_markup=kb.models_kb("chg_model"))
    await call.answer()


@router.callback_query(F.data.startswith("chg_model:"))
async def chg_model(call: CallbackQuery):
    model = call.data.split(":", 1)[1]
    if model not in MODELS:
        await call.answer("Noto'g'ri tanlov", show_alert=True)
        return
    await db.set_model(call.from_user.id, model)
    await call.message.edit_text(t.MODEL_UPDATED.format(model=esc(model)))
    await call.answer("✅")


@router.callback_query(F.data == "set:device")
async def set_device_menu(call: CallbackQuery):
    await call.message.edit_text(t.ASK_DEVICE, reply_markup=kb.device_kb("chg_dev"))
    await call.answer()


@router.callback_query(F.data.startswith("chg_dev:"))
async def chg_dev(call: CallbackQuery):
    has_dev = call.data.endswith(":1")
    await db.set_device(call.from_user.id, has_dev)
    await call.message.edit_text(t.DEVICE_UPDATED.format(device=device_text(has_dev)))
    await call.answer("✅")


@router.callback_query(F.data == "set:logout")
async def logout_ask(call: CallbackQuery):
    await call.message.edit_text(t.LOGOUT_CONFIRM, reply_markup=kb.logout_confirm_kb())
    await call.answer()


@router.callback_query(F.data == "logout:yes")
async def logout_yes(call: CallbackQuery):
    await db.unlink_tg(call.from_user.id)
    await call.message.edit_text(t.LOGGED_OUT)
    await call.answer("👋")


@router.callback_query(F.data == "logout:no")
async def logout_no(call: CallbackQuery):
    await call.message.edit_text(t.MENU_TITLE)
    await call.answer()


# ---------- SOS ----------
@router.message(F.text == kb.BTN_SOS)
async def sos_start(message: Message, state: FSMContext):
    if not await _user(message):
        return
    await state.set_state(Sos.location)
    await message.answer(t.SOS_ASK, reply_markup=kb.sos_kb())


@router.message(Sos.location, F.location)
async def sos_location(message: Message, state: FSMContext):
    row = await db.get_by_tg(message.from_user.id)
    await state.clear()
    username = f"@{message.from_user.username}" if message.from_user.username else ""
    text = t.SOS_ADMIN.format(
        name=esc(message.from_user.full_name), username=esc(username),
        sid=esc(row["scooter_id"]), model=esc(row["model"]), time=now_time())
    for admin_id in ADMIN_IDS:
        try:
            await send_sticker(message.bot, admin_id, "alert")
            await message.bot.send_message(admin_id, text)
            await message.bot.send_location(
                admin_id, message.location.latitude, message.location.longitude)
        except Exception:
            continue
    await message.answer(t.SOS_SENT, reply_markup=kb.main_menu())


@router.message(Sos.location)
async def sos_cancel(message: Message, state: FSMContext):
    await state.clear()
    await message.answer(t.CANCELLED, reply_markup=kb.main_menu())
