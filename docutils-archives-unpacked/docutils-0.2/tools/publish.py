#!/usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.6 $
:Date: $Date: 2002/07/25 01:55:34 $
:Copyright: This module has been placed in the public domain.

A minimal front end to the Docutils Publisher, producing pseudo-XML.
"""

import locale
locale.setlocale(locale.LC_ALL, '')

from docutils.core import publish, default_description


description = ('Generates pseudo-XML from standalone reStructuredText '
               'sources (for testing purposes).  ' + default_description)

publish(description=description)
