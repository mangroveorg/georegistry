from django.db import models
from django.contrib.auth.models import User
from datetime import date
import types
import json
from django.core.signals import request_finished
from django.db.models.signals import post_save


class UserProfile(models.Model):
    user                = models.ForeignKey(User, unique=True)
    mobile_phone_number = models.CharField(max_length=15, blank=True)
    organization_name   = models.CharField(max_length=100, blank=True)
    twitter             = models.CharField(max_length=50, blank=True)
    
    def __unicode__(self):
        return '%s at %s' % (self.user.email, self.organization_name)


permission_choices=(    ('create_feature',  'create_feature'),
                        ('read_feature',    'read_feature'),
                        ('update_feature',  'update_feature'),
                        ('delete_feature',  'delete_feature'),
                )

class Permission(models.Model):
    user  = models.ForeignKey(User)
    permission_name = models.CharField(max_length=50, choices=permission_choices)

    def __unicode__(self):
        return '%s has the %s permissions' % (self.user.email, self.permission_name)
        
    class Meta:
        unique_together = (("user", "permission_name"),)
        
        
#@receiver(post_save, sender=Permission)
#def my_handler(sender, **kwargs):
#    print kwargs['instance']
#
#post_save.connect(my_handler, sender=Permission)
#
#def my_callback(sender, **kwargs):
#    print "Request finished!"
#
#request_finished.connect(my_callback)