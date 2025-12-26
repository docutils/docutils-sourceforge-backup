
r"""
>>> errorist = utils.Errorist(1, 3, sys.stdout)
>>> errorist.system_warning(0, 'a little reminder')
<system_warning: <paragraph...>>
>>> sw = errorist.system_warning(1, 'a mild warning')
Warning: [level 1] a mild warning
>>> sw
<system_warning: <paragraph...>>
>>> sw = errorist.system_warning(2, 'a stern warning')
Warning: [level 2] a stern warning
>>> sw = errorist.system_warning(3, 'an urgent warning, converted to an exception')
Traceback (most recent call last):
  ...
SystemWarning: [level 3] an urgent warning, converted to an exception
>>> sw = errorist.strong_system_warning('STOP', 'a strong warning')
Traceback (most recent call last):
  ,,,
SystemWarning: [level 3] STOP: a strong warning

>>> errorist = utils.Errorist(4, 4, sys.stdout)
>>> sw = errorist.strong_system_warning('STOP', 'a strong warning', 'error\n  source')
>>> str(sw)
'<system_warning level="3"><paragraph><strong>STOP</strong>: a strong warning</paragraph><literal_block>error\n  source</literal_block></system_warning>'
"""

import sys, doctest
import utils, test_utils

if __name__ == '__main__':
	failures, tries = doctest.testmod(test_utils)
	print 'Ran %s tests, %s failures.' % (tries, failures)
	if failures == 0:
		print 'OK'
