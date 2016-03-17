# -*- coding: utf-8 -*-

__author__ = 'Diego Navarro'
__email__ = 'diego@feverup.com'
__version__ = '0.1.2'

try:
    from pysugarcrm import SugarCRM  # noqa
except ImportError:
    # this import is not needed in python 3, not sure it's necessary in python 2
    pass
