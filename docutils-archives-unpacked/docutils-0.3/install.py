#!/usr/bin/env python
# $Id: install.py,v 1.2 2003/06/09 21:26:29 goodger Exp $
# Copyright: This file has been placed in the public domain.

"""
This is a quick & dirty installation shortcut. It is equivalent to the
command::

    python setup.py install

However, the shortcut lacks error checking!
"""

from distutils import core
from setup import do_setup

if __name__ == '__main__' :
    core._setup_stop_after = 'config'
    dist = do_setup()
    dist.commands = ['install']
    dist.run_commands()
