#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.6 $
:Date: $Date: 2002/03/16 05:30:13 $
:Copyright: This module has been placed in the public domain.

Tests for reStructuredText.
"""

import RSTTestSupport

def suite():
    s = RSTTestSupport.ParserTestSuite()
    s.generateTests(totest)
    return s

totest = {}

# See RSTTestSupport.ParserTestSuite.generateTests for a description of the
# 'totest' data structure.
totest['transitions'] = [
["""\
Test transition markers.

--------

Paragraph
""",
"""\
<document>
    <paragraph>
        Test transition markers.
    <transition>
    <paragraph>
        Paragraph
"""],
["""\
Section 1
=========
First text division of section 1.

--------

Second text division of section 1.

Section 2
---------
Paragraph 2 in section 2.
""",
"""\
<document>
    <section id="section-1" name="section 1">
        <title>
            Section 1
        <paragraph>
            First text division of section 1.
        <transition>
        <paragraph>
            Second text division of section 1.
        <section id="section-2" name="section 2">
            <title>
                Section 2
            <paragraph>
                Paragraph 2 in section 2.
"""],
["""\
--------

A section or document may not begin with a transition.

The DTD specifies that two transitions may not
be adjacent:

--------

--------

--------

The DTD also specifies that a section or document
may not end with a transition.

--------
""",
"""\
<document>
    <system_message level="3" type="ERROR">
        <paragraph>
            Document or section may not begin with a transition (line 1).
    <transition>
    <paragraph>
        A section or document may not begin with a transition.
    <paragraph>
        The DTD specifies that two transitions may not
        be adjacent:
    <transition>
    <system_message level="3" type="ERROR">
        <paragraph>
            At least one body element must separate transitions; adjacent transitions at line 10.
    <transition>
    <system_message level="3" type="ERROR">
        <paragraph>
            At least one body element must separate transitions; adjacent transitions at line 12.
    <transition>
    <paragraph>
        The DTD also specifies that a section or document
        may not end with a transition.
    <transition>
    <system_message level="3" type="ERROR">
        <paragraph>
            Document or section may not end with a transition (line 17).
"""],
["""\
Test unexpected transition markers.

    Block quote.

    --------

    Paragraph.
""",
"""\
<document>
    <paragraph>
        Test unexpected transition markers.
    <block_quote>
        <paragraph>
            Block quote.
        <system_message level="4" type="SEVERE">
            <paragraph>
                Unexpected section title or transition at line 5.
            <literal_block>
                --------
        <paragraph>
            Paragraph.
"""],
]

if __name__ == '__main__':
    import unittest
    unittest.main(defaultTest='suite')
