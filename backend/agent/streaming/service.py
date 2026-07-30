from collections.abc import AsyncGenerator

from agent.streaming.models import StreamEvent
from agent.streaming.sse import SSEFormatter


class StreamingService:

    async def stream(
        self,
        generator: AsyncGenerator[str, None],
    ):

        async for token in generator:

            yield SSEFormatter.format(
                StreamEvent(
                    event="token",
                    data=token,
                )
            )

        yield SSEFormatter.format(
            StreamEvent(
                event="done",
                data="",
            )
        )