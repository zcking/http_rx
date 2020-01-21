"""
doctor.py

Defines the Doctor class for managing
a collection of HTTP health checks.
"""

from . import check


class Doctor(object):
    def __init__(self, urls=[]):
        self.checks = [check.Check(u) for u in urls]

    def __iadd__(self, new_check):
        assert isinstance(new_check, check.Check)
        self.checks.append(new_check)

    def run(self):
        num_healthy = 0
        total = len(self.checks)

        # TODO: add multi-threading
        for ch in self.checks:
            if ch.is_healthy():
                num_healthy += 1

        # TODO: create Report class
        return (num_healthy, total)


