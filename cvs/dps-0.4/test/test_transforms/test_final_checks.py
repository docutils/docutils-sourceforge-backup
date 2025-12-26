#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.1 $
:Date: $Date: 2002/04/13 16:59:46 $
:Copyright: This module has been placed in the public domain.

Tests for dps.transforms.universal.FinalChecks.
"""

import DPSTestSupport
from dps.transforms.universal import FinalChecks
import UnitTestFolder
try:
    from restructuredtext import Parser
except ImportError:
    from dps.parsers.restructuredtext import Parser


def suite():
    parser = Parser()
    s = DPSTestSupport.TransformTestSuite(parser)
    s.generateTests(totest)
    return s

totest = {}

totest['final_checks'] = ((FinalChecks,), [
["""\
Unknown reference_.
""",
"""\
<document>
    <paragraph>
        Unknown 
        <problematic id="id2" refid="id1">
            reference_
        .
    <system_message backrefs="id2" id="id1" level="3" type="ERROR">
        <paragraph>
            Unknown target name: "reference".
"""],
])


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
