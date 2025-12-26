#! /usr/bin/env python3

# $Id: test_title.py 9037 2022-03-05 23:31:10Z milde $
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Tests for the 'title' directive.
"""

if __name__ == '__main__':
    import __init__  # noqa: F401
from test_parsers import DocutilsTestSupport


def suite():
    s = DocutilsTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s


totest = {}

totest['title'] = [
["""\
.. title:: This is the document title.
""",
"""\
<document source="test data" title="This is the document title.">
"""],
]


if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
