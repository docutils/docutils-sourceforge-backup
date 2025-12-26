#!/usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.6 $
:Date: $Date: 2002/07/25 01:55:13 $
:Copyright: This module has been placed in the public domain.

A minimal front end to the Docutils Publisher, producing HTML.
"""

import locale
locale.setlocale(locale.LC_ALL, '')

from docutils.core import publish, default_description


description = ('Generates (X)HTML documents from standalone reStructuredText '
               'sources.  ' + default_description)

publish(writer_name='html', description=description)
