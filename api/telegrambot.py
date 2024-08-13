from api.index import get_tg_token
import requests
# \U0001F480 - 💀

#variables (supposted to be hidden)
telegram_bot_list:list[str] = get_tg_token().split(" ")
bot_token = telegram_bot_list[0]
chat_id = telegram_bot_list[1]

def send_telegram_message(message):
    url = f"https://api.telegram.org/bot{bot_token}/sendMessage"
    data = {"chat_id": chat_id, "text": message}
    response = requests.post(url, json=data)

    if response.status_code == 200:
        print("Message sent successfully")
    else:
        print("Failed to send message")

if __name__ == "__main__":
    send_telegram_message("Сервис отзыва запущен \U0001F480")