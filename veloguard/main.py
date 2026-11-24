import asyncio
import logging

from aiogram import Bot, Dispatcher
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.fsm.storage.memory import MemoryStorage
from aiogram.types import BotCommand

import db
from config import BOT_TOKEN
from handlers import admin, menu, start


async def main() -> None:
    logging.basicConfig(level=logging.INFO,
                        format="%(asctime)s %(levelname)s %(name)s: %(message)s")
    if not BOT_TOKEN:
        raise SystemExit("BOT_TOKEN topilmadi. .env faylini to'ldiring.")
    await db.init_db()
    bot = Bot(BOT_TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
    dp = Dispatcher(storage=MemoryStorage())
    # Tartib muhim: admin avval, oddiy menyu keyin
    dp.include_router(admin.router)
    dp.include_router(start.router)
    dp.include_router(menu.router)
    await bot.set_my_commands([
        BotCommand(command="start", description="🛡 Boshlash"),
        BotCommand(command="menu", description="📋 Menyu"),
        BotCommand(command="panel", description="🛠 Admin panel"),
    ])
    await bot.delete_webhook(drop_pending_updates=True)
    await dp.start_polling(bot)


if __name__ == "__main__":
    asyncio.run(main())
