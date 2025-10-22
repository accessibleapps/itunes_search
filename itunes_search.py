from typing import Optional

import requests

BASE_URL = "https://itunes.apple.com/search"


def search(
    term: str,
    country: str = "US",
    media: str = "all",
    entity: Optional[str] = None,
    attribute: Optional[str] = None,
    limit: int = 50,
    lang: str = "en_us",
    explicit: str = "Yes",
    session: Optional[requests.Session] = None,
):
    if session is None:
        session = requests.Session()
    params = {k: v for k, v in locals().items() if v is not None and k != "session"}
    response = session.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()["results"]
