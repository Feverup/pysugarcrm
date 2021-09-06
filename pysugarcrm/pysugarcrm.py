# -*- coding: utf-8 -*-
from contextlib import contextmanager
import json
import requests

try:
    # Python3 imports
    from urllib.parse import urlencode, urlparse, urlunparse
except ImportError:
    # Python2 imports
    from urllib import urlencode
    from urlparse import urlparse, urlunparse


__all__ = ['APIException', 'SugarCRM', 'sugar_api']


class APIException(Exception):
    """
    Custom exception to handle request errors
    """


class SugarCRM(object):
    """
    Sugar CRM API for v10
    """

    def __init__(
        self, url, username, password, client_id="sugar",
        login_path="/rest/v10/oauth2/token",
        base_path="/rest/v10/",
        platform="api"
    ):
        """
        Updates secret token to start making requests
        """

        parsed_url = list(urlparse(url))
        self.scheme, self.netloc = parsed_url[:2]
        parsed_url[2] = login_path
        login_url = urlunparse(parsed_url)
        self.base_path = base_path
        if not self.base_path.endswith('/'):
            self.base_path += '/'

        # Build login data
        data = {
            "grant_type": "password",
            "username": username,
            "password": password,
            "client_id": client_id,
            "platform": platform,
        }

        # Start requests session
        self.session = requests.Session()
        response = self.session.post(login_url, data=json.dumps(data)).json()

        # Retrieve auth token
        try:
            self.secret_token = response["access_token"]
        except KeyError:
            raise ValueError('No access token received')

        self.session.headers.update(
            {
                "Content-Type": "application/json",
                "OAuth-Token": self.secret_token,
            }
        )

        self.is_closed = False

    def _api_request(
        self, method, path, params='', query='', fragment='', *args, **kwargs
    ):
        """
        Low level API request to SugarCRM
        """

        url = urlunparse((
            self.scheme,
            self.netloc,
            self.base_path + path.lstrip('/'),
            params,
            query,
            fragment
        ))
        try:
            request = self.session.request(method, url, *args, **kwargs)
            return request.json()
        except ValueError:
            raise APIException('status code: {}, {}'.format(request.status_code, request.reason))

    @property
    def me(self):
        """
        Returns current user
        """

        return self._api_request("GET", "/me")

    def close(self):
        """
        Logs out the current user
        """

        response = self._api_request("POST", "/oauth2/logout")
        try:
            if response['success']:
                self.is_closed = True
                return self.is_closed
        except KeyError:
            raise APIException('There was a problem during logout')

    def get(self, path, query_params=None):
        """
        Generic GET API call
        """

        return self._api_request(
            "GET", path, query=urlencode(query_params or {})
        )

    def post(self, path, query_params=None, *args, **kwargs):
        """
        Generic POST API call
        """

        return self._api_request(
            "POST", path, query=urlencode(query_params or {}),
            *args, **kwargs
        )

    def put(self, path, query_params=None, *args, **kwargs):
        """
        Generic PUT API call
        """

        return self._api_request(
            "PUT", path, query=urlencode(query_params or {}),
            *args, **kwargs
        )


@contextmanager
def sugar_api(*args, **kwargs):
    conn = None
    try:
        conn = SugarCRM(*args, **kwargs)
        yield conn
    finally:
        if conn is not None and conn.is_closed is False:
            conn.close()
