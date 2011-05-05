from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes import generic


from periscope.topology.models import NetworkObject, Service, EventType

class DNSCache(models.Model):
    hostname = models.CharField(max_length=256, null=True)
    ip = models.CharField(max_length=16, null=True)

class Units(models.Model):
    pass

# Adapted from GENI branch, with a little change
# The subject is a generic relation because EndPointPair and Path are
# not of type NetworkObject
class Metadata(models.Model):
    #subject = models.ForeignKey(NetworkObject)
    event_type = models.ForeignKey(EventType)
    service = models.ForeignKey(Service, null=True, related_name='metadatas')
    key = models.CharField(max_length=255, null=True)
    poll = models.BooleanField(default=False)
    
    objectType = models.ForeignKey(ContentType)
    objectID = models.PositiveIntegerField()
    subject = generic.GenericForeignKey('objectType', 'objectID')
    def __unicode__(self):
        return self.subject.unis_id + ': ' + self.event_type.value


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
