#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf.urls.defaults import *
from django.core.urlresolvers import reverse
from . import views

urlpatterns = patterns('',
    #Webhook
    url(r'^receiver/', views.webhook_receiver, name="webhook_receiver"),
)