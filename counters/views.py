#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import sys, types
from django.http import HttpResponse
import urllib
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from models import AllFeaturesCounter, CountryFeaturesCounter
from models import ClassifierTypeFeaturesCounter, ClassifierCategoryFeaturesCounter
from georegistry.rest_mongo.utils import raw_count_mongo_db
from georegistry.features.models import ClassifierTypes, ClassifierCategories
import json
from georegistry.accounts.decorators import json_login_required, access_required


def query_allfeature_counter(request, collection_name=None):
    try:
        fc=AllFeaturesCounter.objects.get(pk=1)
        r={"status": 200, "count":int(fc.count)}
    except(AllFeaturesCounter.DoesNotExist):
        r={"status": 404, "type":"Error", "message":"Not found."}
    
    return HttpResponse(json.dumps(r, indent=4), status=404)
        
def query_countryfeature_counter(request, country_code, collection_name=None):
    try:
        fc=CountryFeaturesCounter.objects.get(country_code=country_code)
        r={"status": 200, "count":int(fc.count)}
    except(CountryFeaturesCounter.DoesNotExist):
        r={"status": 404, "type":"Error", "message":"Not found."}
    
    return HttpResponse(json.dumps(r, indent=4), status=404)
def query_classifierfeature_counter(request, classifer_level,
                                classifier_slug, collection_name=None):
    if classifer_level=="type":
        try:
            fc=ClassifierTypeFeaturesCounter.objects.get(classifier_type__slug=classifier_slug)
            r={"status": 200, "count":int(fc.count)}
        except(ClassifierTypeFeaturesCounter.DoesNotExist):
            r={"status": 404, "type":"Error", "message":"Not found."}
    
    elif classifer_level=="category":
        try:
            fc=ClassifierCategoryFeaturesCounter.objects.get(classifier_category__slug=classifier_slug)
            r={"status": 200, "count":int(fc.count)}
        except(ClassifierCategoryFeaturesCounter.DoesNotExist):
            r={"status": 404, "type":"Error", "message":"Not found."}
    else:
        r={"status": 404, "type":"Error", "message":"Not found."}
    
    return HttpResponse(json.dumps(r, indent=4), status=404)
#@json_login_required
#@access_required("read_feature")
def build_allfeature_counter(request, collection_name=None):
    """
        Build a count of all features in the system
    """
    
    if request.method == 'POST':
       return HttpResponse("POST NOT ALLOWED", status=400)

    r=raw_count_mongo_db({}, collection_name)
    
    try:
        fc=AllFeaturesCounter.objects.get(pk=1)
        fc.count=int(r['count'])
        fc.save()
    except(AllFeaturesCounter.DoesNotExist):
        fc=AllFeaturesCounter.objects.create(counter=int(r['count']))
        fc.save()
    
    return HttpResponse(json.dumps(r,indent=4))

#@json_login_required
#@access_required("read_feature")
def build_countryfeature_counter(request, country_code, collection_name=None):
    """
        Build a count of all features in the system
    """
    
    if request.method == 'POST':
       return HttpResponse("POST NOT ALLOWED", status=400)

    r=raw_count_mongo_db({'country_code':country_code}, collection_name)

    if r['count']!=0:
        try:
            fc=CountryFeaturesCounter.objects.get(country_code=country_code)
            fc.count=int(r['count'])
            fc.save()
        except(CountryFeaturesCounter.DoesNotExist):
            fc=CountryFeaturesCounter.objects.create(country_code=country_code,
                                                     count=int(r['count']))
            fc.save()
    return HttpResponse(json.dumps(r,indent=4))

#@json_login_required
#@access_required("read_feature")
def build_classifierfeature_counter(request, classifer_level,
                                    classifier_slug, collection_name=None):
    if request.method == 'POST':
       return HttpResponse("POST NOT ALLOWED", status=400)
    
    search_key="classifiers.%s" % (classifer_level) 
    r=raw_count_mongo_db({search_key:classifier_slug}, collection_name)
    if r['count']!=0:
        if classifer_level=="type":
            try: 
                t=ClassifierTypes.objects.get(slug=classifier_slug)
            except:
                return HttpResponse(json.dumps({'status':404,'type':"Error",
                                                "message": "No such type."},
                                    indent=4), status=404)
            try:
                fc=ClassifierTypeFeaturesCounter.objects.get(classifier_type=t)
                fc.count=int(r['count'])
                fc.save()
            except(ClassifierTypeFeaturesCounter.DoesNotExist):
                fc=ClassifierTypeFeaturesCounter.objects.create(classifier_type=t,
                                                         count=int(r['count']))
                fc.save()
                
        if classifer_level=="category":
            try: 
                c=ClassifierCategories.objects.get(slug=classifier_slug)
            except:
                return HttpResponse(json.dumps({'status':404,'type':"Error",
                                                "message": "No such category."},
                                    indent=4), status=404)
            try:
                fc=ClassifierCategoryFeaturesCounter.objects.get(classifier_category=c)
                fc.count=int(r['count'])
                fc.save()
            except(ClassifierCategoryFeaturesCounter.DoesNotExist):
                fc=ClassifierCategoryFeaturesCounter.objects.create(classifier_category=c,
                                                         count=int(r['count']))
                fc.save()
                
    return HttpResponse(json.dumps(r,indent=4))