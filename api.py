from datetime import datetime
from pprint import pprint
from time import sleep
from typing import Generator, Union

import requests
from flask import Flask, Response, request

API_URL = "https://api.telegram.org/bot{token}/{method}"


class Chat:
    def __init__(self, **kwargs: Union[str, int]):
        self.first_name: Union[str, int, None] = kwargs.get("first_name")
        self.id: Union[str, int, None] = kwargs.get("id")
        self.type: Union[str, int, None] = kwargs.get("type")
        self.username: Union[str, int, None] = kwargs.get("username")


class User:
    def __init__(self, **kwargs: Union[str, int]):
        for k, v in kwargs.items():
            setattr(self, k, v)


class Message:
    def __init__(self, **kwargs):
        self.chat: Chat = kwargs["chat"]
        if self.chat:
            self.chat = Chat(**self.chat)
        self.date: datetime = kwargs.get("date")
        if self.date:
            self.date = datetime.fromtimestamp(self.date)
        self.from_user: User = kwargs.get("from")
        if self.chat:
            self.chat = User(**self.from_user)
        self.message_id: int = kwargs.get("message_id")
        self.text: str = kwargs.get("text")


def get_me(token: str) -> dict:
    """
    Return information about bot.
    """
    r = requests.get(API_URL.format(token=token, method="getMe"))
    r.raise_for_status()
    return r.json()


def send_message(token: str, chat_id: int, text: str):
    r = requests.post(
        API_URL.format(token=token, method="sendMessage"),
        data={"chat_id": chat_id, "text": text},
    )
    r.raise_for_status()
    return r.json()


def send_photo(token: str, chat_id: int, i_bytes: bytes):
    files = {"photo": i_bytes}
    data = {"chat_id": chat_id}
    r = requests.post(
        API_URL.format(token=token, method="sendPhoto"), files=files, data=data
    )
    r.raise_for_status()

    return r.json()


def get_updates(token: str, last_update_id: int = None, timeout: int = None) -> dict:
    """
    Get updates for :token: bot, filter updates based on :last_update:
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


def poll_updates(token: str) -> Response:
    """
    Update listener using long-polling.

    Real-time updates notification using infinite 60s long-polling.
    """
    r = get_updates(token)
    yield r
    while True:
        last_update_id = r["result"][-1]["update_id"]
        r = get_updates(token, last_update_id=last_update_id)
        yield r


def listen_updates(token: str):
    """
    Update listener using long-polling.

    Set and listen webhook
    """
    app = Flask("epam-bot")

    @app.route(f"/{token}", methods=["POST"])
    def respond():
        print(f"Webhook was called, 100% by Telegram!!, {request}")
        sleep(10)
        return Response("Hello, World!", status=200)

    app.run(port=8000)
