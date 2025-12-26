#! /usr/bin/env python

"""
:Authors: Garth Kidd, David Goodger
:Contact: garth@deadlybloodyserious.com
:Revision: $Revision: 1.13 $
:Date: $Date: 2002/04/19 02:37:35 $
:Copyright: This module has been placed in the public domain.

Exports the following:

:Modules:
    Try to import modules from the current working copy of restructuredtext
    first, or from the installed version. In test modules, import these modules
    from here:

    - `states` is 'restructuredtext.states'
    - `tableparser` is 'restructuredtext.tableparser'

:Classes:
    - `CustomTestSuite`
    - `CustomTestCase`
    - `ParserTestSuite`
    - `ParserTestCase`
    - `TableParserTestSuite`
    - `TableParserTestCase`
"""
__docformat__ = 'reStructuredText'

import UnitTestFolder
import sys, os, unittest, re, difflib, types, inspect
from pprint import pformat
from dps.parsers import restructuredtext
from dps.parsers.restructuredtext import states, tableparser, directives, \
      languages
from dps.statemachine import string2lines
import dps.utils

try:
    import mypdb as pdb
except:
    import pdb


class CustomTestSuite(unittest.TestSuite):

    """
    A collection of custom TestCases.

    """

    id = ''
    """Identifier for the TestSuite. Prepended to the
    TestCase identifiers to make identification easier."""

    nextTestCaseId = 0
    """The next identifier to use for non-identified test cases."""

    def __init__(self, tests=(), id=None):
        """Initialise the CustomTestSuite.

        Arguments:

        id -- identifier for the suite, prepended to test cases.
        """
        unittest.TestSuite.__init__(self, tests)
        if id is None:
            outerframes = inspect.getouterframes(inspect.currentframe())
            mypath = outerframes[0][1]
            callerpath = outerframes[1][1]
            mydir, myname = os.path.split(mypath)
            if not mydir:
                mydir = os.curdir
            if callerpath.startswith(mydir):
                self.id = callerpath[len(mydir) + 1:] # caller's module
            else:
                self.id = callerpath
        else:
            self.id = id

    def addTestCase(self, testCaseClass, methodName, input, expected,
                    id=None, runInDebugger=0, shortDescription=None):
        """
        Create a custom TestCase in the CustomTestSuite.
        Also returns it, just in case.

        Arguments:

        testCaseClass --
        methodName --
        input -- input to the parser.
        expected -- expected output from the parser.
        id -- unique test identifier, used by the test framework.
        runInDebugger -- if true, run this test under the pdb debugger.
        shortDescription -- override to default test description.
        """
        # generate id if required
        if id is None:
            id = self.nextTestCaseId
            self.nextTestCaseId += 1

        # test identifier will become suiteid.testid
        tcid = '%s: %s' % (self.id, id)

        # generate and add test case
        tc = testCaseClass(methodName, input, expected, tcid,
                             runInDebugger=runInDebugger,
                             shortDescription=shortDescription)
        self.addTest(tc)
        return tc


class CustomTestCase(unittest.TestCase):

    compare = difflib.Differ().compare
    """Comparison method shared by all subclasses."""

    def __init__(self, methodName, input, expected, id,
                 runInDebugger=0, shortDescription=None):
        """
        Initialise the CustomTestCase.

        Arguments:

        methodName -- name of test method to run.
        input -- input to the parser.
        expected -- expected output from the parser.
        id -- unique test identifier, used by the test framework.
        runInDebugger -- if true, run this test under the pdb debugger.
        shortDescription -- override to default test description.
        """
        self.id = id
        self.input = input
        self.expected = expected
        self.runInDebugger = runInDebugger
        # Ring your mother.
        unittest.TestCase.__init__(self, methodName)

    def __str__(self):
        """
        Return string conversion. Overridden to give test id, in addition to
        method name.
        """
        return '%s; %s' % (self.id, unittest.TestCase.__str__(self))

    def compareOutput(self, input, output, expected):
        """`input`, `output`, and `expected` should all be strings."""
        try:
            self.assertEquals('\n' + output, '\n' + expected)
        except AssertionError:
            print >>sys.stderr, '\n%s\ninput:' % (self,)
            print >>sys.stderr, input
            print >>sys.stderr, '-: expected\n+: output'
            print >>sys.stderr, ''.join(self.compare(expected.splitlines(1),
                                                     output.splitlines(1)))
            raise


class ParserTestSuite(CustomTestSuite):

    """
    A collection of ParserTestCases.

    A ParserTestSuite instance manufactures ParserTestCases,
    keeps track of them, and provides a shared test fixture (a-la
    setUp and tearDown).
    """

    def generateTests(self, dict, dictname='totest'):
        """
        Stock the suite with test cases generated from a test data dictionary.

        Each dictionary key (test type name) maps to a list of tests. Each
        test is a list: input, expected output, optional modifier. The
        optional third entry, a behavior modifier, can be 0 (temporarily
        disable this test) or 1 (run this test under the pdb debugger). Tests
        should be self-documenting and not require external comments.
        """
        for name, cases in dict.items():
            casenum = 0
            for casenum in range(len(cases)):
                case = cases[casenum]
                runInDebugger = 0
                if len(case)==3:
                    if case[2]:
                        runInDebugger = 1
                    else:
                        continue
                self.addTestCase(ParserTestCase, 'test_parser',
                                 input=case[0], expected=case[1],
                                 id='%s[%r][%s]' % (dictname, name, casenum),
                                 runInDebugger=runInDebugger)


class ParserTestCase(CustomTestCase):

    """
    Output checker for the parser.

    Should probably be called ParserOutputChecker, but I can deal with
    that later when/if someone comes up with a category of parser test
    cases that have nothing to do with the input and output of the parser.
    """

    parser = restructuredtext.Parser()
    """restructuredtext.Parser shared by all ParserTestCases."""

    def test_parser(self):
        if self.runInDebugger:
            pdb.set_trace()
        document = dps.utils.newdocument(warninglevel=5, errorlevel=5,
                                         debug=UnitTestFolder.debug)
        self.parser.parse(self.input, document)
        output = document.pformat()
        self.compareOutput(self.input, output, self.expected)


class TableParserTestSuite(CustomTestSuite):

    """
    A collection of TableParserTestCases.

    A TableParserTestSuite instance manufactures TableParserTestCases,
    keeps track of them, and provides a shared test fixture (a-la
    setUp and tearDown).
    """

    def generateTests(self, dict, dictname='totest'):
        """
        Stock the suite with test cases generated from a test data dictionary.

        Each dictionary key (test type name) maps to a list of tests. Each
        test is a list: an input table, expected output from parsegrid(),
        expected output from parse(), optional modifier. The optional fourth
        entry, a behavior modifier, can be 0 (temporarily disable this test)
        or 1 (run this test under the pdb debugger). Tests should be
        self-documenting and not require external comments.
        """
        for name, cases in dict.items():
            for casenum in range(len(cases)):
                case = cases[casenum]
                runInDebugger = 0
                if len(case) == 4:
                    if case[3]:
                        runInDebugger = 1
                    else:
                        continue
                self.addTestCase(TableParserTestCase, 'test_parsegrid',
                                 input=case[0], expected=case[1],
                                 id='%s[%r][%s]' % (dictname, name, casenum),
                                 runInDebugger=runInDebugger)
                self.addTestCase(TableParserTestCase, 'test_parse',
                                 input=case[0], expected=case[2],
                                 id='%s[%r][%s]' % (dictname, name, casenum),
                                 runInDebugger=runInDebugger)


class TableParserTestCase(CustomTestCase):

    parser = tableparser.TableParser()

    def test_parsegrid(self):
        self.parser.setup(string2lines(self.input))
        try:
            self.parser.findheadbodysep()
            self.parser.parsegrid()
            output = self.parser.cells
        except Exception, details:
            output = '%s: %s' % (details.__class__.__name__, details)
        self.compareOutput(self.input, pformat(output) + '\n',
                           pformat(self.expected) + '\n')

    def test_parse(self):
        try:
            output = self.parser.parse(string2lines(self.input))
        except Exception, details:
            output = '%s: %s' % (details.__class__.__name__, details)
        self.compareOutput(self.input, pformat(output) + '\n',
                           pformat(self.expected) + '\n')
