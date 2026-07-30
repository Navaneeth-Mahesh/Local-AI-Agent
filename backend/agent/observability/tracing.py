import uuid


class TraceContext:

    @staticmethod
    def new():

        return str(
            uuid.uuid4()
        )