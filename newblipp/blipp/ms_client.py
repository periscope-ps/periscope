import json
import requests

import settings
logger = settings.get_logger('ms_client')


from pprint import pprint

class MSInstance:
    def __init__(self, ms_url):
        self.ms_url=ms_url
        self.def_headers={'content-type':
                          'application/perfsonar+json ;profile=' + settings.SCHEMAS['metadata'],
                          'accept':"*/*"}
        self.post_events_cache = []

    def _def_headers(self, ctype):
        def_headers={'content-type':
                          'application/perfsonar+json profile=' + settings.SCHEMAS[ctype],
                          'accept':"*/*"}
        return def_headers
    
    def post_events(self, md_url, size, ttl):
        post = dict({"metadata_URL": md_url,
                     "collection_size": size,
                     "ttl": ttl
                     })
        post_json = json.dumps(post, indent=2)
        post_url = self.ms_url + "/events"
        headers = self._def_headers("datum")
        logger.info("post_events", url=post_url)
        logger.debug("post_events", headers=str(headers), data=post_json)

        try:
            r = requests.post(post_url, data=post_json, headers=headers)
        except Exception as e:
            logger.exc('post_events', e)
            self.post_events_cache.append(post)
            return None
        h = self._handle_response(r)
        return r.status_code

    def get_events(self):
        get_url = self.ms_url + "/events"
        headers = {"accept": "application/perfsonar+json;"}
        logger.info("get_events", url=get_url)
        logger.debug("get_events", headers=str(headers))
        r = requests.get(get_url, headers=headers)
        h = self._handle_response(r)
        return r.status_code

    def post_data(self, post):
        # takes a list/dict properly formatted as shown on
        # https://github.com/GENI-GEMINI/GEMINI/wiki/MS-REST-API
        post_json = json.dumps(post, indent=2)
        post_url = self.ms_url + "/data"
        headers = self._def_headers("data")
        logger.info("post_data", url=post_url)
        logger.trace("post_data", headers=headers, data=post_json)
        try:
            r = requests.post(post_url, data=post_json, headers=headers)
        except requests.ConnectionError:
            logger.error('post_data', msg="ConnectionError, could not connect to MS", url=post_url)
            return
        except Exception as e:
            logger.exc('post_data', e)
            return
        h = self._handle_response(r)
        if h==400:
            self._retry_post_events()
        return r.status_code
    
    def _retry_post_events(self):
        logger.info("_retry_post_events")
        for entry in self.post_events_cache:
            self.post_events(entry["metadata_URL"], entry["collection_size"], entry["ttl"])

    def _handle_response(self, r):
        if r.status_code>=200 and r.status_code<300: # query OK, ACCEPTED, generally good
            logger.info("handle_response", resp=r.status_code)
            try:
                resp = json.loads(r.text)
                return resp
            except:
                return r.status_code
        else:
            logger.error("handle_response", resp=r.status_code, msg=r.text)
            return r.status_code

        # elif r.status_code==401: # unauthorized
        #     ### LOG unauthorized
        #     return r.status_code
        # elif r.status_code==500: # internal server error
        #     ### LOG internal server error
        #     return r.status_code
        # elif r.status_code==304: # not modified
        #     # if we have a cached version use it
        #     # not implemented yet
        #     ### LOG using cached version
        #     return 304
        # elif r.status_code==404: # not found
        #     ### LOG not found
        #     return None
        # elif r.status_code==409: # metadata already exists
        #     return 409
        # elif r.status_code==400: # bad request
        #     ### LOG invalid metadata
        #     return 400
        # else:
        #     ### LOG wtf
        #     return -1

    
