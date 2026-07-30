from agent.streaming.models import StreamEvent


class SSEFormatter:

    @staticmethod
    def format(
        event: StreamEvent,
    ) -> str:

        return (
            f"event: {event.event}\n"
            f"data: {event.data}\n\n"
        )