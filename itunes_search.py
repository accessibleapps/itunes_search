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
    """Search Apple's iTunes catalog and return its list of result dictionaries.

    term is ordinary search text; Requests handles URL encoding. country selects
    the store, while media, entity and attribute select what to search. limit
    requests a result count, lang selects the result language, and explicit
    controls inclusion of explicit content. Defaults are shown in the signature;
    query values of None are omitted. Query values are not validated locally.

    timeout is passed to Requests unchanged: seconds, a (connect, read) tuple, or
    None to wait indefinitely. It is not sent as a query parameter.

    A supplied requests.Session remains open and is owned by the caller; a session
    created by search is closed before it returns or raises.
    Transport, HTTP and JSON decoding errors propagate. A missing results key
    raises KeyError. An empty results list is returned unchanged.
    """
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
