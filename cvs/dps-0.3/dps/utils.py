#! /usr/bin/env python

"""
Author: David Goodger
Contact: dgoodger@bigfoot.com
Revision: $Revision: 1.1.1.1 $
Date: $Date: 2001/07/22 22:36:09 $
Copyright: This module has been placed in the public domain.

"""

import sys
import nodes


class SystemWarning(Exception):

    def __init__(self, system_warning):
        Exception.__init__(self, system_warning.astext())


class Errorist:

    def __init__(self, warninglevel, errorlevel, warningstream=sys.stderr):
        self.warninglevel = warninglevel
        self.errorlevel = errorlevel
        self.stream = warningstream

    def system_warning(self, level, comment=None, children=[]):
        """
        Return a system_warning object.

        Raise an exception or generate a warning if appropriate.
        """
        sw = nodes.system_warning(comment, level=level, *children)
        if level >= self.errorlevel:
            raise SystemWarning(sw)
        if level >= self.warninglevel:
            print >>self.stream, 'Warning:', sw.astext()
        return sw

    def strong_system_warning(self, admonition, comment, sourcetext=None):
        p = nodes.paragraph()
        p += nodes.strong('', admonition)
        p += nodes.Text(': ' + comment)
        children = [p]
        if sourcetext:
            children.append(nodes.literal_block('', sourcetext))
        return self.system_warning(3, children=children)
