#!/usr/bin/env python
# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext as _, ugettext_lazy as __
from django.db.utils import DatabaseError
import json

class ClassifierTypes(models.Model):
    class Meta:
        verbose_name = __("ClassifierType")
        verbose_name_plural = __("ClassifierTypes")
        ordering = ('name',)
    
    name    = models.CharField(max_length=75, unique=True)
    slug    = models.CharField(max_length=75, unique=True)
    
    def __unicode__(self):
        return self.slug

class ClassifierCategories(models.Model):
    class Meta:
        verbose_name = __("ClassifierCategory")
        verbose_name_plural = __("ClassifierCategories")
        ordering = ('name',)
    
    type    = models.ForeignKey(ClassifierTypes)
    name    = models.CharField(max_length=75, unique=True)
    slug    = models.CharField(max_length=75, unique=True)    
    duplicate_distance_tolerance= models.IntegerField(default=1)
    
    def __unicode__(self):
        return self.slug
    
class ClassifierSubcategories(models.Model):
    class Meta:
        verbose_name = __("ClassifierSubcategory")
        verbose_name_plural = __("ClassifierSubcategories")
        ordering = ('name',)
    
    category    = models.ForeignKey(ClassifierCategories)
    name        = models.CharField(max_length=75, unique=True)
    slug        = models.CharField(max_length=75, unique=True)    
    
    def __unicode__(self):
        return self.slug
    
    
class Classifiers(models.Model):
    category= models.ForeignKey(ClassifierCategories)
    subcategory= models.ForeignKey(ClassifierSubcategories, blank=True, null=True)
    
    class Meta:
        verbose_name = __("Classifier")
        verbose_name_plural = __("Classifiers")
        unique_together = (("category", "subcategory",) )
    
    def __unicode__(self):
        if self.subcategory:
            return "%s.%s.%s" % (self.category.type, self.category, self.subcategory)
        else:
            return "%s.%s" % (self.category.type, self.category)
    
    def __to_dict__(self):
        if self.subcategory:
            d={"type":          self.category.type.slug,
                "category":     self.category.slug,
                "subcategory":  self.subcategory.slug}
        else:
            d={"type":          self.category.type.slug,
               "category":      self.category.slug,
               "subcategory":   ""}
        return d
    
    def __to_json__(self):
        return json.dumps(self.__to_dict__())



class Since(models.Model):
    sinceid = models.IntegerField(default=0)
    def __unicode__(self):
        return str(self.sinceid)


"""type of GIS"""
geometry_choices =(
                ('Point','Point'),
                ('LineString','LineString'),
                ('Polygon','Polygon'),
             )

forbidden_system_fields =('gr_status','gr_validity')

tr_status_fields =('latest','depricated')


status_choices=(('Latest', 'Latest'),('Depricated', 'Depricated'))
            
geometry_choices_tuple =('Point','LineString','Polygon')


validity_choices=(('Unconfirmed','Unconfirmed'),('Validated', 'Validated'))



# Create your models here.
