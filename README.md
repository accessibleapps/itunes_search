# itunes_search

A small Python wrapper for the [Apple iTunes Search API](https://performance-partners.apple.com/search-api).
Requires Python 3.8 or newer and Requests.

## Installation

Install from this repository:

```sh
git clone https://github.com/accessibleapps/itunes_search.git
cd itunes_search
python -m pip install .
```

## Search

```python
from itunes_search import search

podcasts = search("Planet Money", media="podcast", limit=5)
for podcast in podcasts:
    print(podcast.get("collectionName"), podcast.get("feedUrl"))
```

`search()` returns the response's `results` list, containing Apple's result
dictionaries. An empty search result is an empty list. The full response envelope,
including `resultCount`, is not returned. Available fields depend on the media
and entity selected; use Apple's documentation for their meanings.

| Argument | Default | Meaning |
| --- | --- | --- |
| `term` | Required | Search text; pass ordinary text, as Requests handles URL encoding. |
| `country` | `"US"` | Two-letter store country code. |
| `media` | `"all"` | Media type, such as `"podcast"`, `"music"`, or `"ebook"`. |
| `entity` | `None` | Result entity appropriate to the media type. |
| `attribute` | `None` | Search attribute appropriate to the media type. |
| `limit` | `50` | Requested result count; Apple documents a range of 1–200. |
| `lang` | `"en_us"` | Result language: `"en_us"` or `"ja_jp"`. |
| `explicit` | `"Yes"` | Include explicit content with `"Yes"`; exclude it with `"No"`. |
| `session` | `None` | Optional caller-owned `requests.Session`. |

Query arguments whose values are `None` are omitted. The wrapper forwards query
values to Apple without validating them; consult the API documentation for valid
media, entity, and attribute combinations.

## Reuse a session

Supply a session to reuse connections across searches. You own its lifetime;
`search()` leaves it open. A Requests context manager closes it when finished:

```python
import requests
from itunes_search import search

with requests.Session() as session:
    podcasts = search("Planet Money", media="podcast", session=session)
    music = search("Jack Johnson", media="music", session=session)
```

## Errors

Transport errors and HTTP errors from Requests propagate to the caller. The
function checks HTTP status before decoding JSON. JSON decoding errors also
propagate, and a response without a `results` key raises `KeyError`. Errors are
not converted to an empty result list.
