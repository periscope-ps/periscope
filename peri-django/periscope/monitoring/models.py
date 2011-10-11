from django.db import models
from periscope.topology.models import NetworkObject


class PathDataModel(models.Model):
    path_id = models.CharField(max_length=200)
    src = models.CharField(max_length=200)
    dst = models.CharField(max_length=200)
    src_port_range = models.CharField(max_length=200)
    dst_port_range = models.CharField(max_length=200)
    vlan_id = models.CharField(max_length=200)
    direction = models.CharField(max_length=200)
    start_time = models.IntegerField()
    duration = models.IntegerField()
    bandwidth = models.IntegerField()
    bw_class = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    
    def __unicode__(self):
        return self.path_id
	
class GridFTPTransfer(models.Model):
    transfer_id = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    src = models.CharField(max_length=200)
    dst = models.CharField(max_length=200)
    src_port = models.CharField(max_length=200)
    dst_port = models.CharField(max_length=200)
    user = models.CharField(max_length=200)
    misc = models.CharField(max_length=500)

    def __unicode__(self):
        return self.transfer_id

class NetworkObjectStatus(models.Model):
    network_object = models.ForeignKey(NetworkObject)
    status = models.CharField(max_length=200)
    last_update = models.DateTimeField(null=True)
