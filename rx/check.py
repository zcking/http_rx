"""
check.py

Defines functions for performing a health
check against a HTTP target.
"""

import requests


class Check(object):
    def __init__(self, url, method='GET', expected_status=200,
                 headers=[], data={}):
        self.url = url
        self.method = method
        self.expected_status = expected_status
        self.headers = headers
        self.data = data

    def is_healthy(self):
        resp = self.call()
        return resp.status_code == self.expected_status

    def call(self):
        return requests.request(
            self.method,
            headers=self.headers,
            url=self.url,
            data=self.data
        )


