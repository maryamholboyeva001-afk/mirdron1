import os
from dotenv import load_dotenv

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN", "")
ADMIN_IDS = {
    int(x) for x in os.getenv("ADMIN_IDS", "").replace(" ", "").split(",") if x.isdigit()
}
DB_PATH = os.getenv("DB_PATH", "veloguard.db")
TIMEZONE = os.getenv("TIMEZONE", "Asia/Tashkent")
SUPPORT_CONTACT = os.getenv("SUPPORT_CONTACT", "@veloguard_support")

STICKERS = {
    name: os.getenv(f"STICKER_{name.upper()}", "")
    for name in ("welcome", "protected", "alert", "done")
}

MODELS = ["Kugoo", "Xiaomi", "Ninebot", "Yadea", "Voltrix", "Boshqa"]
PAGE_SIZE = 8
SEND_DELAY = 0.05  # xabarlar orasidagi pauza (Telegram limiti uchun)
