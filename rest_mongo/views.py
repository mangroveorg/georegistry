#!/usr/bin/env python
# -*- coding: utf-8 -*-

try:
    import json
except ImportError:
    import simplejson

from django.http import HttpResponse

from utils import query_mongo_db


def create_document(request, form_class, additional_fields={}, render_response=True):
    """
        Take data from a POST request, merge it with additional fields,
        validate it with a form and save it in mongo then return
        either an HTML response, a JSON response or a Python dict.
        
        ::keyword request:: the Django request object
        ::keyword form_class:: the Django form class to validate 
                               the data against
        ::keyword additional_fields:: optional, additional data to update 
                                      the POST dict with
        ::keyword render_response:: optional, whether to return an HTTPResponse or
                                    a Python dict. Default is True.
    """
    
    data = request.POST.copy()
    data.update(additional_fields)
    form = form_class(data, request)
    responsedict = form.save() if form.is_valid() else form.errors 
    r={}
    r['status']=responsedict['status']
    r['body']= json.dumps(responsedict, indent=4)
    return r

    
def update_document(request, feature_id, 
                   form_class, additional_fields={}, render_response=True):
    """
        Check if the document to be updated exists in DB or raise 404.
    
        Take data from a POST request, merge it with additional fields,
        validate it with a form and save it in mongo then return
        either an HTML response, a JSON response or a Python dict.
        
        ::keyword request:: the Django request object
        ::keyword document_id:: the id of the document in MongoDB.
        ::keyword form_class:: the Django form class to validate 
                               the data against
        ::keyword additional_fields:: optional, additional data to update 
                                      the POST dict with
        ::keyword render_response:: optional, wheter to return an HTTPResponse 
                                    or a Python dict. Default is True.
    """
 
    # Feature exists or 404
    responsedict = query_mongo_db({"id": feature_id})
    
    if responsedict['status'] != 200:
        responsedict['message'] = "The document handle could not be located. "\
                                 "Perhaps you mean to create instead of update?"
        responsedict['type'] = "Error"
    
    else: 
        data = request.POST.copy()
        data.update(additional_fields)
        
        form = form_class(data, request)
        responsedict = form.save(feature_id) if form.is_valid() else form.errors
        
    if not render_response:
        return responsedict 
        
    return HttpResponse(json.dumps(responsedict, indent=4), 
                        status=responsedict['status']) 
   
   
def edit_document(request, feature_id, 
                   form_class, additional_fields={}, render_response=True): 
    """
        Check if the document to be updated exists in DB or raise 404.
    
        Take data from a POST request, merge it with additional fields,
        validate it with a form and save it in mongo then return
        either an HTML response, a JSON response or a Python dict.
        
        ::keyword request:: the Django request object
        ::keyword document_id:: the id of the document in MongoDB.
        ::keyword form_class:: the Django form class to validate 
                               the data against
        ::keyword additional_fields:: optional, additional data to update 
                                      the POST dict with
        ::keyword render_response:: optional, wheter to return an HTTPResponse 
                                    or a Python dict. Default is True.
    """
 
    # Feature exists or 404
    responsedict = query_mongo_db({"id": feature_id})
    
    if responsedict['status'] != 200:
        responsedict['message'] = "The document handle to edit could not be located. "
        responsedict['type'] = "Error"
    
    else: 
        data = request.POST.copy()
        data.update(additional_fields)
        
        form = form_class(data, request)
        responsedict = form.save(feature_id) if form.is_valid() else form.errors
        
    if not render_response:
        return responsedict 
        
    return HttpResponse(json.dumps(responsedict, indent=4), 
                        status=responsedict['status'])                         

def get_document_by(request, limit=None, collection_name=None, 
                    search_in=('get', 'post', 'url'), 
                    render_response=True, **kwargs):
    """
        Return a JSON reponse containing the documents matching criteria in
        GET, POST and kwargs. Will search only in collection_name if given.
        
        ::keyword request:: the Django request object
        ::keyword collection_name:: the MongoDB collection to search the data in.
                                    If None, search in all of them. Default is
                                    None
        ::keyword search_in:: list of variables where to get the data
                              to filter from among 'get' (in the GET request params),
                              'post' (in the POST request params), and 'url'
                              (kwargs arguments). 
                              Default is 'get', 'post' and 'url'.
        ::keyword render_response:: optional, wheter to return an HTTPResponse 
                                    or a Python dict. Default is True.
    """   
    
    data = {}
    search = {'get': request.GET, 'post': request.POST, 'url': kwargs}
    
    # cast querydict in dict and merge them in one dict
    for s in search_in:
        data.update(search[s].iteritems())

    responsedict = query_mongo_db(data, limit, collection_name)
    
    if not render_response:
        return responsedict
                              
    return HttpResponse(json.dumps(responsedict, indent=4), 
                        status=responsedict['status'],
                        mimetype='application/json') 
    
