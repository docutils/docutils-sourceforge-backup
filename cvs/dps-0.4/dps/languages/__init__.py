#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2002/02/06 02:42:18 $
:Copyright: This module has been placed in the public domain.

This package contains modules for language-dependent features of
the Python Docstring Processing System.
"""

__docformat__ = 'reStructuredText'

__all__ = ['getlanguage']

_languages = {}

def getlanguage(languagecode):
    if _languages.has_key(languagecode):
        return _languages[languagecode]
    module = __import__(languagecode, globals(), locals())
    _languages[languagecode] = module
    return module
