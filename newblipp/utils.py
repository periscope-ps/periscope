def try__import__(name):
    try:
        ret=__import__(name)
    except ImportError:
        ### LOG unable to import "name"
        ret=None
    return ret
