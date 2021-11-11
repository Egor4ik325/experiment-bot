import json
from io import BytesIO
from pprint import pprint

from api import (
    Message,
    get_updates,
    listen_updates,
    poll_updates,
    send_message,
    send_photo,
)
from tasks import reply, search_movie, show_movie


def start_reply_message():
    pass


if __name__ == "__main__":
    with open("appsettings.json", encoding="utf-8") as appsettings:
        appsettings_json = json.load(appsettings)
        token = appsettings_json["token"]
        rapidapi_key = appsettings_json["x-rapidapi-key"]

    # listen_updates(token)
    for updates in poll_updates(token):
        result = updates["result"]
        for r in result:
            message = r["message"]
            update_id = r["update_id"]
            m = Message(**message)
            pprint(m.text)

            # Process command
            if m.text.startswith("/"):
                # Movie search
                if m.text.startswith("/search"):
                    command, movie_title = m.text.split(" ", 1)

                    result = search_movie.delay(
                        token, m.chat.id, rapidapi_key, movie_title
                    )
                    continue
                if m.text.startswith("/show"):
                    command, imdb_id = m.text.split(" ", 1)
                    result = show_movie(token, m.chat.id, rapidapi_key, imdb_id)
                    continue

            # Push task to the queue
            result = reply.delay(token, m.chat.id, m.text)
