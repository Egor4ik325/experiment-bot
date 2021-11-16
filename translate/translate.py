"""
Translate using Yandex.Translate scrapter.
"""
from typing import Tuple
from urllib.parse import parse_qs, urlparse

from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait

TRANS_URL = "https://translate.yandex.ru/"



def translate(src: str) -> Tuple[str, Tuple[str, str]]:
    """
    Translate given source text to the RU/EN.

    Return:
        translation result text
        source and target languages tuple
    """
    # Get the page source with the tranlsation
    with webdriver.Firefox() as driver:
        driver.get(f"{TRANS_URL}?text={src}")
        WebDriverWait(driver, 1)
        page_source = driver.page_source
        page_url = driver.current_url

    # Parse the source to get translation result
    soup = BeautifulSoup(page_source, "html.parser")
    translation = soup.find(id="translation")
    text = translation.text

    # Parse URL to get translation languages
    page_url_query = urlparse(page_url).query
    lang = parse_qs(page_url_query)["lang"][0]
    source, target = lang.split("-", 1)

    return (src, text), (source, target)


if __name__ == "__main__":
    print(translate("Hello"))
