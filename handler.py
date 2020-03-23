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

    # Is the message edited?
    msg_key = "edited_message" if "edited_message" in data else "message"

    # event does not contain relevant text data
    if "text" not in data[msg_key]:
        return {"statusCode": 200}

    message = str(data[msg_key]["text"])
    chat_id = data[msg_key]["chat"]["id"]
    parse_mode = None

    if message.startswith("/start"):
        if data[msg_key]["chat"]["type"] == "private":
            response = "Hello {}! Welcome to the DAS bot!".format(data[msg_key]["chat"]["first_name"])
        elif data[msg_key]["chat"]["type"] == "group":
            response = "Hello {}! I am the DAS Bot, {} has summoned me here!".format(
                data[msg_key]["chat"]["title"],
                data[msg_key]["from"]["first_name"]
            )
        else:
            response = "Hello"
    elif message.startswith("/help"):
        response = "You have invoked the help command!"
    elif message.startswith("/debug"):
        response = str(data)
    elif message.startswith("/joke"):
        r = requests.get("https://icanhazdadjoke.com/", headers={"Accept": "text/plain"})
        response = r.content.decode() if r.ok else "Oops! Can't fetch joke right now."
    elif message.startswith("/fact"):
        r = requests.get("https://www.mentalfloss.com/api/facts")
        response = str(r.json()[0]['headline']) if r.ok else "Oops! Can't fetch fact right now."
        parse_mode = "HTML"
    else:
        response = "Sorry, I don't understand. Try /help"

    data = {
        "chat_id": chat_id,
        "text": response.encode("utf8")
    }
    if parse_mode:
        data["parse_mode"] = parse_mode

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
