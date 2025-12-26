#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.6 $
:Date: $Date: 2002/04/13 16:59:29 $
:Copyright: This module has been placed in the public domain.

Tests for dps.transforms.references.Substitutions.
"""

import DPSTestSupport
from dps.transforms.references import Substitutions
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

totest['substitutions'] = ((Substitutions,), [
["""\
The |biohazard| symbol is deservedly scary-looking.

.. |biohazard| image:: biohazard.png
""",
"""\
<document>
    <paragraph>
        The 
        <image alt="biohazard" uri="biohazard.png">
         symbol is deservedly scary-looking.
    <substitution_definition name="biohazard">
        <image alt="biohazard" uri="biohazard.png">
"""],
["""\
Here's an |unknown| substitution.
""",
"""\
<document>
    <paragraph>
        Here's an 
        <problematic id="id2" refid="id1">
            |unknown|
         substitution.
    <system_message backrefs="id2" id="id1" level="3" type="ERROR">
        <paragraph>
            Undefined substitution referenced: "unknown".
"""],
])


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
