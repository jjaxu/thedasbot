import json
import os
import sys
import requests

sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "./vendored"))

from dynamodb import setUser, getUser, clearUser
from trivia import Trivia
from boterror import BotError

TOKEN = os.environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

def trigger(event, context):
    msg_key = "message"
    data = json.loads(event["body"])
    if "inline_query" in data:
        return handle_inline_query(data)

    if "callback_query" in data:
        return handle_callback_query(data)

    # don't care about edited messages or event does not contain relevant text data
    if "edited_message" in data or "text" not in data[msg_key]:
        return {"statusCode": 200}

    message = str(data[msg_key]["text"])
    chat_id = data[msg_key]["chat"]["id"]
    user_id = data[msg_key]["from"]["id"]
    parse_mode = None
    other_params = None

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
    elif message.startswith("/clear"):
        response = "Entry cleared!" if clearUser(user_id) else "Nothing to clear!"
    elif message.startswith("/get"):
        response = getUser(user_id) or "Nothing to get! Use /store to set"
    elif message.startswith("/store"):
        index = message.strip().find(" ")
        if index < 0:
            response = "Nothing to store!"
        else:
            result = setUser(user_id, message[index + 1:])
            response = "You stored \"{}\". Use /get to fetch it".format(result) if result else "Failed to store!"
    elif message.startswith("/trivia"):
        parse_mode = "Markdown"
        args = message.strip().split(" ")
        category, difficulty = None, None

        if len(args) > 1:
            category = args[1]
            if len(args) > 2:
                difficulty = args[2]

        try:
            trivia = Trivia(category, difficulty)
        except BotError as err:
            response = str(err)
        else:
            response = trivia.formatted_response()
            correct_ans = chr(trivia.correct_answer_index() + 65)
            buttons = [ {"text": chr(i+65), "callback_data": "{}{}".format(chr(i+65), correct_ans) } for i in range(4) ]

            other_params = {
                "reply_markup": {
                    "inline_keyboard":
                    [
                        [
                            buttons[0],
                            buttons[1]
                        ],
                        [
                            buttons[2],
                            buttons[3]
                        ]
                    ],
                }
            }
    else:
        response = "Sorry, I don't understand. Try /help"

    data = {
        "chat_id": chat_id,
        "text": response
    }
    
    if parse_mode:
        data["parse_mode"] = parse_mode
    if other_params:
        data.update(other_params)

    url = BASE_URL + "/sendMessage"
    res = requests.post(url, json=data)
    if not res.ok:
        print(res.status_code)
        print(res.text)

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

def handle_callback_query(data):
    query = data["callback_query"]
    chat_id = query["message"]["chat"]["id"]
    message_id = query["message"]["message_id"]
    old_text = query["message"]["text"]
    callback_data = query["data"]
    if callback_data == "NULL":
        return {"statusCode": 200}

    try:
        if callback_data[0] == callback_data[1]:
            res_text = "*{}* is correct!".format(callback_data[0])
        else:
            res_text = "*{}* is incorrect! The correct answer is *{}*".format(callback_data[0], callback_data[1])
    except:
        print("something went wrong, returning...")
        return {"statusCode": 200}

    url2 = BASE_URL + "/editMessageText"
    resp2 = {
        "chat_id": chat_id,
        "message_id": message_id,
        "text": "{}\n\n{}".format(old_text, res_text),
        "reply_markup": {
            "inline_keyboard": [],
        },
        "parse_mode": "Markdown"
    }

    res = requests.post(url2, json=resp2)
    if not res.ok:
        print(res.text)

    return {"statusCode": 200}
