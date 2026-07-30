from agent.embeddings.factory import (
    EmbeddingFactory,
)

from app.core.config import settings


def get_embedding_service():

    return EmbeddingFactory.create_gemini(
        api_key=settings.GEMINI_API_KEY,
    )