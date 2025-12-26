#! /usr/bin/env python

"""
:Author: David Goodger
:Contact: goodger@users.sourceforge.net
:Revision: $Revision: 1.12 $
:Date: $Date: 2002/03/28 04:28:10 $
:Copyright: This module has been placed in the public domain.

This is ``the dps.parsers.restructuredtext`` package. It exports a single
class, `Parser`.

Usage
=====

1. Create a parser::

       parser = dps.parsers.restructuredtext.Parser()

   Several optional arguments may be passed to modify the parser's behavior.
   Please see `dps.parsers.Parser` for details.

2. Gather input (a multi-line string), by reading a file or the standard
   input::

       input = sys.stdin.read()

3. Create a new empty `dps.nodes.document` tree::

       docroot = dps.utils.newdocument()

   See `dps.utils.newdocument()` for parameter details.

4. Run the parser, populating the document tree::

       document = parser.parse(input, docroot)

Parser Overview
===============

The reStructuredText parser is implemented as a state machine, examining its
input one line at a time. To understand how the parser works, please first
become familiar with the `dps.statemachine` module, then see the
`states` module.
"""

__docformat__ = 'reStructuredText'

__all__ = ['Parser']

import dps.parsers
import dps.statemachine
import states


class Parser(dps.parsers.Parser):

    """The reStructuredText parser."""

    def parse(self, inputstring, docroot):
        """Parse `inputstring` and populate `docroot`, a document tree."""
        self.setup_parse(inputstring, docroot)
        debug = docroot.reporter[''].debug
        self.statemachine = states.RSTStateMachine(
              stateclasses=states.stateclasses, initialstate='Body',
              debug=debug)
        inputlines = dps.statemachine.string2lines(
              inputstring, convertwhitespace=1)
        self.statemachine.run(inputlines, docroot)
