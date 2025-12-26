#! /usr/bin/env python

"""
Author: David Goodger
Contact: dgoodger@bigfoot.com
Revision: $Revision: 1.1.1.1 $
Date: $Date: 2001/07/21 22:14:13 $
Copyright: This module has been placed in the public domain.

Test module for states.py.
"""

import sys

class Tee:

    """Write to a file and a stream (default: stdout) simulteaneously."""
    
    def __init__(self, filename, stream=sys.__stdout__):
        self.file = open(filename, 'w')
        self.stream = stream
    
    def write(self, string):
        self.stream.write(string)
        self.file.write(string)

# redirect output to a common stream & a file
sys.stderr = sys.stdout = Tee('test_states.out')


import unittest, re, ndiff
import states
from dps.statemachine import string2lines
try:
    import mypdb as pdb
except:
    import pdb

debug = 0


class DataTests(unittest.TestCase):

    """
    Test data marked with 'XXX' denotes areas where further error checking
    needs to be done.
    """

    def setUp(self):
        self.sm = states.RSTStateMachine(stateclasses=states.stateclasses,
                                         initialstate='Body', debug=debug)

    def trytest(self, name, index):
        input, expected = self.totest[name][index]
        self.sm.run(string2lines(input), warninglevel=4,
                    errorlevel=4)
        output = self.sm.memo.document.pprint()
        try:
            self.assertEquals('\n' + output, '\n' + expected)
        except AssertionError:
            print
            print 'input:'
            print input
            print '-: output'
            print '+: expected'
            ndiff.lcompare(output.splitlines(1), expected.splitlines(1))
            raise

    totest = {}

    """Tests to be run. Each key (test type name) maps to a list of tests.
    Each test is a list: input, expected output, optional modifier. The
    optional third entry, a behavior modifier, can be 0 (temporarily disable
    this test) or 1 (run this test under the pdb debugger)."""
    
    proven = {}
    """tests that have proven successful"""

    notyet = {}
    """tests we *don't* want to run"""

    proven['paragraph'] = [
["""\
A paragraph.
""",
"""\
<document>
    <paragraph>
        A paragraph.
    </paragraph>
</document>
"""],
["""\
Paragraph 1.

Paragraph 2.
""",
"""\
<document>
    <paragraph>
        Paragraph 1.
    </paragraph>
    <paragraph>
        Paragraph 2.
    </paragraph>
</document>
"""],
["""\
Line 1.
Line 2.
Line 3.
""",
"""\
<document>
    <paragraph>
        Line 1.
        Line 2.
        Line 3.
    </paragraph>
</document>
"""],
["""\
Paragraph 1, Line 1.
Line 2.
Line 3.

Paragraph 2, Line 1.
Line 2.
Line 3.
""",
"""\
<document>
    <paragraph>
        Paragraph 1, Line 1.
        Line 2.
        Line 3.
    </paragraph>
    <paragraph>
        Paragraph 2, Line 1.
        Line 2.
        Line 3.
    </paragraph>
</document>
"""],
]

    proven['block_quote'] = [
["""\
Line 1.
Line 2.

   Indented.
""",
"""\
<document>
    <paragraph>
        Line 1.
        Line 2.
    </paragraph>
    <block_quote>
        <paragraph>
            Indented.
        </paragraph>
    </block_quote>
</document>
"""],
["""\
Line 1.
Line 2.

   Indented 1.

      Indented 2.
""",
"""\
<document>
    <paragraph>
        Line 1.
        Line 2.
    </paragraph>
    <block_quote>
        <paragraph>
            Indented 1.
        </paragraph>
        <block_quote>
            <paragraph>
                Indented 2.
            </paragraph>
        </block_quote>
    </block_quote>
</document>
"""],
["""\
Line 1.
Line 2.
   Indented.
""",
"""\
<document>
    <paragraph>
        Line 1.
        Line 2.
    </paragraph>
    <system_warning level="2">
        <paragraph>
            Unexpected indentation at line 3.
        </paragraph>
    </system_warning>
    <block_quote>
        <paragraph>
            Indented.
        </paragraph>
    </block_quote>
</document>
"""],
["""\
Line 1.
Line 2.

   Indented.
no blank line
""",
"""\
<document>
    <paragraph>
        Line 1.
        Line 2.
    </paragraph>
    <block_quote>
        <paragraph>
            Indented.
        </paragraph>
    </block_quote>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 5.
        </paragraph>
    </system_warning>
    <paragraph>
        no blank line
    </paragraph>
</document>
"""],
]

    proven['literal_block'] = [
["""\
A paragraph::

    A literal block.
""",
"""\
<document>
    <paragraph>
        A paragraph:
    </paragraph>
    <literal_block>
        A literal block.
    </literal_block>
</document>
"""],
["""\
A paragraph::
    A literal block without a blank line first.
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                A paragraph::
            </term>
            <definition>
                <system_warning level="2">
                    <paragraph>
                        Blank line missing before literal block? Interpreted as a definition list item. At line 2.
                    </paragraph>
                </system_warning>
                <paragraph>
                    A literal block without a blank line first.
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
</document>
"""],
["""\
A paragraph::

    A literal block.
no blank line
""",
"""\
<document>
    <paragraph>
        A paragraph:
    </paragraph>
    <literal_block>
        A literal block.
    </literal_block>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 4.
        </paragraph>
    </system_warning>
    <paragraph>
        no blank line
    </paragraph>
</document>
"""],
["""\
A paragraph: ::

    A literal block.
""",
"""\
<document>
    <paragraph>
        A paragraph:
    </paragraph>
    <literal_block>
        A literal block.
    </literal_block>
</document>
"""],
["""\
A paragraph:

::

    A literal block.
""",
"""\
<document>
    <paragraph>
        A paragraph:
    </paragraph>
    <literal_block>
        A literal block.
    </literal_block>
</document>
"""],
["""\
A paragraph::

Not a literal block.
""",
"""\
<document>
    <paragraph>
        A paragraph:
    </paragraph>
    <system_warning level="1">
        <paragraph>
            Literal block expected at line 2; none found.
        </paragraph>
    </system_warning>
    <paragraph>
        Not a literal block.
    </paragraph>
</document>
"""],
["""\
A paragraph::

    A literal block.
  Literal line 2.

    Literal line 3.
""",
"""\
<document>
    <paragraph>
        A paragraph:
    </paragraph>
    <literal_block>
          A literal block.
        Literal line 2.
        
          Literal line 3.
    </literal_block>
</document>
"""],
]

    proven['bullet_list'] = [
["""\
- item
""",
"""\
<document>
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item
            </paragraph>
        </list_item>
    </bullet_list>
</document>
"""],
["""\
* item 1

* item 2
""",
"""\
<document>
    <bullet_list bullet="*">
        <list_item>
            <paragraph>
                item 1
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                item 2
            </paragraph>
        </list_item>
    </bullet_list>
</document>
"""],
["""\
+ item 1
+ item 2
""",
"""\
<document>
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                item 1
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                item 2
            </paragraph>
        </list_item>
    </bullet_list>
</document>
"""],
["""\
- item 1, para 1.

  item 1, para 2.

- item 2
""",
"""\
<document>
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item 1, para 1.
            </paragraph>
            <paragraph>
                item 1, para 2.
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                item 2
            </paragraph>
        </list_item>
    </bullet_list>
</document>
"""],
["""\
- item 1, line 1
  item 1, line 2
- item 2
""",
"""\
<document>
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item 1, line 1
                item 1, line 2
            </paragraph>
        </list_item>
        <list_item>
            <paragraph>
                item 2
            </paragraph>
        </list_item>
    </bullet_list>
</document>
"""],
["""\
- item 1

+ item 2

* item 3
- item 4
""",
"""\
<document>
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item 1
            </paragraph>
        </list_item>
    </bullet_list>
    <bullet_list bullet="+">
        <list_item>
            <paragraph>
                item 2
            </paragraph>
        </list_item>
    </bullet_list>
    <bullet_list bullet="*">
        <list_item>
            <paragraph>
                item 3
            </paragraph>
        </list_item>
    </bullet_list>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 6.
        </paragraph>
    </system_warning>
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item 4
            </paragraph>
        </list_item>
    </bullet_list>
</document>
"""],
["""\
- item
no blank line
""",
"""\
<document>
    <bullet_list bullet="-">
        <list_item>
            <paragraph>
                item
            </paragraph>
        </list_item>
    </bullet_list>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 2.
        </paragraph>
    </system_warning>
    <paragraph>
        no blank line
    </paragraph>
</document>
"""],
["""\
- 

empty item
""",
"""\
<document>
    <bullet_list bullet="-">
        <list_item/>
    </bullet_list>
    <paragraph>
        empty item
    </paragraph>
</document>
"""],
["""\
-
empty item, no blank line, but no space after hyphen

XXX is this correct behavior?
""",
"""\
<document>
    <paragraph>
        -
        empty item, no blank line, but no space after hyphen
    </paragraph>
    <paragraph>
        XXX is this correct behavior?
    </paragraph>
</document>
"""],
]

    proven['definition_list'] = [
["""\
term
  definition
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                term
            </term>
            <definition>
                <paragraph>
                    definition
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
</document>
"""],
["""\
term
  definition
no blank line
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                term
            </term>
            <definition>
                <paragraph>
                    definition
                </paragraph>
                <system_warning level="1">
                    <paragraph>
                        Unindent without blank line at line 3.
                    </paragraph>
                </system_warning>
            </definition>
        </definition_list_item>
    </definition_list>
    <paragraph>
        no blank line
    </paragraph>
</document>
"""],
["""\
term 1
  definition 1

term 2
  definition 2
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                term 1
            </term>
            <definition>
                <paragraph>
                    definition 1
                </paragraph>
            </definition>
        </definition_list_item>
        <definition_list_item>
            <term>
                term 2
            </term>
            <definition>
                <paragraph>
                    definition 2
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
</document>
"""],
["""\
term 1
  definition 1 (no blank line below)
term 2
  definition 2
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                term 1
            </term>
            <definition>
                <paragraph>
                    definition 1 (no blank line below)
                </paragraph>
                <system_warning level="1">
                    <paragraph>
                        Unindent without blank line at line 3.
                    </paragraph>
                </system_warning>
            </definition>
        </definition_list_item>
        <definition_list_item>
            <term>
                term 2
            </term>
            <definition>
                <paragraph>
                    definition 2
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
</document>
"""],
["""\
term 1
  definition 1

  term 1a
    definition 1a

  term 1b
    definition 1b

term 2
  definition 2

paragraph
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                term 1
            </term>
            <definition>
                <paragraph>
                    definition 1
                </paragraph>
                <definition_list>
                    <definition_list_item>
                        <term>
                            term 1a
                        </term>
                        <definition>
                            <paragraph>
                                definition 1a
                            </paragraph>
                        </definition>
                    </definition_list_item>
                    <definition_list_item>
                        <term>
                            term 1b
                        </term>
                        <definition>
                            <paragraph>
                                definition 1b
                            </paragraph>
                        </definition>
                    </definition_list_item>
                </definition_list>
            </definition>
        </definition_list_item>
        <definition_list_item>
            <term>
                term 2
            </term>
            <definition>
                <paragraph>
                    definition 2
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
    <paragraph>
        paragraph
    </paragraph>
</document>
"""],
]

    proven['doctest_block'] = [
["""\
Paragraph.

>>> print "Doctest block."
Doctest block.

Paragraph.
""",
"""\
<document>
    <paragraph>
        Paragraph.
    </paragraph>
    <doctest_block>
        >>> print "Doctest block."
        Doctest block.
    </doctest_block>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
Paragraph.

>>> print "    Indented output."
    Indented output.
""",
"""\
<document>
    <paragraph>
        Paragraph.
    </paragraph>
    <doctest_block>
        >>> print "    Indented output."
            Indented output.
    </doctest_block>
</document>
"""],
["""\
Paragraph.

    >>> print "    Indented block & output."
        Indented block & output.
""",
"""\
<document>
    <paragraph>
        Paragraph.
    </paragraph>
    <block_quote>
        <doctest_block>
            >>> print "    Indented block & output."
                Indented block & output.
        </doctest_block>
    </block_quote>
</document>
"""],
]

    proven['section_header'] = [
["""\
Title
=====

Paragraph.
""",
"""\
<document>
    <section name="title">
        <title>
            Title
        </title>
        <paragraph>
            Paragraph.
        </paragraph>
    </section>
</document>
"""],
["""\
Paragraph.

    Title
    =====
    Paragraph.
""",
"""\
<document>
    <paragraph>
        Paragraph.
    </paragraph>
    <block_quote>
        <system_warning level="3">
            <paragraph>
                Unexpected section title at line 4.
            </paragraph>
        </system_warning>
        <paragraph>
            Paragraph.
        </paragraph>
    </block_quote>
</document>
"""],
["""\
Title
====

Paragraph.
""",
"""\
<document>
    <system_warning level="0">
        <paragraph>
            Title underline too short at line 2.
        </paragraph>
    </system_warning>
    <section name="title">
        <title>
            Title
        </title>
        <paragraph>
            Paragraph.
        </paragraph>
    </section>
</document>
"""],
["""\
=====
Title
=====

Paragraph.
""",
"""\
<document>
    <section name="title">
        <title>
            Title
        </title>
        <paragraph>
            Paragraph.
        </paragraph>
    </section>
</document>
"""],
["""\
=======
 Title
=======

Paragraph.
""",
"""\
<document>
    <section name="title">
        <title>
            Title
        </title>
        <paragraph>
            Paragraph.
        </paragraph>
    </section>
</document>
"""],
["""\
=======
 Title
""",
"""\
<document>
    <system_warning level="3">
        <paragraph>
            Incomplete section title at line 1.
        </paragraph>
    </system_warning>
    <system_warning level="3">
        <paragraph>
            Missing underline for overline at line 1.
        </paragraph>
    </system_warning>
</document>
"""],
["""\
=======
 Title

Paragraph
""",
"""\
<document>
    <system_warning level="3">
        <paragraph>
            Missing underline for overline at line 1.
        </paragraph>
    </system_warning>
    <paragraph>
        Paragraph
    </paragraph>
</document>
"""],
["""\
=======
 Long    Title
=======

Paragraph.
""",
"""\
<document>
    <system_warning level="0">
        <paragraph>
            Title overline too short at line 1.
        </paragraph>
    </system_warning>
    <section name="long title">
        <title>
            Long    Title
        </title>
        <paragraph>
            Paragraph.
        </paragraph>
    </section>
</document>
"""],
["""\
=======
 Title
-------

Paragraph.
""",
"""\
<document>
    <system_warning level="3">
        <paragraph>
            Title overline & underline mismatch at line 1.
        </paragraph>
    </system_warning>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
Title
=====
Paragraph.
""",
"""\
<document>
    <section name="title">
        <title>
            Title
        </title>
        <paragraph>
            Paragraph.
        </paragraph>
    </section>
</document>
"""],
["""\
Paragraph.

Title
=====

Paragraph.
""",
"""\
<document>
    <paragraph>
        Paragraph.
    </paragraph>
    <section name="title">
        <title>
            Title
        </title>
        <paragraph>
            Paragraph.
        </paragraph>
    </section>
</document>
"""],
["""\
Paragraph 1.

Title 1
=======
Paragraph 2.

Title 2
-------
Paragraph 3.

Title 3
=======
Paragraph 4.

Title 4
-------
Paragraph 5.
""",
"""\
<document>
    <paragraph>
        Paragraph 1.
    </paragraph>
    <section name="title 1">
        <title>
            Title 1
        </title>
        <paragraph>
            Paragraph 2.
        </paragraph>
        <section name="title 2">
            <title>
                Title 2
            </title>
            <paragraph>
                Paragraph 3.
            </paragraph>
        </section>
    </section>
    <section name="title 3">
        <title>
            Title 3
        </title>
        <paragraph>
            Paragraph 4.
        </paragraph>
        <section name="title 4">
            <title>
                Title 4
            </title>
            <paragraph>
                Paragraph 5.
            </paragraph>
        </section>
    </section>
</document>
"""],
["""\
Paragraph 1.

Title 1
=======
Paragraph 2.

Title 2
-------
Paragraph 3.

Title 3
```````
Paragraph 4.

Title 4
-------
Paragraph 5.
""",
"""\
<document>
    <paragraph>
        Paragraph 1.
    </paragraph>
    <section name="title 1">
        <title>
            Title 1
        </title>
        <paragraph>
            Paragraph 2.
        </paragraph>
        <section name="title 2">
            <title>
                Title 2
            </title>
            <paragraph>
                Paragraph 3.
            </paragraph>
            <section name="title 3">
                <title>
                    Title 3
                </title>
                <paragraph>
                    Paragraph 4.
                </paragraph>
            </section>
        </section>
        <section name="title 4">
            <title>
                Title 4
            </title>
            <paragraph>
                Paragraph 5.
            </paragraph>
        </section>
    </section>
</document>
"""],
["""\
Paragraph 1.

Title 1
=======
Paragraph 2.

Title 2
-------
Paragraph 3.

Title 3
=======
Paragraph 4.

Title 4
~~~~~~~
Paragraph 5.
""",
"""\
<document>
    <paragraph>
        Paragraph 1.
    </paragraph>
    <section name="title 1">
        <title>
            Title 1
        </title>
        <paragraph>
            Paragraph 2.
        </paragraph>
        <section name="title 2">
            <title>
                Title 2
            </title>
            <paragraph>
                Paragraph 3.
            </paragraph>
        </section>
    </section>
    <section name="title 3">
        <title>
            Title 3
        </title>
        <paragraph>
            Paragraph 4.
        </paragraph>
        <system_warning level="3">
            <paragraph>
                <strong>
                    ABORT
                </strong>
                : Title level inconsistent at line 15:
            </paragraph>
            <literal_block>
                Title 4
                ~~~~~~~
            </literal_block>
        </system_warning>
        <paragraph>
            Paragraph 5.
        </paragraph>
    </section>
</document>
"""],
["""\
Title
=====

Paragraph.

Title
=====

Paragraph.
""",
"""\
<document>
    <section>
        <title>
            Title
        </title>
        <paragraph>
            Paragraph.
        </paragraph>
    </section>
    <section>
        <title>
            Title
        </title>
        <system_warning level="0">
            <paragraph>
                duplicate implicit link name: "title"
            </paragraph>
        </system_warning>
        <paragraph>
            Paragraph.
        </paragraph>
    </section>
</document>
"""],
]

    proven['comment'] = [
["""\
.. A comment

Paragraph.
""",
"""\
<document>
    <comment>
        A comment
    </comment>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. A comment
   block.

Paragraph.
""",
"""\
<document>
    <comment>
        A comment
        block.
    </comment>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. A comment.
.. Another.

Paragraph.
""",
"""\
<document>
    <comment>
        A comment.
    </comment>
    <comment>
        Another.
    </comment>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. A comment
no blank line

Paragraph.
""",
"""\
<document>
    <comment>
        A comment
    </comment>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 2.
        </paragraph>
    </system_warning>
    <paragraph>
        no blank line
    </paragraph>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. A comment::

Paragraph.
""",
"""\
<document>
    <comment>
        A comment::
    </comment>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
term 1
  definition 1

  .. a comment

term 2
  definition 2
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                term 1
            </term>
            <definition>
                <paragraph>
                    definition 1
                </paragraph>
                <comment>
                    a comment
                </comment>
            </definition>
        </definition_list_item>
        <definition_list_item>
            <term>
                term 2
            </term>
            <definition>
                <paragraph>
                    definition 2
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
</document>
"""],
["""\
term 1
  definition 1

.. a comment

term 2
  definition 2
""",
"""\
<document>
    <definition_list>
        <definition_list_item>
            <term>
                term 1
            </term>
            <definition>
                <paragraph>
                    definition 1
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
    <comment>
        a comment
    </comment>
    <definition_list>
        <definition_list_item>
            <term>
                term 2
            </term>
            <definition>
                <paragraph>
                    definition 2
                </paragraph>
            </definition>
        </definition_list_item>
    </definition_list>
</document>
"""],
]

    proven['directive'] = [
["""\
.. directive::

Paragraph.
""",
"""\
<document>
    <directive type="directive"/>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. directive:: argument

Paragraph.
""",
"""\
<document>
    <directive data="argument" type="directive"/>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. directive::
   block

Paragraph.
""",
"""\
<document>
    <directive type="directive">
        <literal_block>
            block
        </literal_block>
    </directive>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. directive::

   block

Paragraph.
""",
"""\
<document>
    <directive type="directive">
        <literal_block>
            block
        </literal_block>
    </directive>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
["""\
.. directive::
   block
no blank line.

Paragraph.
""",
"""\
<document>
    <directive type="directive">
        <literal_block>
            block
        </literal_block>
    </directive>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 3.
        </paragraph>
    </system_warning>
    <paragraph>
        no blank line.
    </paragraph>
    <paragraph>
        Paragraph.
    </paragraph>
</document>
"""],
]

    proven['footnote'] = [
["""\
.. _[footnote] This is a footnote.
""",
"""\
<document>
    <footnote name="[footnote]">
        <label>
            footnote
        </label>
        <paragraph>
            This is a footnote.
        </paragraph>
    </footnote>
</document>
"""],
["""\
.. _[footnote] This is a footnote
   on multiple lines.
""",
"""\
<document>
    <footnote name="[footnote]">
        <label>
            footnote
        </label>
        <paragraph>
            This is a footnote
            on multiple lines.
        </paragraph>
    </footnote>
</document>
"""],
["""\
.. _[footnote] This is a footnote
     on multiple lines with more space.

.. _[footnote] This is a footnote
  on multiple lines with less space.
""",
"""\
<document>
    <footnote>
        <label>
            footnote
        </label>
        <paragraph>
            This is a footnote
            on multiple lines with more space.
        </paragraph>
    </footnote>
    <footnote>
        <label>
            footnote
        </label>
        <system_warning level="1">
            <paragraph>
                duplicate explicit link name: "[footnote]"
            </paragraph>
        </system_warning>
        <paragraph>
            This is a footnote
            on multiple lines with less space.
        </paragraph>
    </footnote>
</document>
"""],
["""\
.. _[footnote]
   This is a footnote on multiple lines
   whose block starts on line 2.
""",
"""\
<document>
    <footnote name="[footnote]">
        <label>
            footnote
        </label>
        <paragraph>
            This is a footnote on multiple lines
            whose block starts on line 2.
        </paragraph>
    </footnote>
</document>
"""],
["""\
.. _[footnote]

That was an empty footnote.
""",
"""\
<document>
    <footnote name="[footnote]">
        <label>
            footnote
        </label>
    </footnote>
    <paragraph>
        That was an empty footnote.
    </paragraph>
</document>
"""],
["""\
.. _[footnote]
No blank line.
""",
"""\
<document>
    <footnote name="[footnote]">
        <label>
            footnote
        </label>
    </footnote>
    <system_warning level="1">
        <paragraph>
            Unindent without blank line at line 2.
        </paragraph>
    </system_warning>
    <paragraph>
        No blank line.
    </paragraph>
</document>
"""],
]

    proven['target'] = [
["""\
.. _target:

(internal hyperlink)
""",
"""\
<document>
    <target name="target"/>
    <paragraph>
        (internal hyperlink)
    </paragraph>
</document>
"""],
["""\
.. _one-liner: http://structuredtext.sourceforge.net

.. _starts-on-this-line: http://
                         structuredtext.
                         sourceforge.net

.. _entirely-below:
   http://structuredtext.
   sourceforge.net
""",
"""\
<document>
    <target name="one-liner">
        http://structuredtext.sourceforge.net
    </target>
    <target name="starts-on-this-line">
        http://structuredtext.sourceforge.net
    </target>
    <target name="entirely-below">
        http://structuredtext.sourceforge.net
    </target>
</document>
"""],
["""\
.. _a long target name:

.. _`a target name: including a colon (quoted)`:

.. _a target name\: including a colon (escaped):
""",
"""\
<document>
    <target name="a long target name"/>
    <target name="a target name: including a colon (quoted)"/>
    <target name="a target name: including a colon (escaped)"/>
</document>
"""],
["""\
.. _target: http://www.python.org/

(indirect external hyperlink)
""",
"""\
<document>
    <target name="target">
        http://www.python.org/
    </target>
    <paragraph>
        (indirect external hyperlink)
    </paragraph>
</document>
"""],
["""\
.. _target: first

.. _target: second
""",
"""\
<document>
    <target name="target">
        first
    </target>
    <system_warning level="1">
        <paragraph>
            duplicate indirect link name: "target"
        </paragraph>
    </system_warning>
    <target name="target">
        second
    </target>
</document>
"""],
]

    proven['emphasis'] = [
["""\
*emphasis*
""",
"""\
<document>
    <paragraph>
        <emphasis>
            emphasis
        </emphasis>
    </paragraph>
</document>
"""],
["""\
*emphasized sentence
across lines*
""",
"""\
<document>
    <paragraph>
        <emphasis>
            emphasized sentence
            across lines
        </emphasis>
    </paragraph>
</document>
"""],
["""\
*emphasis
""",
"""\
<document>
    <paragraph>
        *emphasis
    </paragraph>
    <system_warning level="1">
        <paragraph>
            Inline emphasis start-string without end-string at line 1.
        </paragraph>
    </system_warning>
</document>
"""],
["""\
'*emphasis*' but not '*' or '"*"' or  x*2* or 2*x* or \\*args or *
or *the\\* *stars\\\\\\* *inside*

(however, '*args' will trigger a warning and may be problematic)

what about *this**?
""",
"""\
<document>
    <paragraph>
        '
        <emphasis>
            emphasis
        </emphasis>
        ' but not '*' or '"*"' or  x*2* or 2*x* or *args or *
        or 
        <emphasis>
            the* *stars\\* *inside
        </emphasis>
    </paragraph>
    <paragraph>
        (however, '*args' will trigger a warning and may be problematic)
    </paragraph>
    <system_warning level="1">
        <paragraph>
            Inline emphasis start-string without end-string at line 4.
        </paragraph>
    </system_warning>
    <paragraph>
        what about 
        <emphasis>
            this*
        </emphasis>
        ?
    </paragraph>
</document>
"""],
["""\
Emphasized asterisk: *\\**

Emphasized double asterisk: *\\***
""",
"""\
<document>
    <paragraph>
        Emphasized asterisk: 
        <emphasis>
            *
        </emphasis>
    </paragraph>
    <paragraph>
        Emphasized double asterisk: 
        <emphasis>
            **
        </emphasis>
    </paragraph>
</document>
"""],
]

    proven['strong'] = [
["""\
**strong**
""",
"""\
<document>
    <paragraph>
        <strong>
            strong
        </strong>
    </paragraph>
</document>
"""],
["""\
(**strong**) but not (**) or '(** ' or x**2 or \\**kwargs or **

(however, '**kwargs' will trigger a warning and may be problematic)
""",
"""\
<document>
    <paragraph>
        (
        <strong>
            strong
        </strong>
        ) but not (**) or '(** ' or x**2 or **kwargs or **
    </paragraph>
    <paragraph>
        (however, '**kwargs' will trigger a warning and may be problematic)
    </paragraph>
    <system_warning level="1">
        <paragraph>
            Inline strong start-string without end-string at line 3.
        </paragraph>
    </system_warning>
</document>
"""],
["""\
Strong asterisk: *****

Strong double asterisk: ******
""",
"""\
<document>
    <paragraph>
        Strong asterisk: 
        <strong>
            *
        </strong>
    </paragraph>
    <paragraph>
        Strong double asterisk: 
        <strong>
            **
        </strong>
    </paragraph>
</document>
"""],
]

    proven['literal'] = [
["""\
``literal``
""",
"""\
<document>
    <paragraph>
        <literal>
            literal
        </literal>
    </paragraph>
</document>
"""],
["""\
``\\literal``
""",
"""\
<document>
    <paragraph>
        <literal>
            \\literal
        </literal>
    </paragraph>
</document>
"""],
["""\
``lite\\ral``
""",
"""\
<document>
    <paragraph>
        <literal>
            lite\\ral
        </literal>
    </paragraph>
</document>
"""],
["""\
``literal\\``
""",
"""\
<document>
    <paragraph>
        <literal>
            literal\\
        </literal>
    </paragraph>
</document>
"""],
["""\
``literal ``TeX quotes'' & \\backslash`` but not "``" or ``

(however, ``standalone TeX quotes'' will trigger a warning
and may be problematic)
""",
"""\
<document>
    <paragraph>
        <literal>
            literal ``TeX quotes'' & \\backslash
        </literal>
         but not "``" or ``
    </paragraph>
    <paragraph>
        (however, ``standalone TeX quotes'' will trigger a warning
        and may be problematic)
    </paragraph>
    <system_warning level="1">
        <paragraph>
            Inline literal start-string without end-string at line 3.
        </paragraph>
    </system_warning>
</document>
"""],
["""\
Find the ```interpreted text``` in this paragraph!
""",
"""\
<document>
    <paragraph>
        Find the 
        <literal>
            `interpreted text`
        </literal>
         in this paragraph!
    </paragraph>
</document>
"""],
]

    proven['interpreted'] = [
["""\
`interpreted`
""",
"""\
<document>
    <paragraph>
        <interpreted>
            interpreted
        </interpreted>
    </paragraph>
</document>
"""],
["""\
`role: interpreted`
""",
"""\
<document>
    <paragraph>
        <interpreted role="role">
            interpreted
        </interpreted>
    </paragraph>
</document>
"""],
["""\
`interpreted :role`
""",
"""\
<document>
    <paragraph>
        <interpreted role="role">
            interpreted
        </interpreted>
    </paragraph>
</document>
"""],
["""\
`role\: escaped: interpreted`
""",
"""\
<document>
    <paragraph>
        <interpreted role="role: escaped">
            interpreted
        </interpreted>
    </paragraph>
</document>
"""],
["""\
`role: not escaped: interpreted`
""",
"""\
<document>
    <paragraph>
        <interpreted role="role">
            not escaped: interpreted
        </interpreted>
    </paragraph>
    <system_warning level="1">
        <paragraph>
            Multiple role-separators in interpreted text at line 1.
        </paragraph>
    </system_warning>
</document>
"""],
["""\
`interpreted` but not \\`interpreted` [`] or ({[`] or [`]}) or `
""",
"""\
<document>
    <paragraph>
        <interpreted>
            interpreted
        </interpreted>
         but not `interpreted` [`] or ({[`] or [`]}) or `
    </paragraph>
</document>
"""],
]

    proven['link'] = [
["""\
link_
""",
"""\
<document>
    <paragraph>
        <link refname="link">
            link
        </link>
    </paragraph>
</document>
"""],
["""\
link_, l_, and l_i-n_k_, but not _link_ or -link_ or link__
""",
"""\
<document>
    <paragraph>
        <link refname="link">
            link
        </link>
        , 
        <link refname="l">
            l
        </link>
        , and 
        <link refname="l_i-n_k">
            l_i-n_k
        </link>
        , but not _link_ or -link_ or link__
    </paragraph>
</document>
"""],
]

    proven['phrase_link'] = [
["""\
`phrase link`_
""",
"""\
<document>
    <paragraph>
        <link refname="phrase link">
            phrase link
        </link>
    </paragraph>
</document>
"""],
["""\
`phrase link
across lines`_
""",
"""\
<document>
    <paragraph>
        <link refname="phrase link across lines">
            phrase link
            across lines
        </link>
    </paragraph>
</document>
"""],
["""\
`phrase\`_ link`_
""",
"""\
<document>
    <paragraph>
        <link refname="phrase`_ link">
            phrase`_ link
        </link>
    </paragraph>
</document>
"""],
]

    proven['footnote_reference'] = [
["""\
[footnote]_
""",
"""\
<document>
    <paragraph>
        <footnote_reference refname="[footnote]">
            [footnote]
        </footnote_reference>
    </paragraph>
</document>
"""],
["""\
[footnote]_ and [foot-note]_ and [foot.note]_ and [1]_ but not [foot note]_
""",
"""\
<document>
    <paragraph>
        <footnote_reference refname="[footnote]">
            [footnote]
        </footnote_reference>
         and 
        <footnote_reference refname="[foot-note]">
            [foot-note]
        </footnote_reference>
         and 
        <footnote_reference refname="[foot.note]">
            [foot.note]
        </footnote_reference>
         and 
        <footnote_reference refname="[1]">
            [1]
        </footnote_reference>
         but not [foot note]_
    </paragraph>
</document>
"""],
]

    proven['standalone_hyperlink'] = [
["""\
http://www.standalone.hyperlink.com

mailto:someone@somewhere.com

someone@somewhere.com

ftp://ends.with.a.period.

(a.question.mark@end?)
""",
"""\
<document>
    <paragraph>
        <link refuri="http://www.standalone.hyperlink.com">
            http://www.standalone.hyperlink.com
        </link>
    </paragraph>
    <paragraph>
        <link refuri="mailto:someone@somewhere.com">
            mailto:someone@somewhere.com
        </link>
    </paragraph>
    <paragraph>
        <link refuri="mailto:someone@somewhere.com">
            someone@somewhere.com
        </link>
    </paragraph>
    <paragraph>
        <link refuri="ftp://ends.with.a.period">
            ftp://ends.with.a.period
        </link>
        .
    </paragraph>
    <paragraph>
        (
        <link refuri="mailto:a.question.mark@end">
            a.question.mark@end
        </link>
        ?)
    </paragraph>
</document>
"""],
]

    ''' # copy this for new entries:
    totest[''] = [
["""\
""",
"""\
"""],
]
    '''

    ## uncomment to run previously successful tests also
    totest.update(proven)

    ## uncomment to run previously successful tests *only*
    #totest = proven

    ## uncomment to run experimental, expected-to-fail tests also
    #totest.update(notyet)

    ## uncomment to run experimental, expected-to-fail tests *only*
    #totest = notyet

    for name, cases in totest.items():
        numcases = len(cases)
        casenumlen = len('%s' % (numcases - 1))
        for i in range(numcases):
            trace = ''
            if len(cases[i]) == 3:      # optional modifier
                if cases[i][-1] == 1:   # 1 => run under debugger
                    del cases[i][0]
                    trace = 'pdb.set_trace();'
                else:                   # 0 => disable
                    continue
            exec ('def test_%s_%0*i(self): %s self.trytest("%s", %i)'
                  % (name, casenumlen, i, trace, name, i))


class FuctionTests(unittest.TestCase):

    escaped = r'escapes: \*one, \\*two, \\\*three'
    nulled = 'escapes: \x00*one, \x00\\*two, \x00\\\x00*three'
    unescaped = r'escapes: *one, \*two, \*three'

    def test_escape2null(self):
        nulled = states.escape2null(self.escaped)
        self.assertEquals(nulled, self.nulled)
        nulled = states.escape2null(self.escaped + '\\')
        self.assertEquals(nulled, self.nulled + '\x00')

    def test_unescape(self):
        unescaped = states.unescape(self.nulled)
        self.assertEquals(unescaped, self.unescaped)
        restored = states.unescape(self.nulled, 1)
        self.assertEquals(restored, self.escaped)


if __name__ == '__main__':
#    sys.argv.extend(['-v'])             # uncomment for verbose output
#    sys.argv.extend(['-v', '-d'])       # uncomment for verbose debug output
    if sys.argv[-1] == '-d':
        debug = 1
        del sys.argv[-1]
    # When this module is executed from the command-line, run all its tests
    unittest.main()
