from django.db import models

# Create your models here.

class Since(models.Model):
    sinceid = models.IntegerField(default=0)
    
    def __unicode__(self):
        return "%s" % (self.sinceid)