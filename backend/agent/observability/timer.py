import time
from contextlib import contextmanager


@contextmanager
def timer(name: str):

    start = time.perf_counter()

    try:
        yield

    finally:
        elapsed = (
            time.perf_counter()
            - start
        )

        print(
            f"{name}: {elapsed:.3f}s"
        )