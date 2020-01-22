"""
doctor.py

Defines the Doctor class for managing
a collection of HTTP health checks.
"""

from . import check, report


class Doctor(object):
    def __init__(self, urls=[]):
        # TODO: determine the type of check to perform dynamically
        self.checks = [check.StatusCodeCheck(u, expected_status=200) for u in urls]

    def __iadd__(self, new_check):
        assert isinstance(new_check, check.Check)
        self.checks.append(new_check)

    def run(self):
        num_healthy = 0
        total = len(self.checks)
        results = [] # to store check.CheckResult

        # TODO: add multi-threading
        for ch in self.checks:
            results.append(ch.result())

        return report.Report(results)


