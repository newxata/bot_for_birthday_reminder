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
        "name": "Светлано",
        "date": "21.03",
        "message": 'хто я такий, щоб щось казати про стосунки між чоловіком і жінкою, адже я лише код програми, але, Света, я ж бачу як Сергій тебе любить - бережи цю любов - вона безцінна',
    },
    {
        "name": "Сергію",
        "date": "21.03",
        "message": 'треба діяти, одними словами ти результатів не добʼєшся, за любов треба боротися, якщо жінка каже, що хоче дом, машину, та фін.безпеку, то так і має бути, і не через 5 років, а вже тут і зараз!',
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
            reminder = f"{name}, {birthday_text}"
            send_telegram(reminder)
            logging.info(f"🎂 Нагадування про ДН: {name}")

    logging.info("✅ Робота завершена")


if __name__ == "__main__":
    main()
