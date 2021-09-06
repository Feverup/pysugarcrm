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

from pysugarcrm import SugarCRM, sugar_api


class TestPysugarcrm(unittest.TestCase):
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

    @responses.activate
    def test_context_manager(self):
        test_access_token = "dsf3898sdjsdfj388jdsj8"
        responses.add(
            responses.POST,
            'http://testserver.com/rest/v10/oauth2/token',
            body=json.dumps({'access_token': "dsf3898sdjsdfj388jdsj8"}),
            status=200
        )

        responses.add(
            responses.POST,
            'http://testserver.com/rest/v10/oauth2/logout',
            body=json.dumps({'success': True}),
            status=200
        )

        responses.add(
            responses.GET,
            'http://testserver.com/rest/v10/me',
            body=json.dumps({'success': True}),
            status=200
        )

        with sugar_api('http://testserver.com/', "admin", "12345") as api:
            self.assertEqual(api.secret_token, test_access_token)
            self.assertEqual(api.me['success'], True)
            self.assertEqual(api.is_closed, False)

        self.assertEqual(api.is_closed, True)

    @responses.activate
    def test_context_manager_without_access_token(self):
        responses.add(
            responses.POST,
            'http://testserver.com/rest/v10/oauth2/token',
            body=json.dumps({}),
            status=200
        )

        self.assertRaises(ValueError, func=sugar_api('http://testserver.com/', "admin", "12345"))
