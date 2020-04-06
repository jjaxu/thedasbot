from os import environ

# Bot token & API
TOKEN = environ['TELEGRAM_TOKEN']
BASE_URL = "https://api.telegram.org/bot{}".format(TOKEN)

# API dict constants
INLINE_QUERY_KEY = "inline_query"
CALLBACK_QUERY_KEY = "callback_query"
EDITED_MESSAGE_KEY = "edited_message"
MESSAGE_KEY = "message"
ID_KEY = "id"
QUERY_KEY = "query"
TEXT_KEY = "text"
CHAT_KEY = "chat"
FROM_KEY = "from"
TYPE_KEY = "type"
TITLE_KEY = "title"
FIRST_NAME_KEY = "first_name"
LAST_NAME_KEY = "last_name"

GROUP_STR = "group"
PRIVATE_STR = "private"
