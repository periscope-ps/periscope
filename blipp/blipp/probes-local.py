"""
BLiPP probes
"""
__author__ = "Dan Gunter <dkgunter@lbl.gov>"
__rcsid__ = "$Id$"

# System imports
import array
import fcntl
import hashlib
import os
import socket
import struct
import subprocess
import sys
import time

# Third-party imports
try:
    import Web10G
except ImportError:
    Web10G = None
    
# Local imports
from blipp import base
from blipp.base import paste_types

## Constants and globals
## ---------------------

## Classes and functions
## ---------------------

def _pexec(cmd, *args):
    """Execute cmd + args and return stdout as a string.
    """
    return subprocess.Popen([cmd] + list(args), stdout=subprocess.PIPE).communicate()[0]

def _pexecln(cmd, *args):
    """Execute cmd + args and return stdout as a list of strings split on newlines.
    """
    return _pexec(cmd, *args).split('\n')

def get_jiffy_ms():
    """Figure out how many millesconds per jiffy.
    """
    hz = os.sysconf(os.sysconf_names['SC_CLK_TCK'])
    return 1000 / hz

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

class TCPStats:
    # Web10G names for TCP 4-tuple
    TCP_TUPLE_NAMES = ('LocalAddress','LocalPort', 'RemAddress', 'RemPort')

    def conn_match(self, local_addr, local_port=-1, remote_addr="*", remote_port=-1):
        """Get TCP statistics from Web10G for matched connection(s).

        Does UNIX-style pattern matching on address strings (local_addr, remote_addr).

        Args:
            local_addr - Local TCP address string. May also be 4-tuple allowing the function
                         to be called with a tuple or 4 arguments.
            local_port - Local TCP port integer.
            remote_addr - Remote TCP address string.
            remote_port - Remote TCP port integer.

        Raises:
            NotImplementedError - If Web10G module was not found at import time.
            ValueError - Improper arguments
            Web10G.error - Error talking to Web10G infrastructure

        Returns:
            { (src1, sport1, dst1, dport1) : { stat : value, .. },
               (src2, sport2, dst2, dport2) : { stat : value, .. }, ... }
        """
        if Web10G is None:
            raise NotImplementedError("Web10G module not found")
        # 'Connect' to Web10G
        agent = Web10Gagent()
        # Split out first argument if it's a 4-tuple instead of a string.
        if not isinstance(local_addr, basestring):
            if not (hasattr(local_addr,'__len__') and len(local_addr) == 4):
                raise ValueError("Must specify 4 arguments, or 4-tuple as first argument")
            local_addr, local_port, remote_addr, remote_port = local_addr
        # Get matching connections
        clist = agent.connection_match(local_addr, local_port, remote_addr, remote_port)
        # Build result
        result = { }
        for conn in clist:
            key = tuple([c.read(name) for name in TCP_TUPLE_NAMES])
            values = c.readall()
            # remove the redundant tuple-keys from the values
            for name in TCP_TUPLE_NAMES:
                del values[name]
            result[key] = values
        # Done
        return result

def get_net_dev(proc=None, active=[ ], **ignore):
    """Input is format of /proc/net/dev on linux.

    Details: Parse second line in header so different fields can be understood:
      "face |bytes    packets errs drop fifo frame compressed multicast|\
       bytes    packets errs drop fifo colls carrier compressed"

    Args:
        proc - Instance of Proc
        active - List of interfaces (usually, active ones) to include in results.
                 If falsy, all interfaces will be included, otherwise
                 only those listed will be included.

    Return: { interface : { event : value, .. } }
    """
    result = { }
    iface_map = { }
    if active:
        iface_filter = dict.fromkeys(active)
    else:
        iface_filter = { }
    f = proc.open('net', 'dev')
    # parse header
    f.readline() # skip hdr line 1
    hdr = f.readline()
    _, r, x = hdr.split('|')
    value_fields = (('rcv',r.split()),('snd',x.split()))
    # parse body
    for line in f:
        iface, v = line.split(':')
        iface = iface.strip()
        values = v.strip().split()
        if iface_filter and not iface in iface_filter:
            continue
        valuedict = { }
        now = time.time()
        for i, (valtype, fields) in enumerate(value_fields):
            for field in fields:
                strval = values[i]
                try:
                    value = int(strval)
                except ValueError:
                    value = float(strval)
                valuedict[field] = [value] # caller expects a list
        result[iface] = valuedict
    return result

class CPUInfo:

    CPU_TYPE = "socket"
    CORE_TYPE = "core"
    
    def __init__(self, proc=None, **ignore):
        self._proc = proc
        self._prev_cpu_hz = { }
        self._prev_cpu_total_hz = { }
        
    def get_data(self):
        """Get host CPU information.
        
        Return: list [ cpu  = list [ value, [ per-core-values.. ] ], ... ]
        """    
        # Get system total from uptime. This will be used
        # to scale the CPU numbers to percentages.
        #f = open(os.path.join(self._dir, "uptime"), "r")
        #up_total, up_idle = map(float, f.readline().split())
        #total_elapsed = up_total - self._prev_up_total
        #if total_elapsed == 0: # not enough time has passed
        #    return self._prev_cpudata
        #self._prev_up_total = up_total
        # Get stat
        result, cpu = [ ], -1
        f = self._proc.open("stat")
        for line in f:
            fields = line.split()
            key = fields[0]
            v = map(int, fields[1:])
            # cpu
            if key.startswith('cpu'):
                if key == 'cpu':
                    # new cpu
                    result.append([ { }, [ ] ])
                    cpu = len(result) - 1
                    core = -1
                else:
                    core = int(key[3:])
                idx = (cpu, core)
                # basic values
                cpudata = dict(zip(('user', 'nice', 'sys', 'idle'), v[0:4]))
                # extended values
                if len(v) >= 7:
                    cpudata.update(dict(zip(('iowait', 'irq', 'softirq'),
                                            v[4:7])))
                # calculate deltas and scale
                prev_values = self._prev_cpu_hz.get(idx, {})
                prev_total = self._prev_cpu_total_hz.get(idx, 0.0)
                total_hz = sum(v)
                total_elapsed_hz = total_hz - prev_total
                for key, value in cpudata.items():
                    prev = prev_values.get(key, 0.0)
                    elapsed_hz = value - prev
                    if total_elapsed_hz == 0:
                        cpudata[key] = 0.0
                    else:
                        cpudata[key] = 1.0 * elapsed_hz / total_elapsed_hz
                    prev_values[key] = value # save abs. value
                if core == -1:
                    result[cpu][0] = cpudata
                else:
                    # don't assume cores come in order; expand list
                    while len(result[cpu][1]) <= core:
                        result[cpu][1].append({})
                    result[cpu][1][core] = cpudata
                self._prev_cpu_hz[idx] = prev_values
                self._prev_cpu_total_hz[idx] = total_hz
        return result

def get_uname():
    """Use os.uname() to get host OS info.
    Returns dictionary that can be used, e.g., to fill in a 'subject'.
    """
    r = os.uname()
    return dict(name=r[0], version=r[2], details=r[3], arch=r[4])

def get_hostname():
    """Get canonical host name.
    """
    return socket.getfqdn()

def get_hostip():
    """Get canonical host ip
    """
    hname = socket.gethostname()
    return socket.gethostbyname(hname)

def get_all_interfaces(max_possible=128):
    """Get a list of all interface names.
    """
    max_bytes = max_possible * 32
    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    sockfd = sock.fileno()
    names = array.array('B', '\0' * max_bytes)
    names_addr = names.buffer_info()[0]
    addresses = fcntl.ioctl(sockfd, SIOCGIFCONF,
                            struct.pack('iL', max_bytes, names_addr))
    outbytes = struct.unpack('iL', addresses)[0]
    namestr = names.tostring()
    return [namestr[i:i+32].split('\0', 1)[0] for i in range(0, outbytes, 32)]

def get_iface_meta(pid, stats, **ts_params):
    iface_meta, meta_blocks = { }, [ ]
    for iface in stats.keys():        
        meta1 = base.MetaBlock(event_type=paste_types(base.BASE_ET, 'interface'),
                               subject={'interface':iface}, parent=pid)
        meta2 = base.MetaBlock(event_type=paste_types(base.BASE_ET, 'timeseries'),
                               parent=meta1.ident,
                               params=ts_params)
        meta_blocks.append(meta1)
        meta_blocks.append(meta2)
        iface_meta[iface] = meta2
    return iface_meta, meta_blocks

class ProcessInfo:
    """Info about a specific process.
    """
    ET = 'process' # event type base
    
    def __init__(self, pid, proc=None):
        self._proc=proc
        self._pid = int(pid)
        self._pidstr = str(pid)
        # stat's state
        self._prev_u, self._prev_s = (None, None)
        # self._jfms = get_jiffy_ms() XXX: Might need this later?
        
    def get_meta(self):
        """Get metadata about the process.

        Return: (subject-dict, params-dict)
        """
        subj = { 'process' : self._pid }
        return (subj, { })
        
    def get_data(self):
        """Get new data about process.

        Return: dict { event_type => data }
        """
        result = { }

        self._stat(result)
        self._statm(result)
        self._io(result)
        self._net(result)
        
        return result

    def _stat(self, d):
        f = self._proc.open(self._pidstr, 'stat')
        fld = f.readline().split()
        nm = lambda s: s#paste_types(base.BASE_ET, self.ET, 'stat', s)

        # calculate user/sys time since last call from overall numbers
        u, s = int(fld[13]), int(fld[14])
        if self._prev_u:
            du, ds = u - self._prev_u, s - self._prev_s
            if du + ds > 0:
                pct_utime, pct_stime = du / (du + ds) * 100, ds / (du + ds) * 100
            else:
                pct_utime, pct_stime = 50, 50 # arbitrary, but should sum to 100
        else:
            if u + s > 0:
                pct_utime, pct_stime = u / (u + s) * 1.0, s / (u + s) * 1.0
            else:
                pct_utime, pct_stime = 50, 50 # arbitrary, but should sum to 100
        self._prev_u, self._prev_s = 1.0 * u, 1.0 * s

        d.update({
            nm('prog') : fld[1],
            nm('state') : fld[2],
            nm('ppid') : int(fld[3]),
            nm('pgrp') : int(fld[4]),
            nm('majflt'): int(fld[11]),
            nm('pct_utime') : pct_utime,
            nm('pct_stime') : pct_stime,
            nm('vsize') : int(fld[22]),
            nm('rss') : int(fld[23]),
            nm('rlim') : int(fld[24]), })

    def _statm(self, d):
        pass

    def _io(self, d):
        pass

    def _net(self, d):
        pass

    
def __test_web10g(*args):
    t = TCPStats()
    d = t.conn_match(args)
    for key, value in d.items():
        print("  {key} : {value}\n".format(key=key, value=value))

if __name__ == '__main__':
    import sys
    __test_web10g(sys.argv[1], int(sys.argv[2]),
                  sys.argv[3], int(sys.argv[4]))
