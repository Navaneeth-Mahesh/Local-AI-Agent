from pathlib import Path

from agent.rag.loaders.factory import LoaderFactory
from agent.rag.chunking.service import ChunkingService
from agent.rag.embedder import ChunkEmbedder
from agent.rag.vector_mapper import ChunkVectorMapper
from agent.vector_store.interfaces import BaseVectorStore


class RagPipeline:

    def __init__(
        self,
        *,
        loader_factory: LoaderFactory,
        chunking_service: ChunkingService,
        embedder: ChunkEmbedder,
        vector_store: BaseVectorStore,
    ):
        self._loader_factory = loader_factory
        self._chunking_service = chunking_service
        self._embedder = embedder
        self._vector_store = vector_store

    async def process(
        self,
        path: Path,
    ):

        loader = self._loader_factory.get_loader(
            path
        )

        document = loader.load(
            path
        )

        chunks = self._chunking_service.chunk(
            document
        )

        for chunk in chunks:

            vector = await self._embedder.embed(
                chunk.text
            )

            record = (
                ChunkVectorMapper.to_vector_record(
                    chunk=chunk,
                    embedding=vector,
                )
            )

            await self._vector_store.upsert(
                record
            )