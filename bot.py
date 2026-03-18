import requests
import os
from datetime import datetime
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s"
)

TELEGRAM_TOKEN = os.environ.get("TELEGRAM_TOKEN")
TELEGRAM_CHAT_ID = os.environ.get("TELEGRAM_CHAT_ID")


MEMBERS = [
    {
        "name": "Сергію",
        "date": "18.03",
        "message": 'Мій друг, це перший БОТ який запрацював, я ВІТАЮ тебе, ти найкращий!!!!',
    },
    # --- додавай нових учасників тут ---
]

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
            birthday_text = member.get("message")

            # Повідомлення тобі
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
