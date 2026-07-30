from pathlib import Path

from agent.rag.scanner import FileScanner


class FileIndexService:

    def __init__(
        self,
        scanner: FileScanner,
    ):
        self._scanner = scanner

    def index(
        self,
        root: Path,
    ):
        return self._scanner.scan(root)