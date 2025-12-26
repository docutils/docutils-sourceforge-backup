============================================
 README: Python Docstring Processing System
============================================

:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Date: $Date: 2002/04/19 01:45:36 $
:Web-site: http://docstring.sourceforge.net/

Thank you for downloading the Python Docstring Processing System
project arhive.  Development has been transferred to the Docutils_
project.  As this is a work in progress, please check the
project web site for updated working files.

To run the code, Python 2.0 or later must already be installed.  You
can get Python from http://www.python.org/.  You will also need the
latest reStructuredText package, available from
http://structuredtext.sourceforge.net/.

.. _Docutils: http://docutils.sourceforge.net/


Project Files & Directories
===========================

* README.txt: You're reading it.

* HISTORY.txt: Release notes for the current and previous project
  releases.

* setup.py: Installation script.  See "Installation" below.

* install.py: Quick & dirty installation script.

* dps: The project source directory, installed as a Python package.

* spec: The project specification directory.  Contains PEPs (Python
  Enhancement Proposals) and XML DTDs (document type definitions)


Installation
============

The first step is to expand the .tar.gz archive.  It contains a
distutils setup file "setup.py".  OS-specific installation
instructions follow.

Linux, Unix, MacOS X
--------------------

1. Open a shell.

2. Go to the directory created by expanding the archive::

       cd <archive_directory_path>

3. Install the package::

       python setup.py install

   If the python executable isn't on your path, you'll have to specify
   the complete path, such as /usr/local/bin/python.  You may need
   root permissions to complete this step.

You can also just run install.py; it does the same thing.

Windows
-------

1. Open a DOS box (Command Shell, MSDOS Prompt, or whatever they're
   calling it these days).

2. Go to the directory created by expanding the archive::

       cd <archive_directory_path>

3. Install the package::

       <path_to_python.exe>\python setup.py install

If your system is set up to run Python when you double-click on .py
files, you can run install.py to do the same as the above.

MacOS
-----

1. Open the folder containing the expanded archive.

2. Double-click on the file "setup.py", which should be a "Python
   module" file.

   If the file isn't a "Python module", the line endings are probably
   also wrong, and you will need to set up your system to recognize
   ".py" file extensions as Python files.  See
   http://gotools.sourceforge.net/mac/python.html for detailed
   instructions.  Once set up, it's easiest to start over by expanding
   the archive again.

3. The distutils options window will appear.  From the "Command" popup
   list choose "install", click "Add", then click "OK".

If install.py is a "Python module" (see step 2 above if it isn't), you
can run it instead of the above.  The distutils options window will
not appear.


Usage
=====

The package modules are mostly in their infancy, continually growing
and evolving.  The module evolution is being driven by the
reStructuredText parser project; see
http://structuredtext.sourceforge.net.  The dps.statemachine module is
usable independently.  It contains extensive inline documentation (in
reStructuredText format).

The specs, the package structure, and the skeleton modules may also be
of interest to you.  Contributions are welcome!


..
   Local Variables:
   mode: indented-text
   indent-tabs-mode: nil
   sentence-end-double-space: t
   fill-column: 70
   End:
