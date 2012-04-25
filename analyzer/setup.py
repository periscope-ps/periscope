try:
    from setuptools import setup
except:
    from distutils.core import setup
from glob import glob
import os
import sys

VERSION = '1.0'

# Main function
# -------------

setup(name = "stampede-analyzer",
      version=VERSION,
      py_modules = ["db",
                  "main",
                    "util", ],
      ext_modules = [], #[ks_ext],
      install_requires=["pystache >= 0.4.1", "netlogger >= 4.3.0" ],
      # metadata for upload to PyPI
      author = "Dan Gunter",
      author_email = "dkgunter@lbl.gov",
      maintainer = "Dan Gunter",
      maintainer_email = "dkgunter@lbl.gov",
      description = "Stampede Analyzer",
      long_description = """The Stampede analyzer provides a dashboard to look at statistics generated by a Pegasus run.""",
      license = "LBNL. See www.lbl.gov/Disclaimers.html",
      classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Environment :: MacOS X",
        "Environment :: No Input/Output (Daemon)",
        "Intended Audience :: Science/Research",
        "Intended Audience :: System Administrators",
        "License :: Other/Proprietary License",
        "Natural Language :: English",
        "Operating System :: POSIX",
        "Programming Language :: Python",
        "Topic :: Database",
        "Topic :: System :: Logging",
        "Topic :: System :: Monitoring",
        ],
      )
