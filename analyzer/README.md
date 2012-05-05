# Stampede Web Workflow Analyzer

This is a web interface to workflow status and performance. It
operates on the [Pegasus](http://pegasus.usu.edu) 3.1 monitoring
database developed under the STAMPEDE project.

## Requirements

Below are the requirements for Python and Javascript.
 
## Python

[Python](http://python.org) 2.5 or above

NetLogger (this package) Python modules must be installed and in
your Python path, i.e. check out this code:

        svn co https://bosshog.lbl.gov/repos/netlogger/trunk nl-trunk
        cd nl-trunk/python
		python setup.py install

Then make sure the install directory is in your PYTHONPATH.

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

## Javascript

These are included in the source code:

* [mustache.js](http://github.com/janl/mustache.js) is an implementation of the [Mustache](http://mustache.github.com/) template system in JavaScript.
* [stringformat](www.masterdata.se/r/string_format_for_javascript/)
  - Help with some string formatting things.
* [Highcharts](http://www.highcharts.com/) - Plotting library

JQuery and JQUery-UI components must be downloaded.
There is an auto-install script install-jquery.sh.
Simply run it as:

        ./install-jquery.sh

If this does not work, you'll have to download and install manually:

* [jQuery](http://docs.jquery.com/Downloading_jQuery)
    JavaScript library for lots of things. You will need to do 
    a "save link as" on the latest current release.
    Then copy `jquery-*.*.*.min.js` to `static/js/jquery.min.js`

* jQuery UI is the official jQuery user interface library.  Go to
  http://jqueryui.com/download, click on "Deselect all" on the Effects, and
  then download the library.

  After unzipping, copy `js/jquery-ui-*.*.*.custom.min.js` to
  `static/js/jquery-ui.custom.min.js`.  Copy css/ui-lightness to 
  static/css/ui-lightness.

## Testing

The tests are written using [nose](http://readthedocs.org/docs/nose/en/latest/)
and [paste](http://pythonpaste.org/), and live in the "test" subdirectory.

Running the tests is as easy as a single command: `nosetests`

## Running

To run directly from the commandline, type: `./stampede-dashboard`.
This simply runs the main.py code.
Then navigate to the [local web URL](http://0.0.0.0:8080/).

