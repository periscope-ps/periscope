import os
import cpu_settings
import settings


# startup
# read config
# check metadata cache based on configured measurements
# use cached metadata, query UNIS for metadata, create mdids
# query MS for collections and create non-existent ones

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


class Probe:
    """Get processor/core statistics.

    Return scaled values instead of raw counters of jiffies.
    """
    CPU_TYPE = "socket"
    CORE_TYPE = "core"
    
    def __init__(self, **kwargs):
        self._proc = Proc(kwargs.get("proc_dir", "/proc/"))
        self._prev_cpu_hz = {}
        self._prev_cpu_total_hz = 0
        
    def get_data(self):
        """Get general host CPU information (first line of /proc/stat)
        
        Return: {'user':.1, 'system':.9, 'nice':0.0, etc... }
        """    
        
        cpu = 0
        stat_file = self._proc.open("stat")
        line = stat_file.readline()
        #timestamp=time.time() # not sure whether this goes here or
                               # just before function call
        fields = line.split()
        key = fields[0]
        v = map(int, fields[1:])
        
        # basic values
        cpudata = dict(zip(('user', 'nice', 'system', 'idle'), v[0:4]))
        # extended values
        if len(v) >= 7:
            cpudata.update(dict(zip(('iowait', 'hwirq', 'swirq'),
                                    v[4:7])))
        # steal and guest if available
        if len(v) >=9:
            cpudata.update(dict(zip(('steal', 'guest'), v[7:9])))
        # calculate deltas and scale
        prev_values = self._prev_cpu_hz
        prev_total = self._prev_cpu_total_hz
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
        (d1, d2, d3) = os.getloadavg()
        cpudata.update({"onemin":d1, "fivemin":d2, "fifteenmin":d3})
        result = cpudata        
        self._prev_cpu_hz = prev_values
        self._prev_cpu_total_hz = total_hz
        return result

class CPUInfo:
    """Get processor/core statistics.

    Return scaled values instead of raw counters of jiffies.
    """
    CPU_TYPE = "socket"
    CORE_TYPE = "core"
    
    def __init__(self, proc=None, **_):
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
        stat_file = self._proc.open("stat")
        for line in stat_file:
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
                cpudata = dict(zip(('user', 'nice', 'system', 'idle'), v[0:4]))
                # extended values
                if len(v) >= 7:
                    cpudata.update(dict(zip(('iowait', 'hwirq', 'swirq'),
                                            v[4:7])))
                # steal and guest if available
                if len(v) >=9:
                    cpudata.update(dict(zip(('steal', 'guest'), v[7:9])))
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

            
            
# def main():
#     try:
#         cpu_settings.COLLECTION_INTERVAL
#         ci=cpu_settings.COLLECTION_INTERVAL
#     except AttributeError:
#         ci,cpu_settings.COLLECTION_INTERVAL=1000,1000
#     try:
#         cpu_settings.REPORTING_INTERVAL
#         ri=cpu_settings.REPORTING_INTERVAL
#     except AttributeError:
#         ri,cpu_settings.REPORTING_INTERVAL=10000,10000
#     try:
#         cpu_settings.UNIS_URL
#     except AttributeError:
#         cpu_settings.UNIS_URL=None
#     try:
#         cpu_settings.MS_URL
#     except AttributeError:
#         cpu_settings.MS_URL=None
#     try:
#         cpu_settings.COLLECTION_TIME
#     except AttributeError:
#         cpu_settings.COLLECTION_TIME=0
#     try:
#         cpu_settings.PROC_DIR
#     except AttributeError:
#         cpu_settings.PROC_DIR="/proc/"
#     if ri<ci:
#         ri=ci
#         ### LOG
#     ### UPDATE UNIS with realized config

#     proc_obj = Proc(cpu_settings.PROC_DIR)
#     cpu_obj = CPUInfoGeneral(proc=proc_obj)

#     # take care of metadata, create collections
#     unis = unis_client.UNISInstance(unis_url=cpu_settings.UNIS_URL)
#     collector = blipp_collector.Collector(ms_url=cpu_settings.MS_URL)
#     mids = {}
#     for metric in cpu_obj.get_data():
#         event_type = blipp_utils.CPU_ET[metric]
#         params = {"datumSchema": blipp_utils.SCHEMAS["datum"],
#                   "collectionInterval": cpu_settings.COLLECTION_INTERVAL
#                   }
#         subject=settings.SUBJECT
#         resp = unis.post_metadata(subject, event_type, params)
#         if isinstance(resp, dict):
#             collector.update_metadatas(resp)
#             mids.update({metric:resp["id"]})
#         else:
#             ### LOG
#             print "metadata post failed, response follows:"
#             print resp

        
    
#     start_time=time.time()
#     end_time=start_time+cpu_settings.COLLECTION_TIME
#     if end_time==start_time:
#         end_time=sys.maxint 

#     last_rtime = 0
#     last_ctime = 0
    
#     # main collection loop
#     while 1:
#         cur_time = time.time()
#         if cur_time > end_time:
#             break

#         if cur_time >= (last_ctime + ci):
#             data = cpu_obj.get_data()
#             ts = cur_time
#             last_ctime=cur_time
#             for metric in data:
#                 mid=mids[metric]
#                 value=data[metric]
#                 collector.insert(mid, ts, value)

#         if cur_time >= (last_rtime + ri):
#             collector.report()
#             last_rtime=cur_time


## TESTING ##    
# proc_obj = Proc()
# cpu_obj = CPUInfo(proc=proc_obj)
# print "BLALALALAL"
# print "["
# for item in cpu_obj.get_data():
#     print "  ["
#     for it in item:
#         if isinstance(it, list):
#             print "    ["
#             for i in it:
#                 print i
#             print "    ]"
#         else:
#             print it
#     print "  ]"
# print "]"

# print "\n\n\n\n"
# cpudat= cpu_obj.get_data()
# for item in cpudat[0]:
#     print item

# proc_obj = Proc()
# gcpu_obj = CPUInfoGeneral(proc=proc_obj)
# print gcpu_obj.get_data()
# time.sleep(1)
# print gcpu_obj.get_data()
# time.sleep(1)
# print gcpu_obj.get_data()

