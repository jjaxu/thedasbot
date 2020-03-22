import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./vendored"))

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)


def trigger(event, context):

    data = json.loads(event["body"])
    message = str(data["message"]["text"])
    chat_id = data["message"]["chat"]["id"]
    first_name = data["message"]["chat"]["first_name"]

    if message.startswith("/start"):
        response = "Hello {}! Welcome to the DAS bot!".format(first_name)
    elif message.startswith("/help"):
        response = "You have invoked the help command!"
    elif message.startswith("/fact"):
        response = "Here's a fun fact:"
    else:
        response = "Sorry, I don't understand. Try /help"

    data = {
        "chat_id": chat_id,
        "text": response.encode("utf8")
    }
    url = BASE_URL + "/sendMessage"
    requests.post(url, data)

    return {"statusCode": 200}
