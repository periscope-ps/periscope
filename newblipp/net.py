import os
from pprint import pprint
import ethtool
from unis_client import UNISInstance

class Proc:
    """Wrapper to opening files in /proc
    """
    def __init__(self, dirname="/proc"):
        """Initialize with optional alternate dirname.
        """
        self._dir = dirname

    def open(self, *path):
        """Open a given file under proc.
        'path' is a sequence of path components like ('net', 'dev')
        """
        return open(os.path.join(self._dir, *path))

    def exists(self, *path):
        try:
            a = open(os.path.join(self._dir, *path))
            return a
        except IOError:
            return False

class Probe:
    """Get network statistics
    """
    UNUSED_METRICS = ["errs_in", "errs_out", "drop_in", "drop_out",
                      "fifo_in", "fifo_out", "frame_in", "compressed_in",
                      "compressed_out", "multicast_in", "colls_out",
                      "carrier_out"]
    
    def __init__(self, **kwargs):
        self._proc = Proc(kwargs.get("proc_dir", "/proc/"))
        self.unis_url=kwargs.get("unis_url", None)
        self.node_subject=kwargs.get("subject", "this_node")
        self.subjects=self.get_interface_subjects()


    def get_data(self):
        netdev = self._proc.open('net', 'dev')
        netsnmp = self._proc.open('net', 'snmp')
        data = {}
        netdev.readline() # Should be 'Inter-| Receive | Transmit'
        heads = netdev.readline()
        headscl = []
        t = False
        r = False
        for item in heads.split():
            if item.startswith('|'):
                t = True
                item = item[1:]
            elif item.count('|'):
                its = item.split('|')
                i1 = its[0]
                headscl.append(i1 + "_in")
                t = False
                r = True
                item = its[1]
            if t:
                item += "_in"
            elif r:
                item += "_out"
            headscl.append(item)

        for line in netdev.readlines():
            line = line.split()
            if line[0][-1] != ":":
                line = line[0].split(":") + line[1:]
                line[0] += ":"
            a = dict(zip(headscl[1:], line[1:]))
            a["errors"]=int(a["errs_in"])+int(a["errs_out"])
            a["drops"]=int(a["drop_in"])+int(a["drop_out"])
            for metric in self.UNUSED_METRICS:
                if metric in a:
                    del a[metric]
            data[self.subjects[line[0][:-1]]] = a

        data[self.node_subject] = {}
        line = netsnmp.readline()
        while line:
            line = line.split()
            if line[0].lower()=="tcp:":
                in_index      = line.index("InSegs")
                out_index     = line.index("OutSegs")
                retrans_index = line.index("RetransSegs")
                dataline = netsnmp.readline().split()
                data[self.node_subject].update({"tcp_segments_in":dataline[in_index],
                                     "tcp_segments_out":dataline[out_index],
                                     "tcp_retrans":dataline[retrans_index]})
            elif line[0].lower()=="udp:":
                in_index  = line.index("InDatagrams")
                out_index = line.index("OutDatagrams")
                dataline = netsnmp.readline().split()                
                data[self.node_subject].update({"datagrams_in":dataline[in_index],
                                     "datagrams_out":dataline[out_index]})
            line = netsnmp.readline()
#        print "PRINTING DATA FROM NET:"
#        pprint(data)
        return data

    def get_interface_subjects(self):
        netdev = self._proc.open('net', 'dev')
        faces = []
        subjects = {}
        for line in netdev:
            line = line.split()
            if line[0].count(":"):
                faces.append(line[0][:line[0].index(":")])
        unis = UNISInstance(unis_url=self.unis_url)
        for face in faces:
            try:
                capacity = ethtool.get_speed(face)
            except OSError:
                capacity = 0
            ### some sort of verification here that capacity is right
            post_dict={"name":face,
                       "capacity":capacity}
            resp = unis.post_port(post_dict)
            if isinstance(resp, dict):
                subjects[face]=resp['selfRef']
        return subjects
