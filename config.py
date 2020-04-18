from os import environ

# Bot token & API
TOKEN = environ['TELEGRAM_TOKEN']
BASE_URL = f"https://api.telegram.org/bot{TOKEN}"
