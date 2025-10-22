import requests

BASE_URL = "https://itunes.apple.com/search"


def search(term, country="US", media="all", entity=None, attribute=None, limit=50, lang="en_us", explicit="Yes"):
    params = {k: v for k, v in locals().items() if v is not None}
    response = requests.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()["results"]
