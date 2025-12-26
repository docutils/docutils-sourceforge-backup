============================================
 README: Python Docstring Processing System
============================================

Author: David Goodger
Contact: dgoodger@bigfoot.com
Version: 0.3
Date: $Date: 2001/07/22 22:36:35 $
Web-site: http://docstring.sourceforge.net/

Thank you for downloading the Python Docstring Processing System
project arhive. As this is a work in progress, please check the
project web site for updated working files. The latest release archive
is available at http://sf.net/project/showfiles.php?group_id=26626.

To run the code, Python 2.0 or later must already be installed. You
can get Python from http://www.python.org/.


Archive Contents
================

* README.txt: You're reading it.

* HISTORY.txt: Release notes for the current and previous project
  releases.

* setup.py: Installation script. See "Installation" below.

* spec: The project specification directory. Contains PEPs (Python
  Enhancement Proposals) and XML DTDs (document type definitions)

* dps: The project source directory, installed as a Python package.


Installation
============

The first step is to expand the dps.0.3.tar.gz archive. It contains a
distutils setup file "setup.py". OS-specific installation instructions
follow.

Linux, Unix, MacOS X
--------------------

1. Open a shell.

2. Go to the directory created by expanding the archive::

       cd <archive_directory_path>

3. Install the package::

       python setup.py install

   If the python executable isn't on your path, you'll have to specify
   the complete path, such as /usr/local/bin/python. You may need root
   permissions to complete this step.

Windows
-------

1. Open a DOS box (Command Shell, MSDOS Prompt, or whatever they're
   calling it these days).

2. Go to the directory created by expanding the archive::

       cd <archive_directory_path>

3. Install the package::

       <path_to_python.exe>\python setup.py install

MacOS
-----

1. Open the folder containing the expanded archive.

2. Double-click on the file "setup.py", which should be a "Python
   module" file.

   If the file isn't a "Python module", the line endings are probably
   also wrong, and you will need to set up your system to recognize
   ".py" file extensions as Python files. See
   http://gotools.sf.net/mac/python.html for detailed instructions.
   Once set up, it's easiest to start over by expanding the archive
   again.

3. The distutils options window will appear. From the "Command" popup
   list choose "install", click "Add", then click "OK".


Usage
=====

The package modules are mostly in their infancy, continually growing
and evolving. The module evolution is being driven by the
reStructuredText parser project; see http://structuredtext.sf.net. The
dps.statemachine module is usable independently. It contains extensive
inline documentation (in reStructuredText format).

The specs, the package structure, and the skeleton modules may also be
of interest to you. Contributions are welcome!


Local Variables:
mode: indented-text
indent-tabs-mode: nil
fill-column: 70
End:
