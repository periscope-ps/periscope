import requests
import json
import uuid
import time

import settings
from utils import *
from pprint import pprint

logger = settings.get_logger('unis_client')

class UNISInstance:
    '''This class will either contact a UNIS instance or make up
    semi-appropriate responses
    '''

    ### still need to implement metadata storage and caching
    ### remember to think about multiple UNISInstance objs sharing one cache
    
    def __init__(self, unis_url=None, md_cache="/tmp/blippmd",
                 unis_consts="unis_consts"):
        self.unis_url=unis_url
        self.md_cache=md_cache
        self.consts=try__import__(unis_consts)

    def _def_headers(self, ctype):
        def_headers={'content-type':
                          'application/perfsonar+json profile=' + settings.SCHEMAS[ctype],
                          'accept':settings.MIME['PSJSON']}
        return def_headers
    
    def post_metadata(self, post_dict, headers=None):
        '''Takes in a dict which will be converted to json
        and posted to UNIS with UNISs response returned, or
        just returned with timestamp, id and selfRef added
        if no UNIS instance is specified. If 409 (conflict)
        is returned, UNIS is queried for the already existing
        metadata'''
        if headers==None:
            headers=self._def_headers('metadata')
        if not self.unis_url:
            self._add_unis_fields(post_dict)
            return post_dict
            
        post_json = json.dumps(post_dict, indent=2)
        url = self.unis_url + '/metadata'
        
        logger.info('post_metadata')
        logger.debug('post_metadata', post=post_json)
        try:
            r = requests.post(url, data=post_json, headers=headers)
        except Exception as e:
            logger.exc('post_metadata', e)
            return None

        h = self._handle_response(r)
        if h==409:
            resp = self.get_metadata(post_dict['subject'], post_dict['event_type'], post_dict['parameters'])
            if isinstance(resp, list) and len(resp)>1:
                logger.warn("post_metadata.conflict.multiple_responses", responses=str(resp))
                latest_ts = 0
                pos = -1
                for md in resp:
                    if md["ts"]>latest_ts:
                        pos=resp.index(md)
                return resp[pos] # return metadata with latest timestamp
            else:
                return resp
        else:
            return h
        
    def _add_unis_fields(self, post_dict):
        id_uuid = str(uuid.uuid4())
        if not "ts" in post_dict:
            post_dict.update({"ts":time.time()})
        if not "id" in post_dict:
            post_dict.update({"id":id_uuid})
        if not "selfRef" in post_dict:
            post_dict.update({"selfRef":"DEADBEEF"+id_uuid})


    def post_port(self, post_dict, headers=None):
        ### This should probably update the node to have these ports as well
        if "$schema" not in post_dict:
            post_dict.update({"$schema":self.consts.SCHEMAS['port']})
        if "urn" not in post_dict:
            post_dict.update({"urn":self.consts.URN_STRING + "port=" + \
                              post_dict.get("name", "")})
        if "location" not in post_dict:
            post_dict.update({"location":self.consts.LOCATION})
        if not self.unis_url:
            self._add_unis_fields(post_dict)
            return post_dict
        if not headers:
            headers=self._def_headers('port')
        
        post_json = json.dumps(post_dict, indent=2)
        url = self.unis_url + '/ports'
        logger.info('post_port')
        logger.debug('post_port', post=post_json)
        try:
            r = requests.post(url, data=post_json, headers=headers)
        except Exception as e:
            logger.exc('post_port', e)
        h = self._handle_response(r)
        return h

    def get_metadata(self, subject, event_type, parameters):
        if not self.unis_url:
            return None
        get = dict({"$schema":self.consts.SCHEMAS['metadata'],
                    "subject": dict({"href":subject,
                                      "rel":"full"}),
                     "eventType":event_type,
                     "parameters": parameters})
        url = self.unis_url + "metadata?"
        url += "subject.href=" + subject
        url += "&eventType=" + event_type
        url += "&parameters.collectionInterval=" +\
               str(parameters["collectionInterval"])
        logger.info('get_metadata')
        logger.debug('get_metadata', query=url)
        r = requests.get(url)
        h = self._handle_response(r)
        return h
        
    # def _read_cached_metadata(self):
    #     try:
    #         md_fname = settings.METADATA_CACHE
    #     except AttributeError:
    #         md_fname = "/tmp/blippmd"
    #     try:
    #         md_file=open(md_fname, 'r')
    #     except IOError:
    #         ### LOG metadata cache could not be opened
    #         return None
    #     try:
    #         md=json.loads(md_file.read())
    #     except ValueError:
    #         ### LOG ValueError: metadata file could not be read as json
    #         return None
    #     return md
    
    def _handle_response(self, r):
        if r.status_code==200: #query OK
            logger.info("handle_response", resp=r.status_code)
            logger.debug("handle_response", resp=r.status_code, headers=str(r.headers), msg=r.text)
            return json.loads(r.text)
        elif r.status_code==201: #insert succesful
            logger.info("handle_response", resp=r.status_code)
            logger.debug("handle_response", resp=r.status_code, headers=str(r.headers), msg=r.text)
            return json.loads(r.text)
        elif r.status_code==401: #unauthorized
            logger.error("handle_response", resp=r.status_code, msg=r.text)
            return r.status_code
        elif r.status_code==500: # internal server error
            logger.error("handle_response", resp=r.status_code, msg=r.text)
            return r.status_code
        elif r.status_code==304: # not modified
            # requests might handle this automagically?
            # if we have a cached version use it
            # not implemented yet
            ### LOG using cached version
            return 304
        elif r.status_code==404: # not found
            logger.error("handle_response", resp=r.status_code, msg=r.text)
            return None
        elif r.status_code==409: # conflict - thing already exists
            logger.warn("handle_response", resp=r.status_code, msg=r.text)
            return 409
        elif r.status_code==400: # bad request
            logger.error("handle_response", resp=r.status_code, msg=r.text)
            return 400
        else:
            logger.error("handle_response", resp=r.status_code, msg=r.text)
            return -1
