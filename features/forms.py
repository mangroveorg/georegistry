#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django import forms

from validators import country_code, subdivision_code, geometry
from models import geometry_choices, validity_choices, status_choices, level_choices

from georegistry.rest_mongo.forms import JsonMongoForm
from models import Classifiers


try:
    classifiers_list=[]
    classifiers_list2=[]
    cl=Classifiers.objects.all()
    for i in cl:
        classifiers_list.append(i)
        classifiers_list2.append(i)
    classifiers_list=tuple(classifiers_list)
    
    classifier_choices_tuple=tuple(classifiers_list)
    classifier_choices=tuple(zip(classifiers_list2, classifiers_list))
    
except():
    pass

class FeatureUploadForm(JsonMongoForm):
    """ Create / update a geographic feature and save it into MongoDB """
    
    TYPE = 'FeatureCollection'
    
    name = forms.CharField(max_length=300, label="Name")
    alt_names = forms.CharField(max_length=300,
                                label="List of Comma-seperated Alternate Names in double quotes",
                                required=False
                                )
    
    tags = forms.CharField(max_length=300,
                                label="List of Comma-seperated tags in double quotes",
                                required=False
                                )
    file  = forms.FileField(required=False)
    
    geometry_type = forms.TypedChoiceField(label="Geometry Type*", 
                                          choices=geometry_choices )
    geometry_coordinates = forms.CharField(widget=forms.Textarea(),
                                            label="Geometry Coordinates", 
                                           required=False)
    geometry_centroid = forms.CharField(widget=forms.Textarea(),
                                        label="Geometry Centroid", 
                                           required=False)
    bounds = forms.CharField(widget=forms.Textarea(), label="Bounds",
                                    required=False)
    
    classifiers = forms.TypedChoiceField(label="Classifiers", 
                                    choices=classifier_choices)
    country_code = forms.CharField(max_length=2, 
                                   label="2 Letter ISO Country Code (Level 0)",
                                   validators=[country_code.validate])
    subdivision_code = forms.CharField(max_length=2, 
                                       label="ISO Subdivision Code (Level 1)",
                                       required=False
                                       #validators=[subdivision_code.validate]
                                       )
    level = forms.TypedChoiceField(label="Admin Level", choices=level_choices,
                                   required=False)
    
    level2_admin_boarder_code = forms.CharField(max_length=50, required=False, 
                                              label="3rd Level Boarder Code")
    level3_admin_boarder_code = forms.CharField(max_length=50, required=False, 
                                               label="4th Level Boarder Code")
    level4_admin_boarder_code = forms.CharField(max_length=50, required=False, 
                                               label="5th Level Boarder Code")
    time_begin = forms.DateTimeField(required=False)
    time_end = forms.DateTimeField(required=False)
    centerpoint = forms.CharField(label="Centerpoint", required=False)
    subcategory = forms.CharField(max_length=300, label="Subcategory", required=False)
    town = forms.CharField(max_length=300, label="Town", required=False)
    license = forms.CharField(max_length=300, label="License", required=False)
    abbr = forms.CharField(max_length=300, label="abbr", required=False)
    website = forms.CharField(max_length=300, label="website", required=False)
    phone = forms.CharField(max_length=300, label="phone", required=False)
    mobile = forms.CharField(max_length=300, label="mobile", required=False)
    address = forms.CharField(max_length=300, label="address", required=False)
    postcode = forms.CharField(max_length=30, label="Postal Code", required=False)
    owner = forms.CharField(max_length=300, label="owner", required=False)
    license = forms.CharField(max_length=300, label="license", required=False)
    contact_name=forms.CharField(max_length=300, label="contact_name", required=False)
    contact_position=forms.CharField(max_length=300, label="contact_position", required=False)
   
    
    
    def clean_geometry_coordinates(self, *args, **kwargs):
        """Clean the Geometry Coordinates"""
        geometry_coordinates = self.cleaned_data['geometry_coordinates']
        geometry_type = self.cleaned_data['geometry_type']
        geometry.validate(geometry_coordinates, geometry_type)
        return geometry_coordinates

    def clean_country_code(self, *args, **kwargs):
        country_code = self.cleaned_data['country_code']
        return country_code.upper()

    def clean_subdivision_code(self, *args, **kwargs):
        subdivision_code = self.cleaned_data['subdivision_code']
        return subdivision_code.upper()


class FeatureUpdateUploadForm(JsonMongoForm):
    """ Create / update a geographic feature and save it into Mongo DB """
    
    TYPE = 'FeatureCollection'
    feature_id = forms.CharField(max_length=300, label="FeatureID")
    name = forms.CharField(max_length=300, label="Name", required=False)
    alt_names = forms.CharField(max_length=300,
                                label="List of Comma-seperated Alternate Names in double quotes",
                                required=False
                                )
    file  = forms.FileField(required=False)
    tags = forms.CharField(max_length=300,
                                label="List of Comma-seperated tags in double quotes",
                                required=False
                                )
    geometry_type = forms.TypedChoiceField(label="Geometry Type*", 
                                          choices=geometry_choices, required=False )
    geometry_coordinates = forms.CharField(label="Geometry Coordinates", 
                                           required=False)
    
    classifiers = forms.TypedChoiceField(label="Classifiers", choices=classifier_choices)
    country_code = forms.CharField(max_length=2, 
                                   label="2 Letter ISO Country Code (Level 0)",
                                   validators=[country_code.validate])
    subdivision_code = forms.CharField(max_length=2, 
                                       label="ISO Subdivision Code (Level 1)",
                                       validators=[subdivision_code.validate])
    level2_admin_boarder_code = forms.CharField(max_length=50, required=False, 
                                              label="3rd Level Boarder Code")
    level3_admin_boarder_code = forms.CharField(max_length=50, required=False, 
                                               label="4th Level Boarder Code")
    level4_admin_boarder_code = forms.CharField(max_length=50, required=False, 
                                               label="5th Level Boarder Code")
    time_begin = forms.DateTimeField(required=False)
    time_end = forms.DateTimeField(required=False)
    centerpoint = forms.CharField(label="Centerpoint", required=False)
    subcategory = forms.CharField(max_length=300, label="Subcategory", required=False)
    town = forms.CharField(max_length=300, label="Town", required=False)
    license = forms.CharField(max_length=300, label="License", required=False)
    abbr = forms.CharField(max_length=300, label="abbr", required=False)
    website = forms.CharField(max_length=300, label="website", required=False)
    phone = forms.CharField(max_length=300, label="phone", required=False)
    mobile = forms.CharField(max_length=300, label="mobile", required=False)
    address = forms.CharField(max_length=300, label="address", required=False)
    postcode = forms.CharField(max_length=30, label="Postal Code", required=False)
    owner = forms.CharField(max_length=300, label="owner", required=False)
    license = forms.CharField(max_length=300, label="license", required=False)
    contact_name=forms.CharField(max_length=300, label="contact_name", required=False)
    contact_position=forms.CharField(max_length=300, label="contact_position", required=False)
    
    
    def clean_geometry_coordinates(self, *args, **kwargs):
        geometry_coordinates = self.cleaned_data['geometry_coordinates']
        geometry_type = self.cleaned_data['geometry_type']
        geometry.validate(geometry_coordinates, geometry_type)
        return geometry_coordinates

    def clean_country_code(self, *args, **kwargs):
        country_code = self.cleaned_data['country_code']
        return country_code.upper()

    def clean_subdivision_code(self, *args, **kwargs):
        subdivision_code = self.cleaned_data['subdivision_code']
        return subdivision_code.upper()

class FeatureEditUploadForm(JsonMongoForm):
    """ Create / update a geographic feature and save it into Mongo DB """
    
    TYPE = 'FeatureCollection'
    feature_id = forms.CharField(max_length=300, label="FeatureID")
    edit = forms.TypedChoiceField(label="EditFlag", choices=( ('true','true'), ) )
    name = forms.CharField(max_length=300, label="Name", required=False)
    alt_names = forms.CharField(max_length=300,
                                label="List of Comma-seperated Alternate Names in double quotes",
                                required=False
                                )
    file  = forms.FileField(required=False)
    tags = forms.CharField(max_length=300,
                                label="List of Comma-seperated tags in double quotes",
                                required=False
                                )
    
    geometry_type = forms.TypedChoiceField(label="Geometry Type*", 
                                          choices=geometry_choices, required=False )
    geometry_coordinates = forms.CharField(label="Geometry Coordinates", 
                                           required=False)
    
    classifiers = forms.TypedChoiceField(label="Classifiers", choices=classifier_choices)    
    
    country_code = forms.CharField(max_length=2, 
                                   label="2 Letter ISO Country Code (Level 0)",
                                   validators=[country_code.validate])
    subdivision_code = forms.CharField(max_length=2, 
                                       label="ISO Subdivision Code (Level 1)",
                                       validators=[subdivision_code.validate])
    level2_admin_boarder_code = forms.CharField(max_length=50, required=False, 
                                              label="3rd Level Boarder Code")
    level3_admin_boarder_code = forms.CharField(max_length=50, required=False, 
                                               label="4th Level Boarder Code")
    level4_admin_boarder_code = forms.CharField(max_length=50, required=False, 
                                               label="5th Level Boarder Code")
    time_begin = forms.DateTimeField(required=False)
    time_end = forms.DateTimeField(required=False)
    
    centerpoint = forms.CharField(label="Centerpoint", required=False)
    subcategory = forms.CharField(max_length=300, label="Subcategory", required=False)
    
    town = forms.CharField(max_length=300, label="Town", required=False)
    license = forms.CharField(max_length=300, label="License", required=False)
    abbr = forms.CharField(max_length=300, label="abbr", required=False)
    website = forms.CharField(max_length=300, label="website", required=False)
    phone = forms.CharField(max_length=300, label="phone", required=False)
    mobile = forms.CharField(max_length=300, label="mobile", required=False)
    address = forms.CharField(max_length=300, label="address", required=False)
    postcode = forms.CharField(max_length=30, label="Postal Code", required=False)
    owner = forms.CharField(max_length=300, label="owner", required=False)
    license = forms.CharField(max_length=300, label="license", required=False)
    contact_name=forms.CharField(max_length=300, label="contact_name", required=False)
    contact_position=forms.CharField(max_length=300, label="contact_position", required=False)
    
    def clean_geometry_coordinates(self, *args, **kwargs):
        geometry_coordinates = self.cleaned_data['geometry_coordinates']
        geometry_type = self.cleaned_data['geometry_type']
        geometry.validate(geometry_coordinates, geometry_type)
        return geometry_coordinates

    def clean_country_code(self, *args, **kwargs):
        country_code = self.cleaned_data['country_code']
        return country_code.upper()

    def clean_subdivision_code(self, *args, **kwargs):
        subdivision_code = self.cleaned_data['subdivision_code']
        return subdivision_code.upper()


class FeatureVerifyUploadForm(JsonMongoForm):
    """ Create / update a geographic feature and save it into Mongo DB """
    
    TYPE = 'FeatureCollection'
    feature_id = forms.CharField(max_length=300, label="FeatureID")


class FeatureDeleteUploadForm(JsonMongoForm):
    """ Create / update a geographic feature and save it into Mongo DB """
    
    TYPE = 'FeatureCollection'
    feature_id = forms.CharField(max_length=300, label="FeatureID")
