import time


class RateLimiter:

    def __init__(
        self,
        max_requests,
        period,
    ):

        self.max_requests = max_requests

        self.period = period

        self.requests = []

    def allow(self):

        now = time.time()

        self.requests = [
            request
            for request in self.requests
            if now - request
            < self.period
        ]

        if (
            len(self.requests)
            >= self.max_requests
        ):

            return False

        self.requests.append(now)

        return True