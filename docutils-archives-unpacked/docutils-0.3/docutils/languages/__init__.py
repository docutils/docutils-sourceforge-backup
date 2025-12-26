# Author: David Goodger
# Contact: goodger@users.sourceforge.net
# Revision: $Revision: 1.4 $
# Date: $Date: 2002/10/09 00:51:44 $
# Copyright: This module has been placed in the public domain.

"""
This package contains modules for language-dependent features of Docutils.
"""

__docformat__ = 'reStructuredText'

_languages = {}

def get_language(language_code):
    if _languages.has_key(language_code):
        return _languages[language_code]
    module = __import__(language_code, globals(), locals())
    _languages[language_code] = module
    return module
