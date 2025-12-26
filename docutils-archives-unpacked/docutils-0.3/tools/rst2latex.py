#!/usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2003/02/24 14:20:02 $
:Copyright: This module has been placed in the public domain.

A minimal front end to the Docutils Publisher, producing HTML.
"""

#import locale
#locale.setlocale(locale.LC_ALL, '')

from docutils.core import publish_cmdline, default_description


description = ('Generates LaTeX documents from standalone reStructuredText '
			   'sources.  ' + default_description)

publish_cmdline(writer_name='latex', description=description)
