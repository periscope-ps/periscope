# Stampede Web Workflow Analyzer

This is a web interface to workflow status and performance. It
operates on the [Pegasus](http://pegasus.usu.edu) 3.1 monitoring
database developed under the STAMPEDE project.
 
## Installation

### Installing NetLogger

NetLogger (this package) Python modules must be installed and in
your Python path, i.e. check out this code:

        svn co https://bosshog.lbl.gov/repos/netlogger/trunk nl-trunk
        cd nl-trunk/python
		python setup.py install

Then make sure the install directory is in your PYTHONPATH.

### Requirements

#### Base

[Python](http://python.org) 2.5 or above

#### External Python modules

We recommend installing Python modules using
[pip](http://pypi.python.org/pypi/pip), which is a replacement for
[easy_install](http://peak.telecommunity.com/DevCenter/EasyInstall).

* Modules:
  + SQLAlchemy
  + web.py
* For testing:
  + mock
  + nose
  + paste

Install specific versions by typing `python setup.py install` from inside the
directories for these:

* lib/pystache - pystache template tool

#### Javascript modules

These are included in the source code:

* [jQuery](http://jquery.com) - JavaScript library for lots of things.
* [mustache.js](http://github.com/janl/mustache.js) is an implementation of the [Mustache](http://mustache.github.com/) template system in JavaScript.
* [stringformat](www.masterdata.se/r/string_format_for_javascript/)
  - Help with some string formatting things.
* [JQplot](http://www.jqplot.com/) - Plotting library

## Running

The main module is called by convention __main.py__.

To run this directly from the commandline, type: `python main.py`.
Then navigate to the [local web URL](http://0.0.0.0:8080/).

### Testing

The tests are written using [nose](http://readthedocs.org/docs/nose/en/latest/)
and [paste](http://pythonpaste.org/), and live in the "test" subdirectory.

Running the tests is as easy as a single command: `nosetests`



