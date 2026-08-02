from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.ext.asyncio import AsyncSession
from jose import JWTError

from app.core.config import settings
from app.core.security import decode_access_token
from app.database.session import get_db
from app.repositories.user_repository import UserRepository
from app.repositories.conversation_repository import ConversationRepository
from app.repositories.message_repository import MessageRepository
from app.models.user import User
from app.services.auth_service import AuthService
from app.services.settings_service import SettingsService
from app.services.ai_provider_service import AIProviderService
from app.services.chat_service import ChatService

from agent.conversation.manager import ConversationManager
from agent.brain.brain import AgentBrain
from agent.context.manager import ContextManager
from agent.prompts.manager import PromptManager
from agent.planner.planner import Planner
from agent.tools.manager import ToolManager
from agent.tools.registry import ToolRegistry
from agent.llm.service import LLMService
from agent.llm.factory import LLMFactory
from agent.llm.enums import ProviderType

oauth_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")


async def get_current_user(
    token: str = Depends(oauth_scheme),
    db: AsyncSession = Depends(get_db),
) -> User:
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
        if user_id is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = await UserRepository(db).get_by_id(int(user_id))
    if not user:
        raise credentials_exception

    return user


async def get_auth_service(db: AsyncSession = Depends(get_db)) -> AuthService:
    return AuthService(db)


async def get_settings_service(db: AsyncSession = Depends(get_db)) -> SettingsService:
    return SettingsService(db)


async def get_ai_provider_service(db: AsyncSession = Depends(get_db)) -> AIProviderService:
    return AIProviderService(db)


async def get_conversation_manager(db: AsyncSession = Depends(get_db)) -> ConversationManager:
    conv_repo = ConversationRepository(db)
    msg_repo = MessageRepository(db)
    return ConversationManager(
        conversation_repository=conv_repo,
        message_repository=msg_repo,
    )


async def get_llm_service(
    user: User = Depends(get_current_user),
    db: AsyncSession = Depends(get_db),
) -> LLMService:
    provider_repo_service = AIProviderService(db)
    provider_db = await provider_repo_service.get_provider(user.id)
    
    api_key = provider_db.api_key if provider_db and provider_db.api_key else settings.GEMINI_API_KEY
    provider_type = ProviderType.GEMINI
    
    provider_instance = LLMFactory.create(
        provider=provider_type,
        api_key=api_key,
    )
    return LLMService(provider=provider_instance)


async def get_agent_brain(
    llm_service: LLMService = Depends(get_llm_service),
) -> AgentBrain:
    tool_registry = ToolRegistry()
    tool_manager = ToolManager(registry=tool_registry)
    context_manager = ContextManager()
    prompt_manager = PromptManager()
    planner = Planner()

    return AgentBrain(
        context_manager=context_manager,
        prompt_manager=prompt_manager,
        planner=planner,
        tool_manager=tool_manager,
        llm_service=llm_service,
    )


async def get_chat_service(
    brain: AgentBrain = Depends(get_agent_brain),
    conversation_manager: ConversationManager = Depends(get_conversation_manager),
) -> ChatService:
    return ChatService(
        brain=brain,
        conversation_manager=conversation_manager,
    )
