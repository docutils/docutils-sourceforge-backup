#! /usr/bin/env python

"""
Author: David Goodger
Contact: dgoodger@bigfoot.com
Revision: $Revision: 1.1.1.1 $
Date: $Date: 2001/07/21 22:14:04 $
Copyright: This module has been placed in the public domain.

"""

from dps.parsers import model
from dps.statemachine import string2lines
import states

__all__ = ['Parser']


class Parser(model.Parser):

    def parse(self, inputstring):
        model.Parser.parse(self, inputstring)
        sm = states.RSTStateMachine(stateclasses=states.stateclasses,
                                    initialstate='Body')
        inputlines = string2lines(self.inputstring)
        sm.run(inputlines, warninglevel=self.warninglevel,
               errorlevel=self.errorlevel)
        sm.unlink()
        return sm.memo.document
