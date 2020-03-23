import json
import os
import sys

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./vendored"))

import requests

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)


def trigger(event, context):

    data = json.loads(event["body"])

    if "inline_query" in data:
        return handle_inline_query(data)


    message = str(data["message"]["text"])
    chat_id = data["message"]["chat"]["id"]
    first_name = data["message"]["chat"]["first_name"]

    if message.startswith("/start"):
        response = "Hello {}! Welcome to the DAS bot!".format(first_name)
    elif message.startswith("/help"):
        response = "You have invoked the help command!"
    elif message.startswith("/debug"):
        response = str(data)
    elif message.startswith("/joke"):
        r = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "text/plain"})
        response = r.content.decode() if r.ok else "Oops! Can't fetch joke right now."
    elif message.startswith("/fact"):
        r = requests.get("https://www.mentalfloss.com/api/facts")
        response = str(r.json()[0]['headline']).replace("<em>", "__").replace("</em>", "__").replace("<i>", "__").replace("</i>", "__") if r.ok else "Oops! Can't fetch fact right now."
    else:
        response = "Sorry, I don't understand. Try /help"

    data = {
        "chat_id": chat_id,
        "text": response.encode("utf8")
    }
    url = BASE_URL + "/sendMessage"
    requests.post(url, data)

    return {"statusCode": 200}

def handle_inline_query(data):
    query_id = data["inline_query"]["id"]
    query = data["inline_query"]["query"]

    # Dummy test data for now
    pic = {
        "type": "photo",
        "id": "my_photo",
        "photo_url": "https://upload.wikimedia.org/wikipedia/commons/2/22/Turkish_Van_Cat.jpg",
        "thumb_url": "https://upload.wikimedia.org/wikipedia/commons/2/22/Turkish_Van_Cat.jpg"
    }

    results = [
        pic,
    ]
    data = {
        'inline_query_id': query_id,
        'results': results
    }
    url = BASE_URL + "/answerInlineQuery"
    res = requests.post(url, json=data)
    return {"statusCode": 200}
