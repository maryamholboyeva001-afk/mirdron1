"""Botning barcha matnlari (HTML formatda)."""

WELCOME = (
    "🛡✨ <b>VeloGuard</b> botiga xush kelibsiz! ✨🛡\n\n"
    "🛴 Biz skuteringizni <b>24/7</b> kuzatamiz va xavf paytida darhol xabar beramiz.\n\n"
    "🔑 Davom etish uchun <b>skuter ID</b> raqamingizni kiriting 👇"
)
WELCOME_BACK = "👋 Qaytganingizdan xursandmiz, <b>{name}</b>! 💚\n🛴 Skuteringiz: <code>{sid}</code>"
ASK_ID_AGAIN = "🔑 Skuter ID raqamingizni kiriting 👇"
BAD_ID = (
    "⚠️ ID noto'g'ri formatda!\n"
    "📝 Faqat lotin harflari, raqam va <code>-</code> belgisi (3–20 belgi) ishlatiladi.\n"
    "🔁 Qaytadan urinib ko'ring."
)
ID_TAKEN = (
    "⛔ Bu ID boshqa Telegram hisobiga bog'langan.\n"
    "📞 Agar bu sizning skuteringiz bo'lsa, yordam xizmatiga murojaat qiling: {support}"
)
NOT_REGISTERED = (
    "🆕 <code>{sid}</code> ID botda topilmadi.\n"
    "📋 Keling, uni <b>ro'yxatdan o'tkazamiz</b>! 🚀\n\n"
    "🛴 Avval skuteringiz <b>modelini</b> tanlang 👇"
)
ASK_DEVICE = (
    "📡 Skuteringizda <b>VeloGuard qurilmasi</b> o'rnatilganmi?\n"
    "👇 Tanlang:"
)
REGISTERED = (
    "🎉 <b>Ro'yxatdan o'tdingiz!</b> 🎉\n\n"
    "🆔 ID: <code>{sid}</code>\n"
    "🛴 Model: <b>{model}</b>\n"
    "📡 VeloGuard qurilmasi: <b>{device}</b>"
)
PROTECTED = (
    "🛡✅ <b>VeloGuard sizni himoyasiga oldi!</b> ✅🛡\n\n"
    "🔒 Skuteringiz <code>{sid}</code> endi nazorat ostida.\n"
    "🚨 Xavf bo'lsa, sizga darhol xabar yuboramiz.\n"
    "😎 Xotirjam yuring!"
)
NO_DEVICE_HINT = (
    "\n\n💡 <i>Eslatma: qurilma o'rnatilmagan, shuning uchun himoya cheklangan. "
    "To'liq himoya uchun VeloGuard qurilmasini o'rnating: {support}</i> 📞"
)
DEVICE_YES = "✅ Bor"
DEVICE_NO = "❌ Yo'q"

MENU_TITLE = "📋 <b>Asosiy menyu</b>\n👇 Kerakli bo'limni tanlang:"
STATUS = (
    "🛡 <b>Himoya holati</b>\n\n"
    "🆔 ID: <code>{sid}</code>\n"
    "🛴 Model: <b>{model}</b>\n"
    "📡 Qurilma: <b>{device}</b>\n"
    "🔐 Holat: <b>{state}</b>\n"
    "📅 Ro'yxatdan o'tgan: {date}"
)
STATE_FULL = "✅ To'liq himoyalangan"
STATE_LIMITED = "⚠️ Cheklangan himoya"
MY_SCOOTER = (
    "🛴 <b>Mening skuterim</b>\n\n"
    "🆔 <code>{sid}</code>\n"
    "🏷 Model: <b>{model}</b>\n"
    "📡 Qurilma: <b>{device}</b>"
)
HELP = (
    "🆘 <b>Yordam markazi</b>\n\n"
    "📞 Aloqa: {support}\n"
    "🕐 Ish vaqti: 24/7\n\n"
    "❓ Savollaringiz bo'lsa, bemalol yozing! 💬"
)
ABOUT = (
    "ℹ️ <b>VeloGuard haqida</b>\n\n"
    "🛡 VeloGuard — skuterlar uchun xavfsizlik tizimi.\n"
    "📍 Joylashuvni kuzatish\n"
    "🚨 Xavf haqida zudlik bilan ogohlantirish\n"
    "🔒 Ishonchli himoya\n\n"
    "💚 Xavfsiz yo'llar tilaymiz!"
)
SETTINGS = "⚙️ <b>Sozlamalar</b>\n👇 Nimani o'zgartiramiz?"
CHOOSE_MODEL = "🛴 Yangi modelni tanlang 👇"
MODEL_UPDATED = "✅ Model <b>{model}</b> ga o'zgartirildi! 🎉"
DEVICE_UPDATED = "✅ Qurilma holati: <b>{device}</b> 📡"
LOGOUT_CONFIRM = "🚪 Hisobdan chiqmoqchimisiz?\n🔑 Qayta kirish uchun skuter ID kerak bo'ladi."
LOGGED_OUT = "👋 Hisobdan chiqdingiz. Qayta kirish uchun /start bosing 🔑"
NEED_LOGIN = "🔑 Avval /start bosib, skuter ID bilan kiring."

SOS_ASK = (
    "🚨 <b>SOS</b> 🚨\n\n"
    "📍 Joylashuvingizni yuboring (pastdagi tugma orqali) — "
    "VeloGuard jamoasi darhol xabardor qilinadi! 👇"
)
SOS_SENT = "✅ SOS yuborildi! 🆘 Jamoamiz siz bilan tez orada bog'lanadi 📞"
SOS_ADMIN = (
    "🆘🚨 <b>SOS signal!</b>\n\n"
    "👤 {name} {username}\n"
    "🆔 Skuter: <code>{sid}</code>\n"
    "🛴 Model: {model}\n"
    "🕐 Vaqt: {time}"
)
CANCELLED = "❌ Bekor qilindi."

# ---------- ADMIN ----------
NO_ACCESS = "⛔ Sizda admin panelga ruxsat yo'q! 🔒"
PANEL = "🛠 <b>VeloGuard admin paneli</b> 🛠\n👇 Amalni tanlang:"
STATS = (
    "📊 <b>Statistika</b>\n\n"
    "👥 Foydalanuvchilar: <b>{users}</b>\n"
    "📡 Qurilmasi borlar: <b>{with_dev}</b>\n"
    "🚫 Qurilmasizlar: <b>{without_dev}</b>\n"
    "🚨 Yuborilgan ogohlantirishlar: <b>{alerts}</b>\n\n"
    "🛴 <b>Modellar:</b>\n{models}"
)
USERS_LIST_TITLE = "👥 <b>Foydalanuvchilar</b> (sahifa {page}/{pages}, jami {total})\n\n"
USER_LINE = "{n}. {dev} <code>{sid}</code> — {model} — {name}\n"
PICK_USER = "👤 Foydalanuvchini tanlang (sahifa {page}/{pages}) 👇"
NO_USERS = "😕 Hozircha foydalanuvchilar yo'q."
ASK_FIND_ID = "🔎 Foydalanuvchining skuter ID sini kiriting 👇"
USER_NOT_FOUND = "❌ Bunday ID topilmadi yoki u akkauntga ulanmagan."
TARGET_ALL = "👥 barcha foydalanuvchilar"
TARGET_ONE = "👤 {sid} ({name})"
ASK_LOCATION = (
    "📍 <b>Xavf joylashuvini yuboring</b>\n\n"
    "📎 Telegramda «Joylashuv» orqali xaritadan belgilang yoki\n"
    "✍️ <code>41.311081, 69.240562</code> ko'rinishida yozing 👇"
)
BAD_LOCATION = "⚠️ Joylashuv tushunarsiz. Lokatsiya yuboring yoki <code>lat, lon</code> yozing."
ASK_TIME = (
    "🕐 <b>Xavf vaqtini kiriting</b>\n"
    "Masalan: <code>14:35</code> yoki <code>24.11 14:35</code>\n"
    "yoki «Hozir» tugmasini bosing 👇"
)
BAD_TIME = "⚠️ Vaqt bo'sh yoki juda uzun. Qaytadan kiriting."
CONFIRM = (
    "📝 <b>Tekshiring:</b>\n\n"
    "🎯 Kimga: {target}\n"
    "📍 Joylashuv: <code>{lat}, {lon}</code>\n"
    "🕐 Xavf vaqti: <b>{time}</b>\n\n"
    "✅ Yuboraylikmi?"
)
SENDING = "⏳ Yuborilmoqda... 🚀"
SENT_REPORT = (
    "🎉 <b>Yuborish tugadi!</b> 🎉\n\n"
    "✅ Yetkazildi: <b>{ok}</b>\n"
    "❌ Xato: <b>{fail}</b>"
)
HISTORY_TITLE = "🗂 <b>So'nggi ogohlantirishlar</b>\n\n"
HISTORY_LINE = "🕐 {created} → {target} | ✅ {ok} ❌ {fail} | ⏰ {time}\n"
NO_HISTORY = "📭 Hali ogohlantirish yuborilmagan."

# Foydalanuvchiga boradigan xavf xabari
DANGER = (
    "🚨🚨🚨 <b>DIQQAT! XAVF!</b> 🚨🚨🚨\n\n"
    "⚠️ <b>Transport vositangiz xavf ostida!</b> 🛴💥\n\n"
    "🆔 Skuter: <code>{sid}</code>\n"
    "🕐 Xavf vaqti: <b>{time}</b>\n"
    "📍 Joylashuv pastda yuborilgan 👇\n\n"
    "🏃 Zudlik bilan harakat qiling va kerak bo'lsa 🚓 politsiyaga (102) murojaat qiling!"
)
