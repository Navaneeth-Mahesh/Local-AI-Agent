from collections import defaultdict


class Metrics:

    def __init__(self):

        self._values = defaultdict(int)

    def increment(
        self,
        name: str,
    ):

        self._values[name] += 1

    def get(
        self,
        name: str,
    ):

        return self._values[name]