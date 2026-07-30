from agent.context.models import LLMContext
from agent.context.providers import BaseContextProvider
from agent.rag.retriever import DocumentRetriever
from agent.rag.ranking import ChunkRanker


class DocumentContextProvider(
    BaseContextProvider,
):

    def __init__(
        self,
        retriever: DocumentRetriever,
        ranker: ChunkRanker,
    ):
        self._retriever = retriever
        self._ranker = ranker

    async def provide(
        self,
        context: LLMContext,
        **kwargs,
    ):

        query = kwargs["user_input"]

        chunks = await self._retriever.retrieve(
            query=query,
        )

        chunks = self._ranker.rank(
            chunks
        )

        if not chunks:
            return

        context.documents = "\n\n".join(
            chunk.metadata.get(
                "text",
                ""
            )
            for chunk in chunks
        )