#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.conf import settings

if not getattr(settings, 'TEST', False):
    raise Exception("You must user use a test setting file. Try "\
                    "./manage.py --settings=rest_mongo.test_settings test")

from http_api import *
