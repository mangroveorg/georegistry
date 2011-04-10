#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

try:
    import json
except ImportError:
    import simplejson as json

import qrencode

from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.conf import settings
from forms import *
from django.views.decorators.csrf import csrf_exempt
from utils import delete_from_mongo, raw_query_mongo_db
from pymongo.son import SON
from georegistry.rest_mongo.views import create_document, update_document, edit_document, get_document_by

from georegistry.accounts.decorators import json_login_required, access_required
from georegistry.simple_locations.models import Area
from django.core import serializers

@json_login_required
def test_authorization(request):
    """
        Test to see if your API credentials are working
    """
    jsonstr = {"status": 200, "message": "You were logged in."}
    jsonstr = json.dumps(jsonstr, indent=4)	
    return HttpResponse(jsonstr, status=200, mimetype='application/json')

@csrf_exempt    
@json_login_required
@access_required("create_feature")
def create_feature(request):
    """
        Create a geographic feature and save it in Mongo DB.
    """
    if request.method == 'POST':
        newdoc=create_document(request, FeatureUploadForm)
        return HttpResponse(newdoc['body'], status=newdoc['status'])
    
    return render_to_response('upload/feature.html', 
                             {'form': FeatureUploadForm()},
                              context_instance = RequestContext(request))

@csrf_exempt 
@json_login_required
@access_required("delete_feature")
def delete_feature(request):
    """
        Update a geographic feature and save changes in Mongo DB.
        
        If the feature doesn't exits, return a 404 error.
    """
        
    if request.method == 'POST':
        if request.POST.has_key('feature_id'):
            r = delete_from_mongo(request.POST['feature_id'])
            return HttpResponse("DELETED", status=200)

    
    return render_to_response('upload/feature.html', 
                              {'form': FeatureDeleteUploadForm()},
                              context_instance = RequestContext(request))

@csrf_exempt     
@json_login_required
@access_required("edit_feature")
def edit_feature(request, feature_id, collection_name=None):
    """
        Edit specific Fields in a geographic feature and save changes in Mongo DB.
        
        If the feature doesn't exits, return a 404 error.
    """
   
    if request.method == 'POST':
        return edit_document(request, feature_id, FeatureUpdateUploadForm)

    r = get_document_by(request, id=feature_id, search_in=('get',),
                        collection_name=collection_name)
    
    r=raw_query_mongo_db({'id': feature_id}, collection_name=collection_name)
    
    r['results'][0].update({'feature_id':r['results'][0]['id']})

    return render_to_response('upload/feature.html', 
                              {'form': FeatureEditUploadForm(r['results'][0])},
                              context_instance = RequestContext(request))

@csrf_exempt
@json_login_required
@access_required("update_feature")
def update_feature(request):
    """
        Update a geographic feature and save changes in Mongo DB.
        
        If the feature doesn't exits, return a 404 error.
    """
    
    if request.method == 'POST':
        return update_document(request, request.POST['feature_id'], FeatureUpdateUploadForm)

    
    return render_to_response('upload/feature.html', 
                              {'form': FeatureUpdateUploadForm()},
                              context_instance = RequestContext(request))
 
 
#@json_login_required
#@access_required("read_feature")
def get_json_feature_by_id(request, feature_id, collection_name=None): 
    """ Return geographic feature matching feature_id. """
    return get_document_by(request, id=feature_id, search_in=('url',),
                           collection_name=collection_name)
  

#@json_login_required
#@access_required("read_feature")
def get_json_feature_by_id_and_epoch(request, feature_id, 
                                     epoch, collection_name=None):   
    #import ipdb; ipdb.set_trace()
    
    if epoch=="all":
        return get_document_by(request, id=feature_id,
                           search_in=('url',),
                           collection_name=[settings.MONGO_DB_NAME,
                                            settings.MONGO_HISTORYDB_NAME])
    else:
        """ Return geographic feature matching feature_id and epoch. """
        return get_document_by(request, id=feature_id, epoch=epoch,
                           search_in=('url',), collection_name=collection_name)


#@json_login_required
#@access_required("read_feature")
def get_qr_feature_by(request, collection_name=None, **kwargs):
    """
        Return QR code image matching the geographic feature matching
        kwargs.
    """
    json_response = get_document_by(request, search_in=('url',), 
                                    collection_name=collection_name, **kwargs)
    
    jr=json.loads(json_response.content)
    if jr['status'] != 200:
        return json_response
   
    response = HttpResponse(mimetype="image/png")
    image = qrencode.encode_scaled(json_response.content, 400)
    image[2].save(response, "PNG")
    return response


#@json_login_required
#@access_required("read_feature")
def get_qr_feature_by_id(request, feature_id, collection_name=None):
    """
        Return QR code image matching the geographic feature matching
        feature_id.
    """
    json_response = get_document_by(request, id=feature_id, search_in=('url',),
                           collection_name=collection_name)
    
    jr=json.loads(json_response.content)
    if jr['status'] != 200:
        return json_response
   
    response = HttpResponse(mimetype="image/png")
    image = qrencode.encode_scaled(json_response.content, 400)
    image[2].save(response, "PNG")
    return response
    

#@json_login_required
#@access_required("read_feature")
def get_qr_feature_by_id_and_epoch(request, feature_id, 
                                   epoch, collection_name=None):
    """
        Return QR code image matching the geographic feature matching
        feature_id and epoch.
    """
    json_response = get_document_by(request, id=feature_id, epoch=epoch,
                           search_in=('url',), collection_name=collection_name)
    
    jr=json.loads(json_response.content)
    if jr['status'] != 200:
        return json_response
   
    response = HttpResponse(mimetype="image/png")
    image = qrencode.encode_scaled(json_response.content, 400)
    image[2].save(response, "PNG")
    return response
    
    


#@json_login_required
#@access_required("read_feature")
def get_features_in_country_subdivision(request, country_subdivision_code):
    country_subdivision_code = country_subdivision_code.upper()
    
    split_values=country_subdivision_code.split("-")
    if len(split_values)==1:
        """ Return geographic feature matching country & subdivision_code. """
        return get_document_by(request, search_in=('url',), 
                           country_code=split_values[0])
    
    return get_document_by(request, search_in=('url',), 
                           country_code=split_values[0], subdivision_code=split_values[1])



#@json_login_required
#@access_required("read_feature")
def get_features_search_dict(request):
    """
        Return a geographic features matching GET parameters.
    """
    return get_document_by(request, search_in=('get',))


#@json_login_required
#@access_required("read_feature")
def get_features_in_boundingbox(request, botleft_lon, botleft_lat,
                                topright_lon, topright_lat):
    """
        Return a geographic features located withing the bouding box and 
        matching GET parameters if any.
    """
    botleft = [float(botleft_lon), float(botleft_lat)]
    topright = [float(topright_lon), float(topright_lat)]
    searchbox = {'$box': [botleft, topright]}
    
    return get_document_by(request, search_in=('url', 'get'),
                           geometry_coordinates={'$within': searchbox})
   
   
#@json_login_required
#@access_required("read_feature")
def get_features_at_point(request, lon, lat):
    """
        Return a geographic features located at these exact coordinates.
    """
    return get_document_by(request, 
                           geometry_coordinates=[float(lon), float(lat)])
 
    
#@json_login_required
#@access_required("read_feature")
def get_features_near_point(request, lat, lon, max_distance=None, limit=None):
    """
        Return a geographic features located neat these coordinates.
    """
    ll = {'$near':[float(lat), float(lon)]}
    if max_distance:
        md={'$maxDistance': max_distance}
        q=SON(ll)
        q.update(md)
        return get_document_by(request, limit=limit, search_in=('url', 'get'),
                               geometry_coordinates=q,
                               )
    else:
        return get_document_by(request, limit=limit, search_in=('url', 'get'),
                               geometry_coordinates=ll,
                               )

#@json_login_required
def get_features_in_polygon(request, feature_id):
    return HttpResponse("Not implemented yet.")


#@json_login_required
def get_features_containing_point(request, lon, lat):
    return HttpResponse("Not implemented yet.")

#@json_login_required
#@access_required("read_feature")
def get_features_classifiers(request):
    """
        Return a list of a classifiers.
    """
    l=[]
    cl=Classifiers.objects.all()
    for c in cl:
        l.append(c.__to_dict__())
    return HttpResponse(json.dumps(l, indent=4), status=200)






#@json_login_required
#@access_required("read_feature")   
def get_features_locations(request):
    """
        Return a list of a coutries in areas.
    """
    loc_tree={}
    c=[]

    areas=Area.objects.all()
    for a in areas:
        loc={}
        loc={"name":a.name, "level":a.level, "slug":a.slug}

        if a.level==0:
            loc.update({"country_code":a.two_letter_iso_country_code,
                        "parent":None, "children":[]})
            loc_tree.update({a.slug:loc})
            
        elif a.level==1:
            loc.update({"subdivision_code":a.two_letter_iso_subdivision_code,
                "parent":a.parent.slug, "children":[]})
        else:
            loc.update({"parent":a.parent.slug, "children":[]})
        
        c.append(loc)
    
    nl=[]
    for i in c:
        nl.append(i)
        if i['level']==1:
            nl.pop()
            if loc_tree.has_key(i['parent']):
                #print loc_tree[i['parent']]
                loc_tree[i['parent']]["children"].append(i)
        
                
    for k in loc_tree.keys():
        
        if loc_tree[k]['children']:
            for i in loc_tree[k]['children']:
                for j in nl:
                    if j['level']==2 and j['parent']==i['slug']:
                        i['children'].append(j)
        
    
    return HttpResponse(json.dumps(loc_tree, indent=4), status=200)

#@json_login_required
#@access_required("read_feature")   
def get_features_countries(request):
    """
        Return a list of a coutries in areas.
    """
    l=[]
    areas=Area.objects.all()
    for a in areas:
        if a.two_letter_iso_country_code not in l:
            l.append(a.two_letter_iso_country_code)
    return HttpResponse(json.dumps(l), status=200)

#@json_login_required
#@access_required("read_feature")
def get_features_subdivisions(request):
    """
        Return a list of subdivisions in areas.
    """
    
    sd={}
    c=[]
    areas=Area.objects.all()
    for a in areas:
        if a.two_letter_iso_country_code not in c:
            c.append(a.two_letter_iso_country_code)
    
    for i in c:    
        sl=[]
        subs=Area.objects.filter(two_letter_iso_country_code=i)
        for s in subs:
            if s not in sl:
                if s.two_letter_iso_subdivision_code!="":
                    sl.append(s.two_letter_iso_subdivision_code)
        sd[i]=sl
 
    return HttpResponse(json.dumps(sd), status=200)
