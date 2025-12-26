#!/usr/bin/env python
# $Id: setup.py,v 1.1.1.1 2001/07/22 22:36:35 goodger Exp $

from distutils.core import setup

if __name__ == '__main__' :

    setup(name = 'dps',
          description = 'Python Docstring Processing System',
          #long_description = '',
          url = 'http://docstring.sf.net/',
          version = '0.1',
          author = 'David Goodger',
          author_email = 'dgoodger@bigfoot.com',
          license = '',
          packages = ['dps', 'dps.parsers', 'dps.formatters',
                      'dps.languages'])
