import json
from io import BytesIO
from pprint import pprint

from api import (
    Message,
    get_file,
    get_updates,
    listen_updates,
    poll_updates,
    send_message,
    send_photo,
)
from imdb2_api import search_movies
from speech_api import convert_voice_to_text
from tasks import reply, search_movie, show_movie, show_movie2


def start_reply_message():
    pass


if __name__ == "__main__":
    with open("appsettings.json", encoding="utf-8") as appsettings:
        appsettings_json = json.load(appsettings)
        token = appsettings_json["token"]
        rapidapi_key = appsettings_json["x-rapidapi-key"]
        speech_key = appsettings_json["speech-key"]
        imdb_key = appsettings_json["imdb-data-key"]

    # listen_updates(token)
    for updates in poll_updates(token):
        result = updates["result"]
        for r in result:
            message = r["message"]

            if "voice" in message:
                voice = message["voice"]
                file_id = voice["file_id"]
                file_bytes = get_file(token, file_id)
                response = convert_voice_to_text(speech_key, file_bytes)
                text = response["data"]["text"].capitalize()
                text = "Django"
                send_message(token, message["chat"]["id"], f"You said {text}?")

                result = search_movies(imdb_key, text)
                top_movie_imdb_id = result["results"][0]["imdb_id"]

                show_movie2(token, message["chat"]["id"], imdb_key, top_movie_imdb_id)
                continue

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
