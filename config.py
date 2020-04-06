from os import environ

# Bot token & API
TOKEN = environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

ALLOW_EDITED_MESSAGES = False
