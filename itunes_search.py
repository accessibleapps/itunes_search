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
    """Search Apple's iTunes catalog and return its list of result dictionaries.

    term is ordinary search text; Requests handles URL encoding. country selects
    the store, while media, entity and attribute select what to search. limit
    requests a result count, lang selects the result language, and explicit
    controls inclusion of explicit content. Defaults are shown in the signature;
    query values of None are omitted. Query values are not validated locally.

    A supplied requests.Session remains open and is owned by the caller.
    Transport, HTTP and JSON decoding errors propagate. A missing results key
    raises KeyError. An empty results list is returned unchanged.
    """
    if session is None:
        session = requests.Session()
    params = {k: v for k, v in locals().items() if v is not None and k != "session"}
    response = session.get(BASE_URL, params=params)
    response.raise_for_status()
    return response.json()["results"]
