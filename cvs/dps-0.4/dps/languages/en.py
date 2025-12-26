#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.10 $
:Date: $Date: 2002/03/16 06:09:23 $
:Copyright: This module has been placed in the public domain.

English-language mappings for language-dependent features of the Python
Docstring Processing System.
"""

__docformat__ = 'reStructuredText'

__all__ = ['labels', 'bibliographic_fields', 'author_separators']


from dps import nodes


labels = {
      'author': 'Author',
      'authors': 'Authors',
      'organization': 'Organization',
      'contact': 'Contact',
      'version': 'Version',
      'revision': 'Revision',
      'status': 'Status',
      'date': 'Date',
      'copyright': 'Copyright',
      'abstract': 'Abstract',
      'attention': 'Attention!',
      'caution': 'Caution!',
      'danger': '!DANGER!',
      'error': 'Error',
      'hint': 'Hint',
      'important': 'Important',
      'note': 'Note',
      'tip': 'Tip',
      'warning': 'Warning',
      'contents': 'Contents'}
"""Mapping of node class name to label text."""

bibliographic_fields = {
      'author': nodes.author,
      'authors': nodes.authors,
      'organization': nodes.organization,
      'contact': nodes.contact,
      'version': nodes.version,
      'revision': nodes.revision,
      'status': nodes.status,
      'date': nodes.date,
      'copyright': nodes.copyright,
      'abstract': nodes.topic}
"""Field name (lowcased) to node class name mapping for bibliographic fields
(field_list)."""

author_separators = [';', ',']
"""List of separator strings for the 'Authors' bibliographic field. Tried in
order."""
