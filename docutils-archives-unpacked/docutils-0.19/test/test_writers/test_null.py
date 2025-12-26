#!/usr/bin/env python3

# $Id: test_null.py 9037 2022-03-05 23:31:10Z milde $
# Author: Lea Wiemann <LeWiemann@gmail.com>
# Copyright: This module has been placed in the public domain.

"""
Test for Null writer.
"""

if __name__ == '__main__':
    import __init__  # noqa: F401
from test_writers import DocutilsTestSupport


def suite():
    s = DocutilsTestSupport.PublishTestSuite('null')
    s.generateTests(totest)
    return s


totest = {}

totest['basic'] = [
["""\
This is a paragraph.
""",
None]
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
