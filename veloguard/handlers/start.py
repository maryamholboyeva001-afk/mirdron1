"""/start, skuter ID bilan kirish va ro'yxatdan o'tish."""
from aiogram import F, Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

import db
import keyboards as kb
import texts as t
from config import MODELS, SUPPORT_CONTACT
from states import Login
from utils import ID_RE, device_text, esc, send_sticker

router = Router()


def _name(user) -> str:
    return user.full_name or user.username or str(user.id)


async def _protected(message: Message, row) -> None:
    text = t.PROTECTED.format(sid=esc(row["scooter_id"]))
    if not row["has_device"]:
        text += t.NO_DEVICE_HINT.format(support=esc(SUPPORT_CONTACT))
    await send_sticker(message.bot, message.chat.id, "protected")
    await message.answer(text, reply_markup=kb.main_menu())


@router.message(CommandStart())
async def cmd_start(message: Message, state: FSMContext):
    await state.clear()
    row = await db.get_by_tg(message.from_user.id)
    if row:
        await message.answer(
            t.WELCOME_BACK.format(name=esc(_name(message.from_user)), sid=esc(row["scooter_id"])),
            reply_markup=kb.main_menu())
        return
    await send_sticker(message.bot, message.chat.id, "welcome")
    await message.answer(t.WELCOME, reply_markup=None)
    await state.set_state(Login.scooter_id)


@router.message(Login.scooter_id, F.text)
async def got_id(message: Message, state: FSMContext):
    sid = message.text.strip()
    if not ID_RE.match(sid):
        await message.answer(t.BAD_ID)
        return
    row = await db.get_by_sid(sid)
    user = message.from_user
    if row:
        if row["tg_id"] and row["tg_id"] != user.id:
            await message.answer(t.ID_TAKEN.format(support=esc(SUPPORT_CONTACT)))
            return
        await db.link_scooter(row["scooter_id"], user.id, _name(user), user.username)
        row = await db.get_by_sid(sid)
        await state.clear()
        await _protected(message, row)
        return
    await state.update_data(sid=sid)
    await state.set_state(Login.model)
    await message.answer(t.NOT_REGISTERED.format(sid=esc(sid)), reply_markup=kb.models_kb("reg_model"))


@router.callback_query(Login.model, F.data.startswith("reg_model:"))
async def got_model(call: CallbackQuery, state: FSMContext):
    model = call.data.split(":", 1)[1]
    if model not in MODELS:
        await call.answer("Noto'g'ri tanlov", show_alert=True)
        return
    await state.update_data(model=model)
    await state.set_state(Login.device)
    await call.message.edit_text(f"🛴 Model: <b>{esc(model)}</b> ✅\n\n{t.ASK_DEVICE}",
                                 reply_markup=kb.device_kb("reg_dev"))
    await call.answer()


@router.callback_query(Login.device, F.data.startswith("reg_dev:"))
async def got_device(call: CallbackQuery, state: FSMContext):
    has_dev = call.data.endswith(":1")
    data = await state.get_data()
    user = call.from_user
    await db.create_scooter(data["sid"], user.id, _name(user), user.username,
                            data["model"], has_dev)
    await state.clear()
    await call.message.edit_text(t.REGISTERED.format(
        sid=esc(data["sid"]), model=esc(data["model"]), device=device_text(has_dev)))
    await call.answer("🎉")
    row = await db.get_by_tg(user.id)
    await _protected(call.message, row)


@router.message(Login.model)
@router.message(Login.device)
async def use_buttons(message: Message):
    await message.answer("👆 Iltimos, yuqoridagi tugmalardan birini tanlang.")
