import asyncio


class RetryPolicy:

    async def run(
        self,
        func,
        retries=3,
    ):

        for attempt in range(
            retries
        ):

            try:

                return await func()

            except Exception:

                if (
                    attempt
                    == retries - 1
                ):

                    raise

                await asyncio.sleep(
                    2 ** attempt
                )