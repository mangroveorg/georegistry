from django.db import models
from georegistry.simple_locations.iso3166_2letter import two_letter_country_code_choices
from georegistry.features.forms import classifier_choices
from georegistry.features.models import ClassifierTypes, ClassifierCategories

class AllFeaturesCounter(models.Model):
    count= models.IntegerField(default=0)

    def __unicode__(self):
        return str(self.count)

class CountryFeaturesCounter(models.Model):
    country_code = models.CharField(max_length=2,
                                    choices=two_letter_country_code_choices,
                                    unique=True)
    count        = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s=%s' % (self.country_code, self.count)
        

class ClassifierTypeFeaturesCounter(models.Model):
    classifier_type = models.ForeignKey(ClassifierTypes, unique=True)
    count      = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s=%s' % (self.classifier_type,  self.count)
    
class ClassifierCategoryFeaturesCounter(models.Model):
    classifier_category = models.ForeignKey(ClassifierCategories, unique=True)
    count      = models.IntegerField(default=0)

    def __unicode__(self):
        return '%s=%s' % (self.classifier_category, self.count)