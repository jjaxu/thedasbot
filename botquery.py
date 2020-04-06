from json import loads
from boterror import BotError
from constants import *

class BotQuery(object):

    @classmethod
    def parse_event(cls, event_json, load_json=True):
        try:
            data = loads(event_json) if load_json else event_json
            empty = dict()
            result = cls()
            
            if INLINE_QUERY_KEY in data:
                result.is_inline_query = True
                result.inline_query_id = data[INLINE_QUERY_KEY][ID_KEY]
                result.inline_query_text = data[INLINE_QUERY_KEY][QUERY_KEY]
        
            if CALLBACK_QUERY_KEY in data:
                result.has_callback_query = True
                result.callback_query = cls.parse_event(data[CALLBACK_QUERY_KEY], load_json=False)

            msg_key = None
            if MESSAGE_KEY in data:
                msg_key = MESSAGE_KEY
            elif EDITED_MESSAGE_KEY in data:
                msg_key = EDITED_MESSAGE_KEY
                result.is_edited = True
                
            result.message = data.get(msg_key, empty).get(TEXT_KEY)
            result.chat_id = data.get(msg_key, empty).get(CHAT_KEY, empty).get(ID_KEY)
            result.chat_title = data.get(msg_key, empty).get(CHAT_KEY, empty).get(TITLE_KEY)
            result.from_id = data.get(msg_key, empty).get(FROM_KEY, empty).get(ID_KEY)
            result.user_first_name = data.get(msg_key, empty).get(FROM_KEY, empty).get(FIRST_NAME_KEY)
            result.user_last_name = data.get(msg_key, empty).get(FROM_KEY, empty).get(LAST_NAME_KEY)

            result.is_private = data.get(msg_key, empty).get(CHAT_KEY, empty).get(TYPE_KEY) == PRIVATE_STR
            result.is_group = data.get(msg_key, empty).get(CHAT_KEY, empty).get(TYPE_KEY) == GROUP_STR
            result.is_private = data.get(msg_key, empty).get(CHAT_KEY, empty).get(TYPE_KEY) == PRIVATE_STR

            if not (
                result.message or
                result.is_inline_query or 
                result.has_callback_query
            ): raise ValueError("Invalid or unsupported query event while parsing")
        except Exception as err:
            raise BotError("BotQuery parsing failed:\n\t{}".format(str(err)))
        else:
            return result

    def __init__(self):
        super().__init__()
        self.is_private = False
        self.is_group = False
        self.is_edited = False

        # Inline query
        self.is_inline_query = False
        self.inline_query_id = None
        self.inline_query_text = None

        # Callback query
        self.has_callback_query = False
        self.callback_query = None

        # Message content
        self.message = None
        self.chat_id = None
        self.from_id = None
        self.user_first_name = None
        self.user_last_name = None
        self.chat_title = None
