#!/usr/bin/env python
# -*- coding: utf-8 -*-

import uuid
import datetime, time
import sys

try:
    import json
except ImportError:
    import simplejson as json

from django.conf import settings   

from pymongo import Connection, json_util

import os, uuid, time, sys
from datetime import datetime, timedelta
from georegistry import settings
from models import Since, Classifiers
import Geohash

#if not in this list then we should pack it into properties or geometry
top_level_fields=('total', 'status', 'geometry',)

from georegistry.rest_mongo.utils import build_utcnow_epoch_timestamp, build_pretty_id
from georegistry.rest_mongo.utils import build_geohash_id, unflatten_geometry, unflatten_properties
from georegistry.rest_mongo.utils import unflatten, raw_query_mongo_db, query_mongo_db 
from georegistry.rest_mongo.views import get_document_by
from pymongo.son import SON
from georegistry.features.models import ClassifierCategories

def check_for_pos_dupes_via_geoloc(attrs, collection_name=None):
    if attrs['geometry_type']=="Point":
            ll = {'$near':[float(attrs['geometry_coordinates'][0]),
                           float(attrs['geometry_coordinates'][1] )]}
	    cc = ClassifierCategories.objects.get(slug=attrs['classifiers']['category'])
            md={'$maxDistance': int(cc.duplicate_distance_tolerance)}
            q=SON(ll)
            q.update(md)

            gq={'geometry_coordinates': q,
                'classifiers.category': attrs['classifiers']['category']}

	    x=query_mongo_db(gq, collection_name=collection_name)

	    if x.has_key('features'):
                if len(x['features'])>0:
                    attrs['possible_duplicate']=True
    return attrs
    
def delete_from_mongo(tr_id, collection_name=None):
    
    try:
        mconnection =  Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db = mconnection[settings.MONGO_DB_NAME]
        
        if not collection_name:
            """if no collection givben use the main one"""
            transactions = db[settings.MONGO_DB_NAME] 
        else:
            transactions = db[collection_name]
              
    except:
        print str(sys.exc_info())
        result_list=[]
    
    try: 
    
        if tr_id:
            print """DELETE""", tr_id
            r=transactions.remove({'id':tr_id})
            print r
        else:
            print """DELETE CERTIAN FIELDS of: """, tr_id
            r=transactions.remove(attrs)
            print r
            
    except():
        print str(sys.exc_info())

def save_to_mongo(attrs, tr_id=None, collection_name=None):
    """returns the saved object or an empty list"""
    result_list=[]
    try:
        mconnection =  Connection(settings.MONGO_HOST, settings.MONGO_PORT)
        db = mconnection[settings.MONGO_DB_NAME]
        
        if not collection_name:
            """if no collection given, use the main one"""
            transactions = db[settings.MONGO_DB_NAME] 
        else:
            transactions = db[collection_name]
            
        history = db[settings.MONGO_HISTORYDB_NAME]    
    except:
        #print str(sys.exc_info())
        result_list=[]    
    
    s=Since.objects.get(pk=1)   
    
    try: 
        """Make sure out coordinates are a list, not a string """
        attrs['geometry_coordinates']=json.loads(attrs['geometry_coordinates'])
        """Convert alt_names into a list"""    
        if attrs.has_key('alt_names'):
            attrs['alt_names']=json.loads(attrs['alt_names'])
        """Convert tags into a list"""    
        if attrs.has_key('tags'):
                attrs['tags']=json.loads(attrs['tags'])   
	if attrs.has_key('classifiers'):
	    #print "Classifiers: ", attrs['classifiers']
	    attrs['classifiers']=json.loads(attrs['classifiers'])
	
        if tr_id:
            """Copy the old tx to the historical collection"""        
            responsedict=raw_query_mongo_db({'id': tr_id})
            hist_id=history.insert(responsedict['results'])
            """Use the original tx_id handle"""
            attrs['id']=str(tr_id)
            

            """Set the new uuid"""
            s=Since.objects.get(pk=1)
	    """Set the Since ID"""
            attrs['sinceid']=s.sinceid
            
            if attrs.has_key('alt_names'):
                attrs['alt_names']=json.loads(attrs['alt_names'])
                
            if attrs.has_key('tags'):
                attrs['tags']=json.loads(attrs['tags'])
            
            attrs['_id']=str(uuid.uuid4())
            attrs['history']=True
            attrs['verified']=False
            attrs['epoch']=build_utcnow_epoch_timestamp()
            #ensure the old version is out of the main collection
            my_id=transactions.remove({"id":tr_id })
            #insert the updated version
            my_id=transactions.insert(attrs)
            mysearchresult=transactions.find({'_id':attrs['_id']}) 
            
        else:
            """The feature is NEW"""
            
            """
            Check to see if the a similar item exists closeby.
            If so, flag this as a possible duplicate.
            """
            attrs=check_for_pos_dupes_via_geoloc(attrs,
                                                 collection_name=collection_name)
            """Set the new uuid"""
            attrs['_id']=str(uuid.uuid4())
            """build the tr_id a.k.a. handle"""
            if attrs['geometry_type']=='Point':
                attrs['id']=build_geohash_id(attrs['geometry_coordinates'][0],
                                             attrs['geometry_coordinates'][1])
                
            else:
                attrs['id']=build_pretty_id(attrs['_id'])
            

                
            """Set the Since ID"""
            attrs['sinceid']=s.sinceid
            attrs['verified']=False
            attrs['epoch']=build_utcnow_epoch_timestamp()
            my_id=transactions.insert(attrs)
            mysearchresult=transactions.find({'_id':attrs['_id']})
            
        for d in mysearchresult:
            d=unflatten(d)
            result_list.append(d)
            d['type']="Feature"
        """Increment the sinceid"""
        s.sinceid=int(s.sinceid) + 1
        s.save()
    except:
        
        
        result_list=[]
    return result_list
