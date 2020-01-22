"""
check.py

Defines functions for performing a health
check against a HTTP target.
"""

import requests
from enum import Enum


# TODO: add more types to this (e.g. body parsing etc.)
class ConditionType(Enum):
    STATUS_CODE = 1


class Check(object):
    def __init__(self, url, method='GET', headers=[], data={}):
        self.url = url
        self.method = method
        self.headers = headers
        self.data = data

    def call(self):
        return requests.request(
            self.method,
            headers=self.headers,
            url=self.url,
            data=self.data
        )


class StatusCodeCheck(Check):
    def __init__(self, url, method='GET', headers=[], data={}, expected_status=200):
        super().__init__(url, method, headers, data)
        self.expected_status = expected_status

    def result(self):
        resp = self.call()

        if resp.status_code != self.expected_status:
            fail_msg = f'expected status code {self.expected_status} but got {resp.status_code}'
            return Result(resp=resp, is_healthy=False, fail_reason=fail_msg)
        else:
            return Result(resp=resp, is_healthy=True)


class Result(object):
    def __init__(self, name='', resp=None, is_healthy=True, fail_reason=None):
        self.resp        = resp
        self.is_healthy  = is_healthy
        self.fail_reason = fail_reason
        self.name        = name

    def failure_str(self):
        if self.name:
            return f'check {self.name} failed : {self.fail_reason}'
        else:
            return f'check {self.resp.url} failed : {self.fail_reason}'


