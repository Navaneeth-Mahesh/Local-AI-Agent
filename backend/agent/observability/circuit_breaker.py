class CircuitBreaker:

    def __init__(
        self,
        threshold=5,
    ):

        self.failures = 0

        self.threshold = threshold

    def record_failure(self):

        self.failures += 1

    def is_open(self):

        return (
            self.failures
            >= self.threshold
        )