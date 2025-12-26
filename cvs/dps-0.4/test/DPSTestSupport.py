#! /usr/bin/env python
"""
:Authors:  David Goodger; Garth Kidd
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.10 $
:Date: $Date: 2002/04/19 02:36:49 $
:Copyright: This module has been placed in the public domain.

Exports the following:

:Modules:
    Try to import modules from the current working copy of dps first,
    or from the installed version. In test modules, import these
    modules from here:

    - `statemachine` is 'dps.statemachine'
    - `nodes` is 'dps.nodes'
    - `urischemes` is 'dps.urischemes'
    - `utils` is 'dps.utils'
    - `transforms` is 'dps.transforms'
"""
__docformat__ = 'reStructuredText'

import UnitTestFolder
import sys, os
import unittest, difflib, inspect, os, sys
import dps                              # or restructuredtext on path?
from dps import statemachine, nodes, urischemes, utils, transforms
from dps.transforms import universal

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
        """
        Initialize the CustomTestSuite.

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
                    id=None, runInDebugger=0, shortDescription=None,
                    **kwargs):
        """
        Create a custom TestCase in the CustomTestSuite.
        Also return it, just in case.

        Arguments:

        testCaseClass --
        methodName --
        input -- input to the parser.
        expected -- expected output from the parser.
        id -- unique test identifier, used by the test framework.
        runInDebugger -- if true, run this test under the pdb debugger.
        shortDescription -- override to default test description.
        """
        if id is None:                  # generate id if required
            id = self.nextTestCaseId
            self.nextTestCaseId += 1
        # test identifier will become suiteid.testid
        tcid = '%s: %s' % (self.id, id)
        # generate and add test case
        tc = testCaseClass(methodName, input, expected, tcid,
                           runInDebugger=runInDebugger,
                           shortDescription=shortDescription,
                           **kwargs)
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


class TransformTestSuite(CustomTestSuite):

    """
    A collection of TransformTestCases.

    A TransformTestSuite instance manufactures TransformTestCases,
    keeps track of them, and provides a shared test fixture (a-la
    setUp and tearDown).
    """

    def __init__(self, parser):
        self.parser = parser
        """Parser shared by all test cases."""

        CustomTestSuite.__init__(self)

    def generateTests(self, dict, dictname='totest',
                      testmethod='test_transforms'):
        """
        Stock the suite with test cases generated from a test data dictionary.

        Each dictionary key (test type's name) maps to a list of transform
        classes and list of tests. Each test is a list: input, expected
        output, optional modifier. The optional third entry, a behavior
        modifier, can be 0 (temporarily disable this test) or 1 (run this test
        under the pdb debugger). Tests should be self-documenting and not
        require external comments.
        """
        for name, (transforms, cases) in dict.items():
            for casenum in range(len(cases)):
                case = cases[casenum]
                runInDebugger = 0
                if len(case)==3:
                    if case[2]:
                        runInDebugger = 1
                    else:
                        continue
                self.addTestCase(
                      TransformTestCase, testmethod,
                      transforms=transforms, parser=self.parser,
                      input=case[0], expected=case[1],
                      id='%s[%r][%s]' % (dictname, name, casenum),
                      runInDebugger=runInDebugger)


class TransformTestCase(CustomTestCase):

    """
    Output checker for the transform.

    Should probably be called TransformOutputChecker, but I can deal with
    that later when/if someone comes up with a category of transform test
    cases that have nothing to do with the input and output of the transform.
    """

    def __init__(self, *args, **kwargs):
        self.transforms = kwargs['transforms']
        """List of transforms to perform for this test case."""

        self.parser = kwargs['parser']
        """Input parser for this test case."""

        del kwargs['transforms'], kwargs['parser'] # only wanted here
        CustomTestCase.__init__(self, *args, **kwargs)

    def test_transforms(self):
        if self.runInDebugger:
            pdb.set_trace()
        doctree = utils.newdocument(warninglevel=5, errorlevel=5,
                                    debug=UnitTestFolder.debug)
        self.parser.parse(self.input, doctree)
        for transformClass in (self.transforms + universal.test_transforms):
            transformClass(doctree).transform()
        output = doctree.pformat()
        self.compareOutput(self.input, output, self.expected)

    def test_transforms_verbosely(self):
        if self.runInDebugger:
            pdb.set_trace()
        print '\n', self.id
        print '-' * 70
        print self.input
        doctree = utils.newdocument(warninglevel=5, errorlevel=5,
                                    debug=UnitTestFolder.debug)
        self.parser.parse(self.input, doctree)
        print '-' * 70
        print doctree.pformat()
        for transformClass in self.transforms:
            transformClass(doctree).transform()
        output = doctree.pformat()
        print '-' * 70
        print output
        self.compareOutput(self.input, output, self.expected)
