from io import BytesIO

import requests
from celery import Celery

from api import send_message, send_photo
from imdb2_api import get_movie_by_imdb_id
from imdb_api import IMDBAPIClient

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


@app.task
def search_movie(token: str, chat_id: int, rapidapi_key: str, movie_title: str):
    c = IMDBAPIClient(rapidapi_key)
    results = c.search_movies_by_title(movie_title)

    result_message = "Movies found for search:\n"
    result_message += "".join(
        [f"- {result.title} ({result.year}) [{result.imdb_id}]\n" for result in results]
    )

    send_message(token, chat_id, result_message)


DETAILS_MESSAGE = """
{title}
{description}
- "{tagline}"
- Year: {year}
- Rating: {rating} ({vote_count})
"""


def show_movie(token: str, chat_id: int, rapidapi_key: str, imdb_id: str):
    c = IMDBAPIClient(rapidapi_key)
    details = c.get_movie_details(imdb_id)
    image = c.get_movie_images(imdb_id)

    i = image.poster_image
    i.save("poster.jpg", "JPEG")

    # Send photo
    send_photo(token, chat_id, open("poster.jpg", "rb"))

    # Send details
    send_message(
        token,
        chat_id,
        DETAILS_MESSAGE.format(
            title=details.title,
            description=details.description,
            tagline=details.tagline,
            year=details.year,
            rating=details.imdb_rating,
            vote_count=details.vote_count,
        ),
    )


def show_movie2(token: str, chat_id: int, imdb_api_key: str, imdb_id: str):
    # c = IMDBAPIClient(rapidapi_key)
    # details = c.get_movie_details(imdb_id)
    # image = c.get_movie_images(imdb_id)
    movie = get_movie_by_imdb_id(imdb_api_key, imdb_id)

    details = movie["results"]
    banner = details["banner"]

    # i = image.poster_image
    # i.save("poster.jpg", "JPEG")

    banner_response = requests.get(banner)
    banner_response.raise_for_status()

    # Send photo
    send_photo(token, chat_id, banner_response.content)

    # Send details
    send_message(
        token,
        chat_id,
        DETAILS_MESSAGE.format(
            title=details["title"],
            description=details["description"],
            tagline="No",
            year=details["year"],
            rating=details["rating"],
            vote_count=100,
        ),
    )
