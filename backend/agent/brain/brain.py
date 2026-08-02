from typing import Any
from agent.brain.models import AgentResponse
from agent.brain.loop import AgentLoop
from agent.context.manager import ContextManager
from agent.llm.service import LLMService
from agent.planner.planner import Planner
from agent.prompts.manager import PromptManager
from agent.state.manager import AgentStateManager
from agent.state.models import AgentState
from agent.tools.manager import ToolManager


class AgentBrain:
    """
    Main AI orchestrator.

    Coordinates context building, planning, tool execution, and response synthesis.
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
        *,
        conversation: Any = None,
    ) -> AgentResponse:
        state = AgentState(
            user_input=user_input,
        )

        AgentStateManager.start(state)

        state.context = await self._context_manager.create_context(
            state=state,
        )

        loop = AgentLoop(
            planner=self._planner,
            tool_manager=self._tool_manager,
            llm_service=self._llm_service,
            prompt_manager=self._prompt_manager,
        )

        plan, tool_results, llm_response = await loop.execute(state)

        AgentStateManager.complete(state)

        text_response = llm_response.text if llm_response else "Processing complete."

        return AgentResponse(
            state=state,
            plan=plan,
            response=text_response,
            tool_results=tool_results,
        )