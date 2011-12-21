from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


from periscope.topology.models import NetworkObject, Service, EventType

class DNSCache(models.Model):
    # TODO (AH): add timestamp and timeout period for each entry
    hostname = models.CharField(max_length=256, null=True)
    ip = models.CharField(max_length=40, null=True)
    timestamp = models.DateTimeField(auto_now=True)

    def __unicode__(self):
        return "%s: %s" % (self.hostname, self.ip)
    
class Units(models.Model):
    pass


class Metadata(models.Model):
    subject = models.ForeignKey(NetworkObject)
    event_type = models.ForeignKey(EventType)
    service = models.ForeignKey(Service, null=True, related_name='metadatas')
    key = models.CharField(max_length=255, null=True)
    poll = models.BooleanField(default=False)
    last_poll = models.DateTimeField(null=True)
    # TODO (AH) add interval for scheduled pulling
    
    def __unicode__(self):
        return self.subject.__unicode__() + ': ' + self.event_type.value


class Data(models.Model):
    metadata = models.ForeignKey(Metadata)
    time = models.DateTimeField()
    value = models.FloatField()
    units = models.CharField(max_length=50)
    
    def __unicode__(self):
        return str(self.value)

class EventTypes(object):
    pass

class UrnStub(object):
    pass
