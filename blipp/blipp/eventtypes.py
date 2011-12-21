"""
Event types.

Don't do anything that will cause problems with 'import *', since that's how
this module will be imported.
"""


def et_paste(*args):
    return ':'.join(args)

def et_split(s, start=None, end=None):
    fld = s.split(':')
    if start is None:
        return fld
    elif end is None:
        if start < 0:
            return fld[start:]
        else:
            return fld[start:start+1]
    else:
        return fld[start:end]

## Constants and globals
## ---------------------

BASE_ET = "ps:host"
BASE_NET_ET = "ps:net"
CPU_ET = "cpu"

IF_ET = et_paste(BASE_ET, 'interface')
NETDEV_ET = et_paste(BASE_ET, 'net', 'dev')
STAT_ET = et_paste(BASE_ET, 'stat')
PID_ET = et_paste(BASE_ET, 'stat', 'process')
CPU_STAT_ET = et_paste(BASE_ET, 'stat', 'cpu')
CPU_ET = et_paste(BASE_ET,  'cpu')
NET_TCP_ET = et_paste(BASE_ET, 'tcp')
