#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import datetime, time
import Geohash
import pymongo
from pymongo import Connection, json_util

try:
    import json
except ImportError:
    import simplejson as json
    
import os, uuid, time, sys
from datetime import datetime, timedelta
from django.conf import settings 


def build_utcnow_epoch_timestamp():
    """Build a timestamp in epoch format from UTC time"""
    date = datetime.utcnow().timetuple()
    return "%d" % time.mktime(date)
    
    
def build_pretty_id(guid):
    """Build a pretty id"""
    return "GR_%s%s" % (guid[0:8], guid[24:36])
    
def build_geohash_id(lat, lon):
    """Build a GR id with an embedded geohash"""
    gh = Geohash.encode(lat, lon)
    id="GR_%s" % (gh)
    return str(id)

def query_mongo_db_forms(kwargs, collection_name=None):
    """forms"""
    forms=[]
    response_dict={'status': 404,
                   'type': 'Form',
                   'forms': forms,
                   'total': 0
                   }
    try:
        mconnection =  Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db = 	   mconnection[settings.MONGO_DB_NAME]
        
        if not collection_name:
            """if no collection givben use the main one"""
            transactions = db[settings.MONGO_FORMDB_NAME]

        elif (collection_name=="form_history"):
            """otherwise query 'historical' if specified"""
            transactions = db[settings.MONGO_HISTORYFORMDB_NAME]
        
        mysearchresult=transactions.find(kwargs)
        mysearchcount=mysearchresult.count()
        if mysearchcount>0:
            response_dict['status']=200
            response_dict['total']=mysearchcount
            for d in mysearchresult:
                response_dict['forms'].append(d)
    except:
        print "Error reading from Mongo"
        print str(sys.exc_info())
        response_dict['status']=400
        response_dict['type']="Error"
        response_dict['message']=str(sys.exc_info())
    return response_dict

    
    
#if not in this list then we should pack it into properties or geometry
top_level_fields=('total', 'status', 'geometry',)
feature_level_fields=('id', 'epoch', 'sinceid', '_id', '')
def query_mongo_db(kwargs, limit=None, collection_name=None):
    """
    query mongo and unflatten the results so its pretty json
    """
    """return a result list or an empty list"""
    if limit:
        limit=int(limit)
    features=[]
    search_list=False
    response_dict={'status': 404,
                   'type': 'FeatureCollection',
                   'features': features,
                   'total': 0
                   }    
    try:
        if kwargs.has_key('country_code'):
            kwargs['country_code']=kwargs['country_code'].upper()
        
        if kwargs.has_key('subdivision_code'):
            kwargs['subdivision_code']=kwargs['subdivision_code'].upper()
        
        mconnection =  Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db = 	   mconnection[settings.MONGO_DB_NAME]
        transactions = db[settings.MONGO_DB_NAME]
        if not collection_name:
            """if no collection given, use the main one"""
            transactions = db[settings.MONGO_DB_NAME]
        elif type(collection_name)==list:
            search_list=True
        else:
            transactions = db[collection_name]

        if not search_list:
            
            if kwargs.has_key('name'):
                """search has name so lets search for alt name too."""
                searchname=kwargs['name']
                if limit:
                    mysearchresult=transactions.find({'alt_names' :searchname}).limit(limit)
                else:
                    mysearchresult=transactions.find({'alt_names' :searchname})
                mysearchcount=mysearchresult.count()
                if mysearchcount>0:
                    response_dict['status']=200
                    response_dict['total']=response_dict['total']+ mysearchcount
                    for d in mysearchresult:
                        d=unflatten(d)
                        response_dict['features'].append(d)
                        d['type']="Feature"
            if limit:            
                mysearchresult=transactions.find(kwargs).limit(limit)    
            else:
                mysearchresult=transactions.find(kwargs)
            mysearchcount=mysearchresult.count()
            if mysearchcount>0:
                response_dict['status']=200
                response_dict['total']=response_dict['total']+ mysearchcount
                for d in mysearchresult:
                    d=unflatten(d)
                    response_dict['features'].append(d)
                    d['type']="Feature"
            response_dict['total']=len(response_dict['features'])
        else:
            response_dict['total']=0
            for i in collection_name:
                transactions = db[i]
                if kwargs.has_key('name'):
                    """search has name so lets search for alt name too."""
                    searchname=kwargs['name']
                    if limit:
                        mysearchresult=transactions.find({'alt_names' :searchname}).limit(limit)
                    else:
                        mysearchresult=transactions.find({'alt_names' :searchname})
                    mysearchcount=mysearchresult.count()
                    if mysearchcount>0:
                        response_dict['status']=200
                        response_dict['total']=response_dict['total']+ mysearchcount
                        for d in mysearchresult:
                            d=unflatten(d)
                            response_dict['features'].append(d)
                            d['type']="Feature"

                if limit:
                    mysearchresult=transactions.find(kwargs).limit(limit)
                else:
                    mysearchresult=transactions.find(kwargs)
                mysearchcount=mysearchresult.count()
                if mysearchcount>0:
                    response_dict['status']=200
                    response_dict['total']=response_dict['total'] + mysearchcount
                    for d in mysearchresult:
                        d=unflatten(d)
                        response_dict['features'].append(d)
                        d['type']="Feature"
                response_dict['total']=len(response_dict['features'])
    except:
        print "Error reading from Mongo"
        print str(sys.exc_info())
        response_dict['status']=400
        response_dict['type']="Error"
        response_dict['message']=str(sys.exc_info())
    return response_dict


def raw_query_mongo_db(kwargs, collection_name=None):
    print collection_name
    print kwargs
    #for key in kwargs:
    #    print "arg: %s: %s" % (key, kwargs[key])

    """return a result list or an empty list"""
    l=[]
    response_dict={}
    
    try:
        mconnection =  Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db = 	   mconnection[settings.MONGO_DB_NAME]
        if not collection_name:
            transactions = db[settings.MONGO_DB_NAME]
        elif (collection_name=="history"):
            transactions = db[settings.MONGO_HISTORYDB_NAME]
        elif (collection_name=="verified"):
            transactions = db[settings.MONGO_VERIFIEDDB_NAME]
        
        mysearchresult=transactions.find(kwargs)
        mysearchcount=mysearchresult.count()
        if mysearchcount>0:
            response_dict['status']=200
            for d in mysearchresult:
                l.append(d)
            response_dict['results']=l
    except:
        print "Error reading from Mongo"
        print str(sys.exc_info())
        response_dict['status']=400
        response_dict['type']="Error"
        response_dict['message']=str(sys.exc_info())
    return response_dict




def build_json_error(status, message, **kwargs):
    d={'status': status, 'message': message}
    if kwargs:
        d.update(kwargs)
        d.j=json.dumps(d)
    return j


def flatten_dict(dct):
    return dict([ (str(k), dct.get(k)) for k in dct.keys() ])

def add_href(d):
    if d.has_key('id'):
        d['href']="%s%s.json" % (settings.BASE_FEATURES_URL,
                              d['id'],
                              )
    return d

def unflatten_geometry(d):
    """Unflatten gemoetry"""
    d['geometry'] = {"type": str(d['geometry_type']),
                     "coordinates": list(d['geometry_coordinates'])
                     }
    del d['geometry_type']
    del d['geometry_coordinates']
    return d
    

def unflatten_properties(d):
    """"Unflatten the results"""
    """Place any item not in top_level_fields into properties"""
    properties={}
    for k,v in d.items():
        if k not in top_level_fields:
            properties[k]=v
            del d[k]
    for k,v in properties.items():
        if k in feature_level_fields:
            d[k]=v
            del properties[k]
    d['properties']=properties
    return d

def unflatten(d):
    "Unflatten results from object store into GeoJSON"
    return unflatten_properties(unflatten_geometry(add_href(d)))
