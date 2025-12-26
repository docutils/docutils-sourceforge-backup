#!/usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.2 $
:Date: $Date: 2002/07/25 01:55:21 $
:Copyright: This module has been placed in the public domain.

A minimal front end to the Docutils Publisher, producing HTML from PEP
(Python Enhancement Proposal) documents.
"""

import locale
locale.setlocale(locale.LC_ALL, '')

from docutils.core import publish, default_description


description = ('Generates (X)HTML from reStructuredText-format PEP files.  '
               + default_description)

publish(reader_name='pep', writer_name='pep_html', description=description)
