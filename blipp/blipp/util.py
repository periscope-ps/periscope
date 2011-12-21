"""
Utility functions
"""
__rcsid__ = "$Id: util.py 27069 2011-02-08 20:09:10Z dang $"
__author__ = "Dan Gunter (dkgunter (at) lbl.gov)"

# System imports
from asyncore import compact_traceback
import logging
import os
import signal
import sys

# Third-party imports
import bson
if hasattr(bson, 'dumps'):
    # standalone bson
    bson_encode = bson.dumps
    bson_decode = bson.loads
else:
    # pymongo's bson
    bson_encode = bson.BSON.encode
    bson_decode = bson.decode_all

## Classes and functions
## ---------------------

def handleSignals(*siglist):
    """Set up signal handlers.

    Input is a list of pairs of a function, and then a list of signals
    that should trigger that action, e.g.:
       handleSignals( (myfun1, (signal.SIGUSR1, signal.SIGUSR2)),
                      (myfun2, (signal.SIGTERM)) )
    """
    for action, signals in siglist:
        for signame in signals:
            if hasattr(signal, signame):
                signo = getattr(signal, signame)
                signal.signal(signo, action)

def traceback():
    """Traceback as a string with no newlines."""
    return str(compact_traceback())

def daemonize(log, root_log=None, close_fds=True):
    """Make current process into a daemon.
    """
    # Do a double-fork so that the daemon process is completely
    # detached from its parent (it becomes a child of init).
    # For details the classic text is: 
    # W. Richard Stevens, "Advanced Programming in the UNIX Environment"
    log.info("daemonize.start")
    log.debug("daemonize.fork1")
    try: 
        pid = os.fork() 
        if pid > 0:
            # parent: exit
            sys.exit(0) 
    except OSError, err: 
        log.exception( "fork.1.failed", err)
        sys.exit(1)
    log.debug("daemonize.fork2")
    # child: do second fork
    try: 
        pid = os.fork() 
        if pid > 0:
            # parent: exit
            sys.exit(0) 
    except OSError, err: 
        log.exc("daemonize.fork2.failed, msg=%s", str(err))
        sys.exit(1)
    # child: decouple from parent environment
    log.debug("daemonize.chdir_slash")
    os.chdir("/")
    try:
        os.setsid() 
    except OSError:
        pass
    os.umask(0)
    if close_fds:
        # Remove log handlers that write to stdout or stderr.
        # Construct list of other log handlers' file descriptors.
        no_close = [ ] # list of fd's to keep open
        if root_log and len(root_log.handlers) > 0:
            console = (sys.stderr.fileno(), sys.stdout.fileno())
            for handler in root_log.handlers[:]:
                fd = handler.stream.fileno()
                if fd in console:
                    log.removeHandler(handler)
                else:
                    no_close.append(fd)
        # Close all fd's except those that belong to non-console
        # log handlers, just discovered above.
        log.info("daemonize.close_fds, ignore=%s", ','.join(no_close))
        for fd in xrange(1024):
            if fd not in no_close:
                try:
                    os.close(fd)
                except OSError:
                    pass
    # redirect stdin, stdout, stderr to /dev/null
    log.info("daemonize.redirect")
    try:
        devnull = os.devnull
    except AttributeError:
        devnull = "/dev/null"
    os.open(devnull, os.O_RDWR)
    try:
        os.dup2(0, 1)
        os.dup2(0, 2)
    except OSError:
        pass
    log.info("daemonize.end")
