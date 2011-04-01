#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

import sys, types
from django.http import HttpResponse
import urllib
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from models import FeatureCounter


@csrf_exempt
def webhook_receiver(request):
    """
        Accept the API's webhook callback. Increcment the feature counter  by 1
    """
    
    if not request.method == 'POST':
       return HttpResponse("GET NOT ALLOWED", status=400)

    if not request.POST.has_key('webhook_key'):
        return HttpResponse("NO KEY SO AUTH FAILED", status=401)
    
    if not str(request.POST['webhook_key']) == str(settings.TX_WEBHOOK_KEY):  
        return HttpResponse("WEBHOOK KEYS DO NOT MATCH SO AUTH FAILED", status=401)
    
    try:
        fc=FeatureCounter.objects.get(pk=1)
        fc.featurecounter=int(fc.featurecounter) + 1
        fc.save()
    except(FeatureCounter.DoesNotExist):
        fc=FeatureCounter.objects.create(featurecounter=1)
        fc.save()
    
    return HttpResponse("OK")
