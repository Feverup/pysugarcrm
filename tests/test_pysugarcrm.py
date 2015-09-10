#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
test_pysugarcrm
----------------------------------

Tests for `pysugarcrm` module.
"""

import json
import unittest
import responses

from pysugarcrm import SugarCRM


class TestPysugarcrm(unittest.TestCase):

    def setUp(self):
        pass

    @responses.activate
    def test_login(self):
        test_access_token = "dsf3898sdjsdfj388jdsj8"
        responses.add(
            responses.POST,
            'http://testserver.com/rest/v10/oauth2/token',
            body=json.dumps({'access_token': test_access_token}),
            status=200
        )

        api = SugarCRM('http://testserver.com/', "admin", "12345")
        self.assertEqual(api.secret_token, test_access_token)
