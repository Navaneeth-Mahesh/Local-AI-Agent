class Telemetry:

    def tool_started(
        self,
        tool,
    ):

        print(
            f"Tool Start: {tool}"
        )

    def tool_finished(
        self,
        tool,
    ):

        print(
            f"Tool End: {tool}"
        )