"""
Python install/distribution script for BLiPP.
"""
try:
    from setuptools import setup
except:
    from distutils.core import setup
import os
import sys

VERSION = '0.1'

# snapshot pseudo-target
# -------------------
# Change VERSION to current date and svn
# revisionand then
# replace 'snapshot' with 'sdist' and continue.
#
if 'snapshot' in sys.argv:
    import time, subprocess, re
    date = time.strftime("%Y%m%d")
    proc = subprocess.Popen("svn update", stdout=subprocess.PIPE, shell=True)
    s = proc.stdout.readline()
    rev = re.search("revision (\d+)", s).group(1)
    VERSION = "%sr%s" % (date, rev)
    sys.argv[sys.argv.index('snapshot')] = 'sdist'

# Main function
# -------------

setup(name = "blipp",
      version=VERSION,
      packages = ["blipp"],
      ext_modules = [],
      package_data = {},
      scripts = ['bin/blippd', 'bin/xsp_server'],
      # metadata for upload to PyPI
      author = "Dan Gunter",
      author_email = "dkgunter@lbl.gov",
      maintainer = "Dan Gunter",
      maintainer_email = "dkgunter@lbl.gov",
      description = "Basic Lightweight Periscope Probe (BLiPP)",
      long_description = """Basic Lightweight Periscope Probe (BLiPP)""",
      license = "LGPL",
      keywords = "monitoring periscope netlogger",
      url = "http://TBD/",
      classifiers = [
        "Intended Audience :: Science/Research",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: System :: Monitoring",
        ],
      )
