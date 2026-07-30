from agent.brain.result import AgentResult


class AgentExecutor:

    def __init__(
        self,
        brain,
        tool_registry,
    ):
        self._brain = brain
        self._tool_registry = tool_registry

    async def execute(
        self,
        state,
    ) -> AgentResult:

        while True:

            state.iteration += 1

            response = await self._brain.run(
                state
            )

            if response.tool_call is None:

                return AgentResult(
                    response=response.content,
                    iterations=state.iteration,
                    tool_calls=len(
                        state.tool_history
                    ),
                )

            tool = self._tool_registry.get(
                response.tool_call.name
            )

            result = await tool.execute(
                **response.tool_call.arguments
            )

            state.tool_history.append(
                result
            )