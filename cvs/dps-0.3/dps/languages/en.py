#! /usr/bin/env python
# $Id: en.py,v 1.1.1.1 2001/07/22 22:35:42 goodger Exp $
# by David Goodger (dgoodger@bigfoot.com)

"""
This module contains English-language mappings for language-dependent
features.
"""

__all__ = [parser, formatter]
__docformat__ = 'reStructuredText'


class Stuff:

    """Stores a bunch of stuff for dotted-attribute access."""

    def __init__(self, **keywordargs):
        self.__dict__.update(keywordargs)


parser = Stuff()
"""
Mappings for input parsers. Attributes:

- bibliofields: Field name (lowcased) to node class name mapping for
  bibliographic elements.
- authorseps: List of separator strings for 'Authors' fields, tried in order.
- interpreted: Interpreted text role name to node class name mapping.
- directives: Directive name to directive module name mapping.
"""

parser.bibliofields = {'title': 'title',
                       'author': 'author',
                       'authors': 'authors',
                       'organization': 'organization',
                       'contact': 'contact',
                       'version': 'version',
                       'revision': 'revision',
                       'status': 'status',
                       'date': 'date',
                       'copyright': 'copyright',}

parser.authorseps = [';', ',']

parser.interpreted = {'package': 'package',
                      'module': 'module',
                      'class': 'inline_class',
                      'method': 'method',
                      'function': 'function',
                      'variable': 'variable',
                      'parameter': 'parameter',
                      'type': 'type',
                      'class attribute': 'class_attribute',
                      'classatt': 'class_attribute',
                      'instance attribute': 'instance_attribute',
                      'instanceatt': 'instance_attribute',
                      'module attribute': 'module_attribute',
                      'moduleatt': 'module_attribute',
                      'exception class': 'exception_class',
                      'exception': 'exception_class',
                      'warning class': 'warning_class',
                      'warning': 'warning_class',}

parser.directives = {}

formatter = Stuff()
"""
Mappings for output formatters. Attributes:

- bibliolabels: Bibliographic node class name to label text mapping.
"""

formatter.bibliolabels = {'title': 'Title',
                          'author': 'Author',
                          'authors': 'Authors',
                          'organization': 'Organization',
                          'contact': 'Contact',
                          'version': 'Version',
                          'revision': 'Revision',
                          'status': 'Status',
                          'date': 'Date',
                          'copyright': 'Copyright',}
