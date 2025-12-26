#! /usr/bin/env python
# $Id: model.py,v 1.1.1.1 2001/07/22 22:35:42 goodger Exp $
# by David Goodger (dgoodger@bigfoot.com)


class Parser:

    def __init__(self, warninglevel=1, errorlevel=3, language='en'):
        """Initialize the Parser instance."""
        self.warninglevel = warninglevel
        self.errorlevel = errorlevel
        self.language = language

    def parse(self, inputstring):
        """Return a document tree."""
        self.inputstring = inputstring
