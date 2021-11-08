from celery import Celery

from api import send_message

# celery -A tasks worker --log-level INFO
app = Celery(
    "tasks", backend="redis://localhost:6379/0", broker="redis://localhost:6379/0"
)


@app.task
def hello():
    return "Hello"


@app.task
def reply(token: str, chat_id: int, text: str):
    return send_message(token, chat_id, text)
