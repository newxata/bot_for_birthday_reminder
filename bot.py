import requests
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

# ============================================================
#  НАЛАШТУВАННЯ
# ============================================================

TELEGRAM_TOKEN = "ВАШ_ТОКЕН_TELEGRAM_БОТА"  # від @BotFather
TELEGRAM_CHAT_ID = "ВАШ_CHAT_ID"            # твій особистий chat_id

# ============================================================
#  УЧАСНИКИ VIBER-ГРУПИ
#  date: "ДД.ММ"
#  message: None = використати DEFAULT_MESSAGE
# ============================================================

MEMBERS = [
    {
        "name": "Олена",
        "date": "15.03",
        "message": None,
    },
    {
        "name": "Василь",
        "date": "22.07",
        "message": None,
    },
    {
        "name": "Марія",
        "date": "05.11",
        "message": "🌸 Маріє, нехай цей день буде сповнений радості та тепла! Щасливого дня народження! 🎂",
    },
    # --- додавай нових учасників тут ---
]

# ============================================================
#  СТАНДАРТНЕ ПРИВІТАННЯ  ({name} = ім'я учасника)
# ============================================================

DEFAULT_MESSAGE = (
    "🎉 Вітаємо {name} з Днем народження! 🎂\n\n"
    "Нехай цей особливий день принесе лише радість, "
    "тепло та усмішки. Бажаємо здоров'я, щастя "
    "та здійснення всіх мрій! 🥳🎊"
)

# ============================================================
#  ЛОГІКА — не потрібно редагувати
# ============================================================

def send_telegram(text: str) -> bool:
    url = f"https://api.telegram.org/bot{TELEGRAM_TOKEN}/sendMessage"
    payload = {
        "chat_id": TELEGRAM_CHAT_ID,
        "text": text,
        "parse_mode": "HTML"
    }
    try:
        resp = requests.post(url, json=payload, timeout=10)
        result = resp.json()
        if result.get("ok"):
            logging.info("✅ Нагадування надіслано в Telegram")
            return True
        else:
            logging.error(f"❌ Помилка Telegram API: {result}")
            return False
    except Exception as e:
        logging.error(f"❌ Виняток: {e}")
        return False


def main():
    today = datetime.now().strftime("%d.%m")
    logging.info(f"🔍 Перевірка днів народження: {today}")

    for member in MEMBERS:
        if member["date"] == today:
            name = member["name"]
            birthday_text = member.get("message") or DEFAULT_MESSAGE.format(name=name)

            # Повідомлення тобі в Telegram
            reminder = (
                f"🎂 <b>Сьогодні день народження — {name}!</b>\n\n"
                f"Скопіюй і відправ у Viber-групу:\n"
                f"——————————————\n"
                f"{birthday_text}\n"
                f"——————————————"
            )
            send_telegram(reminder)
            logging.info(f"🎂 Нагадування про ДН: {name}")

    logging.info("✅ Робота завершена")


if __name__ == "__main__":
    main()
