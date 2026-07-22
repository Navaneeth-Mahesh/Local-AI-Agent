from agent.prompts.manager import PromptManager


def test_chat_prompt():
    manager = PromptManager()

    prompt = manager.build_chat_prompt(
        conversation="User: Hi",
        user_input="Hello"
    )

    assert "Hello" in prompt
    assert "Local AI Agent" in prompt