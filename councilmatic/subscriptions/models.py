import datetime
from django.db import models

import django.contrib.auth.models as auth
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic

class DistributionChannel (models.Model):
    recipient = models.ForeignKey(auth.User, null=True)
    
    class Meta:
        abstract = True

class EmailChannel (DistributionChannel):
    email = models.CharField(max_length=256)
    
    def __unicode__(self):
        return "Email to %s" % self.email

class RssChannel (DistributionChannel):
    pass

class SmsChannel (DistributionChannel):
    number = models.CharField(max_length=32)
    carrier = models.CharField(max_length=32)
    
    def __unitcode__(self):
        return "Send SMS to %s number %s" % (self.carrier, self.number)

    
class Subscription (models.Model):
    channel = models.ForeignKey('EmailChannel', null=True)
    last_sent = models.DateTimeField()
    
    def save(self, *args, **kwargs):
        """On save, update timestamps."""
        
        # We could use Django's built-in ability to make this an auto_now field,
        # but then we couldn't change the value when we want.
        if not self.id:
            self.last_sent = datetime.datetime.now()
        super(Subscription, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return self.email

class SearchSubscription (Subscription):
    query = models.TextField()
    
    def __unicode__(self):
        return self.query
