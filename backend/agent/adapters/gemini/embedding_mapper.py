from agent.embeddings.models import EmbeddingResult


class GeminiEmbeddingMapper:
    """
    Maps Gemini embedding responses
    into our domain model.
    """

    @staticmethod
    def to_domain(response) -> EmbeddingResult:

        vector = response.embeddings[0].values

        return EmbeddingResult(
            vector=vector,
            dimensions=len(vector),
            provider="gemini",
        )