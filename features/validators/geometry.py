#!/usr/bin/env python
# -*- coding: utf-8 -*-
# vim: ai ts=4 sts=4 et sw=4

try:
    import json
except ImportError:
    import simplejson as json

from django.core.exceptions import ValidationError
    
from georegistry.features.models import geometry_choices_tuple


def validate(geometry_coordinates, geometry_type):
    """
    Ensure the given geometry is a valid Polygon, Linestring or Point. Raise
    ValidationError otherwise.
    """
    #Check geometry is a list
    try:
        l = json.loads(geometry_coordinates)
        if type(l) != type([]):
            raise ValidationError("Invalid coordinates list.")  
    except:
        raise ValidationError("Invalid coordinates list.")
    
    # Check geometry_type is valid
    if not geometry_type in geometry_choices_tuple:
        raise ValidationError("%s is not a valid geometry_type. "\
                              "Choose from %s." % (geometry_type, 
                                            ", ".join(geometry_choices_tuple)))
    
    if geometry_type == "Polygon":
        if len(l) < 3:
            raise ValidationError("A Polygon must have at least 3 coordinates.")
        try:
            for i in l:
                lon = float(i[0])
                lat = float(i[1])
            #TODO: Check for valid Coords.
            #TODO: add an exception to the execpt and avoid catching everything
        except:
            raise ValidationError("lon/lat were not valid values.")
        
    if geometry_type == "LineString":
        if len(l) < 2:
            raise ValidationError("A Linestring must have 2 or more coordinates.")
        try:
            for i in l:
                lon = float(i[0])
                lat = float(i[1])
            #TODO: Check for valid Coords.
        except:
            raise ValidationError("lon/lat were not valid values.")
    
    if geometry_type == "Point" :
        if len(l)!=2:
            raise ValidationError("A point can only have 2 coordinates.")
        try:
            lon = float(l[0])
            lat = float(l[1])
            #TODO: Check for valid Coords.
        except:
            raise ValidationError("lon/lat were not valid values.")
    
