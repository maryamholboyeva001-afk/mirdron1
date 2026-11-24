# 🛡 VeloGuard Telegram bot

## Ishga tushirish
```bash
pip install -r requirements.txt
cp .env.example .env      # BOT_TOKEN va ADMIN_IDS ni to'ldiring
python main.py
```
- `/start` — skuter ID so'raydi; ID yangi bo'lsa model va qurilma tanlanadi, ro'yxatdan o'tadi.
- ID bilan kirganda: «VeloGuard sizni himoyasiga oldi».
- `/panel` — faqat adminlar: hammaga yoki tanlangan foydalanuvchiga xavf xabari + joylashuv + vaqt.
- Stikerlar: `.env` ga file_id yozing (botga stiker yuborib, update ichidan file_id ni oling).
