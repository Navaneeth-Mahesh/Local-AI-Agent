from pathlib import Path

from agent.rag.pipeline import RagPipeline
from agent.rag.scanner import FileScanner


class FileIndexService:

    def __init__(
        self,
        scanner: FileScanner,
        pipeline: RagPipeline,
    ):
        self._scanner = scanner
        self._pipeline = pipeline

    async def index(
        self,
        root: Path,
    ):

        files = self._scanner.scan(root)

        for file in files:

            await self._pipeline.process(
                file.path
            )