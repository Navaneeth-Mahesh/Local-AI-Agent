from agent.brain.brain import AgentBrain
from agent.context.builder import ContextBuilder
from agent.context.manager import ContextManager
from agent.llm.dependencies import get_llm_service
from agent.planner.planner import Planner
from agent.prompts.manager import PromptManager
from agent.tools.manager import ToolManager
from agent.tools.registry import ToolRegistry
from agent.tools.calculator.tool import CalculatorTool


def get_agent_brain() -> AgentBrain:

    registry = ToolRegistry()

    registry.register(
        CalculatorTool()
    )

    return AgentBrain(
        context_manager=ContextManager(
            ContextBuilder([])
        ),
        prompt_manager=PromptManager(),
        planner=Planner(),
        tool_manager=ToolManager(registry),
        llm_service=get_llm_service(),
    )