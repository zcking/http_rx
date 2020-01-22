"""
check.py

Defines functions for performing a health
check against a HTTP target.
"""

import requests
import json


class Check(object):
    def __init__(self, conf):
        self.url = conf['url']
        self.method = conf.get('method', 'GET') # defaults to HTTP GET
        self.headers = conf.get('headers', [])
        self.data = conf.get('data')

    def call(self):
        return requests.request(
            self.method,
            headers=self.headers,
            url=self.url,
            data=self.data
        )


class StatusCodeCheck(Check):
    def __init__(self, conf):
        super().__init__(conf)
        self.expected_status = conf.get('expected', 200) # default to expect 200 (OK)

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


CHECK_DEFS = {
        'status': StatusCodeCheck,
}


def parse_check(conf):
    ctype = conf.get('type', None)
    if ctype is None:
        raise Exception('you must specify a \'type\' in your check config')
    ch = CHECK_DEFS.get(ctype, None)
    if ch is None:
        raise Exception(f'{ctype} is not a valid check type')

    # Check is valid and we now have the actual class/type loaded
    # initialize the check and return it to caller
    return ch(conf)


