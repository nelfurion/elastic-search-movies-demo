from requests import request

class ElasticSearchService:
    def __init__(self, endpoint):
        self.PUSH_FORMAT = '{endpoint}/{index}/{type}/{id}'
        self.endpoint = endpoint
        self.search_endpoint = self.endpoint + '/_search'

    def push(self, index, type, id, object):
        push_endpoint = self.PUSH_FORMAT.format(
            endpoint=self.endpoint,
            index=index,
            type=type,
            id=id
        )

        return self._send_request(
            method = 'post',
            url = push_endpoint,
            data = object
        )

    def search(self, options):
        return self._send_request(
            method = 'get',
            url = self.endpoint,
            data = options
        )

    def full_text_search(self, text = "", size = 10 , skip = 0):
        print('FULL TEXT SEARCH: ', text)
        query = {
            "from": skip,
            "size": size,
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "_index": "movies"
                            }
                        }, {
                            "match": {
                                "_type": "movie"
                            }
                        }, {
                            "match": {
                                "_all": text
                            }
                        }
                    ]
                }
            }
        }

        return self._send_request(
            method = 'get',
            url = self.search_endpoint,
            data = query)

    def _send_request(self, method, url, data):
        return request(method=method, url=url, json=data).json()

    def get_movies(self, size = 10, skip = 0):
        query = {
            "from": skip,
            "size": size,
            "query": {
                "bool": {
                    "should": [
                        {
                            "match": {
                                "_index": "movies"
                            }
                        }, {
                            "match": {
                                "_type": "movie"
                            }
                        }
                    ]
                }
            }
        }

        return self._send_request(
            method='get',
            url=self.search_endpoint,
            data=query
        )