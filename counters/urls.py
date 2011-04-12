#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from . import views


urlpatterns = patterns('',
    #counters
    
    url(r'^cached-total/$', views.query_allfeature_counter,
        name="query_allfeature_counter"),
    
    url(r'^cached-country/(?P<country_code>[^/]+)$', views.query_countryfeature_counter,
        name="query_allfeature_counter"),
    
    url(r'^cached-classifier/(?P<classifer_level>[^/]+)/(?P<classifier_slug>[^/]+)$',
        views.query_classifierfeature_counter,
        name="query_classifierfeature_counter"),
        
    url(r'^build-cached-total/$', views.build_allfeature_counter,
        name="build_allfeature_counter"),
    
    url(r'^build-cached-country/(?P<country_code>[^/]+)$',
        views.build_countryfeature_counter, name="build_countryfeature_counter"),
    
    url(r'^build-cached-classifier/(?P<classifer_level>[^/]+)/(?P<classifier_slug>[^/]+)$',
        views.build_classifierfeature_counter, name="build_classifierfeature_counter"),
    

)