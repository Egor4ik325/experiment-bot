import json

import requests

BASE_URL = "https://speech-recognition-english1.p.rapidapi.com/api/asr"


def convert_voice_to_text(rapidapi_key, audio_bytes: bytes):

    headers = {
        "x-rapidapi-host": "speech-recognition-english1.p.rapidapi.com",
        "x-rapidapi-key": rapidapi_key,
    }

    files = {"sound": audio_bytes}
    r = requests.post(BASE_URL, files=files, headers=headers)
    r.raise_for_status()

    return r.json()


if __name__ == "__main__":
    with open("appsettings.json") as appsettings:
        settings = json.load(appsettings)
        speech_key = settings["speech-key"]

    response = convert_voice_to_text(speech_key, open("python_is_awesome.m4a", "rb"))

    print(response["data"]["text"])
