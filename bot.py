import json
from pprint import pprint

import requests
from flask import Flask, request, Response

API_URL = "https://api.telegram.org/bot{token}/{method}"


def get_me(token: str):
    r = requests.get(API_URL.format(token=token, method="getMe"))
    r.raise_for_status()
    return r.json()


def get_updates(token: str, last_update_id: int = None, timeout: int = None):
    """
    Get updates for :token: bot, filter updates (only new) based on :last_update:
    and wait for response for :timeout: seconds.
    """
    if last_update_id is None:
        r = requests.get(API_URL.format(token=token, method="getUpdates"))
        r.raise_for_status()
        return r.json()

    r = requests.get(
        API_URL.format(token=token, method="getUpdates"),
        params={"offset": last_update_id + 1, "timeout": timeout or 60},
    )
    r.raise_for_status()
    return r.json()


def poll_updates(token: str):
    """
    Real-time updates notification using infinite 60s long-polling.
    """
    r = get_updates(token)
    pprint(r)
    while True:
        last_update_id = r["result"][-1]["update_id"]
        r = get_updates(token, last_update_id=last_update_id)
        pprint(r)


def listen_updates(token: str):
    """
    Set and listen webhook
    """
    app = Flask("epam-bot")

    @app.route("/webhook/", methods=["POST"])
    def respond():
        pprint(request.json)
        return Response(status=200)

    app.run()


if __name__ == "__main__":
    with open("appsettings.json") as appsettings:
        appsettings_json = json.load(appsettings)
        token = appsettings_json["token"]

    # pprint(get_me(token))
    # try:
    #     print("Polling started")
    #     poll_updates(token)
    # finally:
    #     print("Polling ended")
    listen_updates(token)
