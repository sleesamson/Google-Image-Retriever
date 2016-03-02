import requests
import json
#from PIL import Image

def response_json(res):
    try:
        return res.json()
    except TypeError:
        return res.json
    except json.JSONDecodeError:
        return ''

class ImageRetriever(object):
    #TODO Support atom structure
    '''
        Create a Google API Key here: https://console.developers.google.com
        Create a custom search engine here: https://cse.google.com/cse/
            and enable image search to use this wrapper.
    '''

    google_api = "https://www.googleapis.com/customsearch/v1"

    ALLOWED_TYPES = (
        'jpg',
        'png',
        'gif',
        'bmp',
    )

    ALLOWED_DOMINENT_COLORS = (
        'black',
        'blue',
        'brown',
        'gray',
        'green',
        'orange',
        'pink',
        'purple',
        'red',
        'teal',
        'white',
        'yellow',
    )

    ALLOWED_SIZES = (
        "huge",
        "icon",
        "large",
        "medium",
        "small",
        "xlarge",
        "xxlarge",
    )

    def __init__(self, api_key, cx=None, cref=None):
        if cx is None and cref is None:
            raise ValueError(
                '''
                cx or a cref must be specified.
                Refer to https://developers.google.com/custom-search/json-api/v1/reference/cse/list
                '''
            )

        self.params = {
            'key': api_key,
            'cx': cx,
            'cref': cref,
            'alt': 'json',
            'searchType': 'image'
        }

    def _GET(self):
        self.resp = requests.get(self.google_api, params=self.params)

        print self.resp.url
        if self.resp.status_code != 200:
            raise Exception(error)

        try:
            self.data = response_json(self.resp)
        except ValueError as ex:
            raise

        return self.data

    def query(self, query, fileType=None, size=None, dom_color=None):
        self.params.update({
                'q': query,
        })

        if fileType:
            if fileType.lower() not in self.ALLOWED_TYPES:
                raise TypeError("Must specify jpg, png, gif, bmp only")

            self.params['&fileType=%s'] = fileType

        if size:
            if size.lower() not in self.ALLOWED_SIZES:
                raise TypeError("Size must be in %s" % self.ALLOWED_SIZES)

            self.params['imgSize'] = size

        if dom_color:
            if dom_color.lower() not in self.ALLOWED_DOMINENT_COLORS:
                raise TypeError("Color must be in %s" % self.ALLOWED_DOMINENT_COLORS)

            self.params['imgDominantColor'] = dom_color

        self.data = self._GET()

        return self.data

    def filter_by_resolution(self, width, height, find_more=False):
        '''API does not support querying by resolution so lets to some grunt work'''
        '''Just returns a list of image links that match the resolution specfied'''

        good_results = []

        for item in self.data.get('items', []):
            if item['image']['width'] == int(width) and item['image']['height'] == int(height):
                good_results.append(item['link'])

        #recursive call
        #will search through next indexes until we find good match(es)
        if not good_results or find_more:
            next_index = self.data['queries']['nextPage'][0]['startIndex']
            self.params.update({'start': next_index })
            self.data = self._GET()

            self.filter_by_resolution(width, height)

        return good_results

