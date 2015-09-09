===============================
PySugarCRM
===============================

.. image:: https://img.shields.io/travis/dnmellen/pysugarcrm.svg
        :target: https://travis-ci.org/dnmellen/pysugarcrm

.. image:: https://img.shields.io/pypi/v/pysugarcrm.svg
        :target: https://pypi.python.org/pypi/pysugarcrm


Python API Wrapper for SugarCRM v10

* Free software: BSD license
* Documentation: https://pysugarcrm.readthedocs.org.

Quickstart
------------

.. code-block :: bash

    $ pip install pysugarcrm


.. code-block :: python

    from pysugarcrm.pysugarcrm import SugarCRM
    api = SugarCRM('https://yourdomain.sugaropencloud.eu', 'youruser', 'yourpassword')
    api.me
    api.get('/Calls')

Features
--------

* OAuth2 authentication with username and password
