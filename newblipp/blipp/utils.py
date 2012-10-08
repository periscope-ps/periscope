import os

def try__import__(name):
    try:
        ret=__import__(name)
    except ImportError as exp:
        SETTINGS_FILE = "blipp" + "." + name
        try:
            ret=__import__(SETTINGS_FILE)
            ret = getattr(ret, name)
        except ImportError as exp:
            ret=None
  
    return ret
