import resource
import os

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
    """Get memory statistics.
    """
    
    def __init__(self, **kwargs):
        self._proc = Proc(kwargs.get("proc_dir", "/proc/"))


    def get_data(self):
        bean_counts = self._proc.exists("user_beancounters")
        ans = {}
        if bean_counts:
            total=0
            used=0
            page_size_kb=resource.getpagesize()/1024
            for line in bean_counts:
                linel=line.split()
                if "kmemsize" in linel:
                    loc = linel.index("kmemsize")+1
                    ans.update({"kernel":int(linel[loc])/1024})
                elif "physpages" in linel:
                    loc = linel.index("physpages")+1
                    ans.update({"used":int(linel[loc])*page_size_kb})
                    used = int(linel[loc])*page_size_kb
                elif "vmguarpages" in linel:
                    loc = linel.index("vmguarpages")+3
                    total = int(linel[loc])
#                    # the "barrier" field of vmguarpages
#                    # is the number of pages that apps in
#                    # the vm are guaranteed to be able to
#                    # allocate, but the may be able to
#                    # allocate more depending on the amount
#                    # of physical memory available
            ans.update({"free":total-used})
        else:
            meminfo = self._proc.open("meminfo")
            for line in meminfo.readlines():
                linel=line.split()
                if linel[0].startswith("MemFree"):
                    ans.update({"free":int(linel[1])})
                    free=int(linel[1])
                elif linel[0].startswith("Buffers"):
                    ans.update({"buffer":int(linel[1])})
                elif linel[0].startswith("Cached"):
                    ans.update({"cache":int(linel[1])})
                elif linel[0].startswith("MemTotal"):
                    total=int(linel[1])
                elif linel[0].startswith("Slab"):
                    ans.update({"kernel":int(linel[1])})
            ans.update({"used":(total-free)})
        return ans
