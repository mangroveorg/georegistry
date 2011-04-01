#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy as __
from django.db.utils import DatabaseError


class FacilityType(models.Model):
    class Meta:
        verbose_name = __("FacilityType")
        verbose_name_plural = __("FacilityTypes")
        ordering = ('name',)

    name = models.CharField(max_length=75, unique=True)
    slug = models.CharField(max_length=75, unique=True)
    duplicate_distance_tolerance= models.IntegerField(default=1)
    
    def __unicode__(self):
        return self.name


try:
    facility_type_list=[]
    ft=FacilityType.objects.all()
    for i in ft:
        facility_type_list.append(i.slug)
    facility_type_list2=facility_type_list
    facility_type_list=tuple(facility_type_list)
    
    properties_feature_type_choices_tuple=tuple(facility_type_list)
    properties_feature_type_choices=tuple(zip(facility_type_list, facility_type_list2))
    
except():
    pass

"""type of GIS"""
geometry_choices =(
                ('Point','Point'),
                ('LineString','LineString'),
                ('Polygon','Polygon'),
             )

forbidden_system_fields =('tr_status','tr_validity')

tr_status_fields =('latest','depricated')

tr_validity_fields=('tr_status','tr_validity')

status_choices=(('Latest', 'Latest'),('Depricated', 'Depricated'))
            
geometry_choices_tuple =('Point','LineString','Polygon')


validity_choices=(('Unconfirmed','Unconfirmed'),('Validated', 'Validated'))

status_choices=(('Latest', 'Latest'),('Depricated', 'Depricated'))


# Create your models here.
