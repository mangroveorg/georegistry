from django.db import models

class FeatureCounter(models.Model):
    featurecounter= models.IntegerField()

    def __unicode__(self):
        return '#features=%s' % (featurecounter)

