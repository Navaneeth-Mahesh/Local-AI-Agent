from agent.brain.models import AgentResponse
from agent.context.manager import ContextManager
from agent.llm.service import LLMService
from agent.planner.planner import Planner
from agent.prompts.manager import PromptManager
from agent.state.manager import AgentStateManager
from agent.state.models import AgentState
from agent.tools.context import ToolContext
from agent.tools.manager import ToolManager


class AgentBrain:
    """
    Main AI orchestrator.

    Coordinates every AI subsystem.
    """

    def __init__(
        self,
        *,
        context_manager: ContextManager,
        prompt_manager: PromptManager,
        planner: Planner,
        tool_manager: ToolManager,
        llm_service: LLMService,
    ) -> None:

        self._context_manager = context_manager
        self._prompt_manager = prompt_manager
        self._planner = planner
        self._tool_manager = tool_manager
        self._llm_service = llm_service

    async def run(
        self,
        user_input: str,
    ) -> AgentResponse:

        state = AgentState(
            user_input=user_input,
        )

        AgentStateManager.start(state)

        state.context = await self._context_manager.create_context(
            state=state,
        )

        prompt = self._prompt_manager.build_chat_prompt(
            conversation="",
            user_input=user_input,
        )

        plan = await self._planner.plan(state)

        tool_results = []

        for step in plan.steps:

            if step.step_type.value == "tool":

                result = await self._tool_manager.execute(
                    "calculator",
                    ToolContext(state),
                    expression="2 + 2",
                )

                tool_results.append(result)

        llm_response = await self._llm_service.generate(
            prompt=prompt,
        )

        AgentStateManager.complete(state)

        return AgentResponse(
            state=state,
            plan=plan,
            response=llm_response.text,
            tool_results=tool_results,
        )