from agent.planner.enums import PlanStepType
from agent.state.manager import AgentStateManager
from agent.tools.context import ToolContext


class AgentLoop:
    """
    Executes an execution plan.

    The loop is responsible for coordinating
    tools and the LLM.
    """

    def __init__(
        self,
        planner,
        tool_manager,
        llm_service,
        prompt_manager,
    ):
        self._planner = planner
        self._tool_manager = tool_manager
        self._llm_service = llm_service
        self._prompt_manager = prompt_manager

    async def execute(
        self,
        state,
    ):

        plan = await self._planner.plan(state)

        tool_results = []

        llm_response = None

        for step in plan.steps:

            match step.step_type:

                case PlanStepType.TOOL:

                    tool_result = await self._tool_manager.execute(
                        step.metadata["tool"],
                        ToolContext(state),
                        **step.metadata.get(
                            "arguments",
                            {},
                        ),
                    )

                    tool_results.append(tool_result)

                    AgentStateManager.next_step(state)

                case PlanStepType.LLM:

                    prompt = self._prompt_manager.build_chat_prompt(
                        conversation="",
                        user_input=state.user_input,
                    )

                    llm_response = await self._llm_service.generate(
                        prompt=prompt,
                    )

                    AgentStateManager.next_step(state)

                case PlanStepType.FINISH:

                    AgentStateManager.complete(state)

        return plan, tool_results, llm_response