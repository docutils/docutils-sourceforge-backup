#! /usr/bin/env python
# $Id: test_statemachine.py,v 1.9 2001/06/01 20:53:53 David_Goodger Exp $
# by David Goodger (dgoodger@bigfoot.com)

import unittest, sys, re
from statemachine import *


debug = 0
testtext = string2lines("""\
First paragraph.

- This is a bullet list. First list item.
  Second line of first para.

  Second para.

      block quote

- Second list item. Example::

        a
      literal
           block

Last paragraph.""")
expected = ('StateMachine1 text1 blank1 bullet1 knownindent1 '
            'StateMachine2 text2 text2 blank2 text2 blank2 indent2 '
            'StateMachine3 text3 blank3 finished3 finished2 '
            'bullet1 knownindent1 '
            'StateMachine2 text2 blank2 literalblock2(4) finished2 '
            'text1 finished1').split()
para1 = testtext[:2]
item1 = [line[2:] for line in testtext[2:9]]
item2 = [line[2:] for line in testtext[9:-1]]
lbindent = 6
literalblock = [line[lbindent:] for line in testtext[11:-1]]
para2 = testtext[-1]


class MockState(StateWS):

    patterns = {'bullet': re.compile(r'- '),
                'text': re.compile('.')}
    initialtransitions = [['bullet'], ['text']]
    levelholder = [0]

    def bof(self, context):
        self.levelholder[0] += 1
        self.level = self.levelholder[0]
        if self.debug: print >>sys.stderr, 'StateMachine%s' % self.level
        return [], ['StateMachine%s' % self.level]

    def blank(self, match, context, nextstate):
        result = ['blank%s' % self.level]
        if self.debug: print >>sys.stderr, 'blank%s' % self.level
        if context and context[-1] and context[-1][-2:] == '::':
            result.extend(self.literalblock())
        return [], None, result

    def indent(self, match, context, nextstate):
        if self.debug: print >>sys.stderr, 'indent%s' % self.level
        context, nextstate, result = StateWS.indent(self, match, context,
                                                    nextstate)
        return context, nextstate, ['indent%s' % self.level] + result

    def knownindent(self, match, context, nextstate):
        if self.debug: print >>sys.stderr, 'knownindent%s' % self.level
        context, nextstate, result = StateWS.knownindent(self, match, context,
                                                         nextstate)
        return context, nextstate, ['knownindent%s' % self.level] + result

    def bullet(self, match, context, nextstate):
        if self.debug: print >>sys.stderr, 'bullet%s' % self.level
        context, nextstate, result \
              = self.knownindent(match, context, nextstate)
        return [], nextstate, ['bullet%s' % self.level] + result

    def text(self, match, context, nextstate):
        if self.debug: print >>sys.stderr, 'text%s' % self.level
        return [match.string], nextstate, ['text%s' % self.level]

    def literalblock(self):
        indented, indent, offset = self.statemachine.getindented()
        if self.debug: print >>sys.stderr, 'literalblock%s(%s)' % (self.level,
                                                                   indent)
        return ['literalblock%s(%s)' % (self.level, indent)]

    def eof(self, context):
        self.levelholder[0] -= 1
        if self.debug: print >>sys.stderr, 'finished%s' % self.level
        return ['finished%s' % self.level]


class EmptySMTestCase(unittest.TestCase):

    def setUp(self):
        self.sm = StateMachine(stateclasses=[], initialstate='State',
                               debug=debug)

    def test_addstate(self):
        self.sm.addstate(State)
        self.assert_(len(self.sm.states) == 1)
        self.assertRaises(DuplicateStateError, self.sm.addstate,
                          State)
        self.sm.addstate(StateWS)
        self.assert_(len(self.sm.states) == 2)

    def test_addstates(self):
        self.sm.addstates((State, StateWS))
        self.assertEqual(len(self.sm.states), 2)

    def test_getstate(self):
        self.assertRaises(UnknownStateError, self.sm.getstate)
        self.sm.addstates((State, StateWS))
        self.assertRaises(UnknownStateError, self.sm.getstate, 'unknownState')
        self.assert_(isinstance(self.sm.getstate('State'), State))
        self.assert_(isinstance(self.sm.getstate('StateWS'), State))
        self.assertEqual(self.sm.currentstate, 'StateWS')


class EmptySMWSTestCase(EmptySMTestCase):

    def setUp(self):
        self.sm = StateMachineWS(stateclasses=[], initialstate='State',
                                 debug=debug)


class SMWSTestCase(unittest.TestCase):

    def setUp(self):
        self.sm = StateMachineWS([MockState], 'MockState', debug=debug)
        self.sm.states['MockState'].levelholder[0] = 0

    def test___init__(self):
        self.assertEquals(self.sm.states.keys(), ['MockState'])
        self.assertEquals(len(self.sm.states['MockState'].transitions), 2)

    def test_getindented(self):
        self.sm.inputlines = testtext
        self.sm.nextline(3)
        indented, offset = self.sm.getknownindented(2)
        self.assertEquals(indented, item1)
        self.assertEquals(offset, len(para1))
        self.sm.nextline()
        indented, offset = self.sm.getknownindented(2)
        self.assertEquals(indented, item2)
        self.assertEquals(offset, len(para1) + len(item1))
        self.sm.previousline(3)
        if self.sm.debug:
            print '\ntest_getindented: self.sm.line:\n', self.sm.line
        indented, indent, offset = self.sm.getindented()
        if self.sm.debug:
            print '\ntest_getindented: indented:\n', indented
        self.assertEquals(indent, lbindent)
        self.assertEquals(indented, literalblock)
        self.assertEquals(offset, (len(para1) + len(item1) + len(item2)
                                   - len(literalblock)))

    def test_run(self):
        self.assertEquals(self.sm.run(testtext), expected)


class EmptyStateTestCase(unittest.TestCase):

    def setUp(self):
        self.state = State(None, debug=debug)
        self.state.patterns = {'nop': 'dummy'}

    def test_addtransitions(self):
        self.assertEquals(len(self.state.transitions), 0)
        self.state.addtransitions([None])
        self.assertEquals(len(self.state.transitions), 1)

    def test_maketransition(self):
        self.assertEquals(self.state.maketransition('nop', 'bogus'),
                          ('nop', 'dummy', self.state.nop, 'bogus'))
        self.assertEquals(self.state.maketransition('nop'),
                          ('nop', 'dummy', self.state.nop,
                           self.state.__class__.__name__))

    def test_maketransitions(self):
        self.assertEquals(self.state.maketransitions((['nop'],
                                                      ('nop', 'bogus'))),
                          [('nop', 'dummy', self.state.nop,
                            self.state.__class__.__name__),
                           ('nop', 'dummy', self.state.nop, 'bogus')])


class MiscTestCase(unittest.TestCase):

    s2l_string = "hello\tthere\thow are\tyou?\n\tI'm fine\tthanks.\n"
    s2l_expected = ['hello   there   how are you?',
                    "        I'm fine        thanks.", '']
    indented_string = """\
        a
      literal
           block"""

    def test_string2lines(self):
        self.assertEquals(string2lines(self.s2l_string), self.s2l_expected)

    def test_extractindented(self):
        block = string2lines(self.indented_string)
        self.assertEquals(extractindented(block), ([s[6:] for s in block], 6))
        self.assertEquals(extractindented(self.s2l_expected), ([], 0))

def suite():
    """Return a suite containing all the test cases in this module."""
    suites = [unittest.makeSuite(case, 'test_') for case in
              (EmptySMTestCase, EmptySMWSTestCase, EmptyStateTestCase,
               SMWSTestCase, MiscTestCase)]
    return unittest.TestSuite(suites)


if __name__ == '__main__':
#    sys.argv.extend(['-v', '-d'])       # uncomment for very verbose output
    if sys.argv[-1] == '-d':
        debug = 1
        del sys.argv[-1]
    # When this module is executed from the command-line, run all its tests
    unittest.main(defaultTest='suite')
