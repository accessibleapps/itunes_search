import json
import urllib

__version__ = 0.2
__author__ = 'Christopher Toth'
__doc__ = """Simple wrapper over the iTunes search API"""

BASE_URL = 'https://itunes.apple.com/search'

def search(term, country='US', media='all', entity=None, attribute=None, limit=50, lang='en_us', explicit='Yes'):
 params = {k:v for k, v in locals().iteritems() if v is not None}
 url = '%s?%s' % (BASE_URL, urllib.urlencode(params))
 response = urllib.urlopen(url).read()
 return json.loads(response)['results']


