==========================
 README: reStructuredText
==========================

Author: David Goodger
Contact: dgoodger@bigfoot.com
Version: 0.1
Date: 2001-06-02
Website: http://structuredtext.sf.net

Thank you for downloading the reStructuredText project, version 0.1. This
version consists almost entirely of the specification. If you want to take a
look at the code (there isn't anything usable yet, just a skeleton), Python
must already be installed. You can get Python from http://www.python.org.

reStructuredText is an input parser component of the `Python Docstring
Processing System`_, ans is installed as "dps.parsers.restructuredtext".

.. _Python Docstring Processing System: http://docstring.sf.net

Installation
============

Since you're reading this file, you've probably already completed the first
step, which is to expand the rst-0.1.tar.gz archive. It contains a distutils
setup file "setup.py". OS-specific installation instructions follow.

Linux, Unix, MacOS X
--------------------

1. Open a shell.

2. Go to the directory created by expanding the archive::

       cd <archive_directory_path>

3. Install the package::

       python setup.py install

   If the python executable isn't on your path, you'll have to specify the
   complete path, such as /usr/local/bin/python. You may need root permissions
   to complete this step.

Windows
-------

1. Open a DOS box (Command Shell, MSDOS Prompt, or whatever they're calling it
   these days).

2. Go to the directory created by expanding the archive::

       cd <archive_directory_path>

3. Install the package::

       <path_to_python.exe>\python setup.py install

MacOS
-----

1. Open the folder containing the expanded archive.

2. Double-click on the file "setup.py", which should be a "Python module" file.

   If the file isn't a "Python module", the line endings are probably also
   wrong, and you will need to set up your system to recognize ".py" file
   extensions as Python files. See http://gotools.sf.net/mac/python.html for
   detailed instructions. Once set up, it's easiest to start over by expanding
   the archive again.

3. The distutils options window will appear. From the "Command" popup list
   choose "install", click "Add", then click "OK".
