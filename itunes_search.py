from contextlib import nullcontext
from typing import Optional, Tuple, Union

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
    *,
    timeout: Optional[Union[float, Tuple[Optional[float], Optional[float]]]] = None,
):
    with requests.Session() if session is None else nullcontext(session) as session:
        params = {
            "term": term,
            "country": country,
            "media": media,
            "entity": entity,
            "attribute": attribute,
            "limit": limit,
            "lang": lang,
            "explicit": explicit,
        }
        params = {k: v for k, v in params.items() if v is not None}
        response = session.get(BASE_URL, params=params, timeout=timeout)
        response.raise_for_status()
        return response.json()["results"]
