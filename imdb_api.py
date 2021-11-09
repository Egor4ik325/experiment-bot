"""
IMDB via RapidAPI Python client library/module/wrapper/package.

API client library:

- Covert JSON to language specific types (classes)
- Type annotate data
- Handle networking/request error
- Handle specific HTTP results
"""
from datetime import datetime
from typing import List

import requests

API_HOST = "movies-tvshows-data-imdb.p.rapidapi.com"
API_BASE = f"https://{API_HOST}/"


class IMBDAPIError(Exception):
    """Raised when IMDB API error occur.  Handle this exception on your own."""


class MovieSearchResult:
    """Parsed response of movie search API action."""

    def __init__(self, title: str, year: str, imdb_id: str):
        self.title = title
        self.year = int(year)
        self.imdb_id = imdb_id

    def __str__(self):
        return f"{self.title} ({self.year})"


class MovieDetailsResult(MovieSearchResult):
    """Parsed response of movie details API action."""

    def __init__(
        self,
        title: str,
        year: str,
        imdb_id: str,
        description: str,
        tagline: str,
        release_date: str,
        imdb_rating: str,
        vote_count: str,
        popularity: str,
        rated: str,
        **kwargs,
    ):
        super().__init__(title, year, imdb_id)
        self.description = description
        self.tagline = tagline
        self.release_date = datetime.strptime(release_date, r"%Y-%m-%d").date()
        self.imdb_rating = float(imdb_rating)
        self.vote_count = float(vote_count)
        self.popularity = float(popularity)
        self.rated = rated


class IMDBAPIClient:
    """
    Python API client for RapidAPI IMDB API.

    Includes:

    - search movie
    - movie details
    - movie images
    """

    def __init__(self, rapidapi_key: str):
        self.s = requests.Session()
        self.s.headers = {
            "x-rapidapi-host": API_HOST,
            "x-rapidapi-key": rapidapi_key,
        }

    def search_movies_by_title(self, title: str) -> List[MovieSearchResult]:
        """
        Search for movies by title.

        Return <= 20 search results.
        """
        params = {"type": "get-movies-by-title", "title": title}
        r = self.s.get(API_BASE, params=params)

        # Raise exception for error response
        r.raise_for_status()

        data = r.json()

        if data["status"] != "OK":
            raise IMBDAPIError(data["status_message"])

        if data["search_results"] == 0:
            return []

        return [
            MovieSearchResult(**movie_result) for movie_result in data["movie_results"]
        ]

    def get_movie_details(self, imdb_id: str):
        """
        Get movie detailed information about the movie.

        Return MovieDetailsResult
        """
        r = self.s.get(API_BASE, params={"type": "get-movie-details", "imdb": imdb_id})
        r.raise_for_status()

        data = r.json()

        if data["status"] != "OK":
            raise IMBDAPIError(data["status_message"])

        return MovieDetailsResult(**data)

    def get_movie_images(self, imdb_id: str):
        """
        Get movie images as URLs.
        """


if __name__ == "__main__":
    import json

    with open("appsettings.json", encoding="utf-8") as settings:
        settings_json = json.load(settings)

    c = IMDBAPIClient(settings_json["x-rapidapi-key"])
    results = c.search_movies_by_title("God")

    # Print search results
    # for r in results:
    #     print(r)

    movie = results[0]
    details = c.get_movie_details(movie.imdb_id)

    print("Movie:", details)
    print("Descpription:", details.description)
    print("Rating:", details.imdb_rating)
