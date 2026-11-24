from aiogram.types import (InlineKeyboardButton, InlineKeyboardMarkup, KeyboardButton,
                           ReplyKeyboardMarkup)
from aiogram.utils.keyboard import InlineKeyboardBuilder

from config import MODELS

BTN_STATUS = "🛡 Himoya holati"
BTN_SCOOTER = "🛴 Skuterim"
BTN_SOS = "🚨 SOS"
BTN_HELP = "🆘 Yordam"
BTN_ABOUT = "ℹ️ Bot haqida"
BTN_SETTINGS = "⚙️ Sozlamalar"
BTN_CANCEL = "❌ Bekor qilish"


def main_menu() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[
            [KeyboardButton(text=BTN_STATUS), KeyboardButton(text=BTN_SCOOTER)],
            [KeyboardButton(text=BTN_SOS), KeyboardButton(text=BTN_HELP)],
            [KeyboardButton(text=BTN_SETTINGS), KeyboardButton(text=BTN_ABOUT)],
        ],
        resize_keyboard=True,
        input_field_placeholder="Bo'limni tanlang 👇",
    )


def cancel_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text=BTN_CANCEL)]], resize_keyboard=True)


def sos_kb() -> ReplyKeyboardMarkup:
    return ReplyKeyboardMarkup(
        keyboard=[[KeyboardButton(text="📍 Joylashuvni yuborish", request_location=True)],
                  [KeyboardButton(text=BTN_CANCEL)]],
        resize_keyboard=True,
    )


def models_kb(prefix: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for m in MODELS:
        b.button(text=f"🛴 {m}", callback_data=f"{prefix}:{m}")
    b.adjust(2)
    return b.as_markup()


def device_kb(prefix: str) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="✅ Ha, bor", callback_data=f"{prefix}:1")
    b.button(text="❌ Yo'q", callback_data=f"{prefix}:0")
    b.adjust(2)
    return b.as_markup()


def settings_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="🛴 Modelni o'zgartirish", callback_data="set:model")
    b.button(text="📡 Qurilma holatini o'zgartirish", callback_data="set:device")
    b.button(text="🚪 Hisobdan chiqish", callback_data="set:logout")
    b.adjust(1)
    return b.as_markup()


def logout_confirm_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="✅ Ha, chiqaman", callback_data="logout:yes")
    b.button(text="↩️ Yo'q", callback_data="logout:no")
    b.adjust(2)
    return b.as_markup()


# ---------- admin ----------
def panel_kb() -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    b.button(text="🚨 Hammaga xavf yuborish", callback_data="alert:all")
    b.button(text="👤 Tanlangan foydalanuvchiga", callback_data="alert:pick")
    b.button(text="🔎 ID bo'yicha qidirib yuborish", callback_data="alert:find")
    b.button(text="👥 Foydalanuvchilar", callback_data="ul:0")
    b.button(text="📊 Statistika", callback_data="adm:stats")
    b.button(text="🗂 Tarix", callback_data="adm:history")
    b.button(text="✖️ Yopish", callback_data="adm:close")
    b.adjust(1, 1, 1, 2, 1, 1)
    return b.as_markup()


def back_panel_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[[InlineKeyboardButton(text="⬅️ Panelga qaytish", callback_data="adm:back")]])


def pager(prefix: str, page: int, pages: int) -> list[InlineKeyboardButton]:
    row = []
    if page > 0:
        row.append(InlineKeyboardButton(text="⬅️", callback_data=f"{prefix}:{page - 1}"))
    row.append(InlineKeyboardButton(text=f"{page + 1}/{pages}", callback_data="noop"))
    if page < pages - 1:
        row.append(InlineKeyboardButton(text="➡️", callback_data=f"{prefix}:{page + 1}"))
    return row


def users_list_kb(page: int, pages: int) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        pager("ul", page, pages),
        [InlineKeyboardButton(text="⬅️ Panelga qaytish", callback_data="adm:back")],
    ])


def pick_kb(rows, page: int, pages: int) -> InlineKeyboardMarkup:
    b = InlineKeyboardBuilder()
    for r in rows:
        dev = "📡" if r["has_device"] else "🚫"
        b.button(text=f"{dev} {r['scooter_id']} • {r['full_name'] or '—'}",
                 callback_data=f"pk:{r['tg_id']}")
    b.adjust(1)
    kb = b.as_markup()
    kb.inline_keyboard.append(pager("pkp", page, pages))
    kb.inline_keyboard.append(
        [InlineKeyboardButton(text="⬅️ Panelga qaytish", callback_data="adm:back")])
    return kb


def time_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🕐 Hozir", callback_data="time:now")],
        [InlineKeyboardButton(text="❌ Bekor qilish", callback_data="adm:cancel")],
    ])


def confirm_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[[
        InlineKeyboardButton(text="✅ Yuborish", callback_data="send:yes"),
        InlineKeyboardButton(text="❌ Bekor", callback_data="adm:cancel"),
    ]])
