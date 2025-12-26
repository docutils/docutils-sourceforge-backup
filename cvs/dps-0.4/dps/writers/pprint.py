#! /usr/bin/env python

"""
:Authors: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.3 $
:Date: $Date: 2002/02/12 02:13:51 $
:Copyright: This module has been placed in the public domain.

Simple internal document tree Writer, writes indented pseudo-XML.
"""

__docformat__ = 'reStructuredText'

__all__ = ['Writer']


from dps import writers


class Writer(writers.Writer):

    output = None
    """Final translated form of `document`."""

    def translate(self):
        self.output = self.document.pformat()

    def record(self):
        self.recordfile(self.output, self.destination)
