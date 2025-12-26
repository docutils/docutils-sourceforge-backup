#! /usr/bin/env python

"""
Author: David Goodger
Contact: dgoodger@bigfoot.com
Revision: $Revision: 1.1.1.1 $
Date: $Date: 2001/07/22 22:36:04 $
Copyright: This module has been placed in the public domain.

Test module for nodes.py.
"""

import unittest, sys, re
import nodes

debug = 0


class TextTests(unittest.TestCase):

    def setUp(self):
        self.text = nodes.Text('Line 1.\nLine 2.')

    def test_repr(self):
        self.assertEquals(repr(self.text), r"<#text: 'Line 1.\nLine 2.'>")

    def test_str(self):
        self.assertEquals(str(self.text), 'Line 1.\nLine 2.')

    def test_asdom(self):
        dom = self.text.asdom()
        self.assertEquals(dom.toxml(), 'Line 1.\nLine 2.')
        dom.unlink()

    def test_astext(self):
        self.assertEquals(self.text.astext(), 'Line 1.\nLine 2.')

    def test_pprint(self):
        self.assertEquals(self.text.pprint(), 'Line 1.\nLine 2.\n')


class ElementTests(unittest.TestCase):

    def test_empty(self):
        element = nodes._Element()
        self.assertEquals(repr(element), '<_Element: >')
        self.assertEquals(str(element), '<_Element/>')
        dom = element.asdom()
        self.assertEquals(dom.toxml(), '<_Element/>')
        dom.unlink()
        element['attr'] = '1'
        self.assertEquals(repr(element), '<_Element: >')
        self.assertEquals(str(element), '<_Element attr="1"/>')
        dom = element.asdom()
        self.assertEquals(dom.toxml(), '<_Element attr="1"/>')
        dom.unlink()
        self.assertEquals(element.pprint(), '<_Element attr="1"/>\n')

    def test_withtext(self):
        element = nodes._Element('text\nmore', nodes.Text('text\nmore'))
        self.assertEquals(repr(element), r"<_Element: <#text...>>")
        self.assertEquals(str(element), '<_Element>text\nmore</_Element>')
        dom = element.asdom()
        self.assertEquals(dom.toxml(), '<_Element>text\nmore</_Element>')
        dom.unlink()
        element['attr'] = '1'
        self.assertEquals(repr(element), r"<_Element: <#text...>>")
        self.assertEquals(str(element),
                          '<_Element attr="1">text\nmore</_Element>')
        dom = element.asdom()
        self.assertEquals(dom.toxml(),
                          '<_Element attr="1">text\nmore</_Element>')
        dom.unlink()
        self.assertEquals(element.pprint(),
"""\
<_Element attr="1">
    text
    more
</_Element>
""")


if __name__ == '__main__':
#    sys.argv.extend(['-v'])             # uncomment for verbose output
#    sys.argv.extend(['-v', '-d'])       # uncomment for very verbose output
    if sys.argv[-1] == '-d':
        debug = 1
        del sys.argv[-1]
    # When this module is executed from the command-line, run all its tests
    unittest.main()
