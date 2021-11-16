import requests


def search_movies(api_key: str, title: str) -> dict:
    url = f"https://data-imdb1.p.rapidapi.com/movie/imdb_id/byTitle/{title}/"
    headers = {
        "x-rapidapi-host": "data-imdb1.p.rapidapi.com",
        "x-rapidapi-key": api_key,
    }
    response = requests.request("GET", url, headers=headers)
    response.raise_for_status()
    return response.json()


def get_movie_by_imdb_id(api_key: str, imdb_id: str) -> dict:
    url = f"https://data-imdb1.p.rapidapi.com/movie/id/{imdb_id}/"

    headers = {
        "x-rapidapi-host": "data-imdb1.p.rapidapi.com",
        "x-rapidapi-key": api_key,
    }

    response = requests.request("GET", url, headers=headers)

    response.raise_for_status()
    return response.json()
