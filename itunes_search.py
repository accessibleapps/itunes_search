import requests

__version__ = 0.1
__author__ = 'Christopher Toth'
__doc__ = """Simple wrapper over the iTunes search API, using Requests"""

BASE_URL = 'https://itunes.apple.com/search'

def search(term, country='US', media='all', entity=None, attribute=None, limit=50, lang='en_us', explicit='Yes'):
 params = {k:v for k, v in locals().iteritems() if v is not None}
 session = requests.session()
 session.adapters['https://'].max_retries = 4
 response = session.get(BASE_URL, params=params)
 response.raise_for_status()
 return response.json()['results']
