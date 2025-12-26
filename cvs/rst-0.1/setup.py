#!/usr/bin/env python
# $Id: setup.py,v 1.1 2001/06/01 20:45:34 David_Goodger Exp $

from distutils.core import setup

if __name__ == '__main__' :

    setup(name = 'restructuredtext',
          description = 'reStructuredText parser for Python DPS',
          #long_description = '',
          url = 'http://structuredtext.sf.net/',
          version = '0.1',
          author = 'David Goodger',
          author_email = 'dgoodger@bigfoot.com',
          license = '',
          packages = ['dps.parsers.restructuredtext'],
          package_dir = {'dps.parsers.restructuredtext': 'restructuredtext'})
