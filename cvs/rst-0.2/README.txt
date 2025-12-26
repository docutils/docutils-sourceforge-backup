==========================
 README: reStructuredText
==========================

Author: David Goodger
Contact: dgoodger@bigfoot.com
Version: 0.2
Date: $Date: 2001/06/18 23:34:03 $
Web-site: http://structuredtext.sf.net/

Thank you for downloading the reStructuredText project archive. As
this is a work in progress, please check the project web site for
updated working files. The latest release archive is available at
http://sf.net/project/showfiles.php?group_id=7050.

This version consists almost entirely of the specification. If you
want to take a look at the code (there isn't anything usable yet, just
a skeleton), Python must already be installed. You can get Python from
http://www.python.org/.

reStructuredText is an input parser component of the `Python Docstring
Processing System`_, ans is installed as
"dps.parsers.restructuredtext".

.. _Python Docstring Processing System: http://docstring.sf.net/


Archive Contents
================

* README.txt: You're reading it.

* HISTORY.txt: Release notes for the current and previous project
  releases.

* setup.py: Installation script. See "Installation" below.

* spec: The project specification directory.

* restructuredtext: The project source directory, installed as Python
  package ``dps.parsers.restructuredtext``.


Installation
============

The first step is to expand the rst-0.2.tar.gz archive. It contains a
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


Local Variables:
mode: indented-text
indent-tabs-mode: nil
fill-column: 70
End:
