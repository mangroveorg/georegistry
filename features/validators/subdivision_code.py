#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

from django.core.exceptions import ValidationError

from georegistry.simple_locations.models import Area

def validate(s):
    """
        Check if the given subdivision_code exists in Database. Raise 
        ValidationError otherwise.
    """
    s=s.upper()
    if not Area.objects.filter(two_letter_iso_subdivision_code=s).exists():
        raise ValidationError("The subdivision %s " % s)

