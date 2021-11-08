import json
from pprint import pprint

from api import Message, get_updates, listen_updates, poll_updates, send_message
from tasks import reply


def start_reply_message():
    pass


if __name__ == "__main__":
    with open("appsettings.json", encoding="utf-8") as appsettings:
        appsettings_json = json.load(appsettings)
        token = appsettings_json["token"]

    # listen_updates(token)
    for updates in poll_updates(token):
        result = updates["result"]
        for r in result:
            message = r["message"]
            update_id = r["update_id"]
            m = Message(**message)
            pprint(m.text)

            # Push task to the queue
            result = reply.delay(token, m.chat.id, m.text)
