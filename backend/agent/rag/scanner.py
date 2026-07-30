from pathlib import Path

from agent.rag.filters import FileFilter
from agent.rag.hasher import FileHasher
from agent.rag.models import IndexedFile


class FileScanner:

    def scan(
        self,
        root: Path,
    ):

        files = []

        for path in root.rglob("*"):

            if not path.is_file():
                continue

            if not FileFilter.supported(path):
                continue

            stat = path.stat()

            files.append(
                IndexedFile(
                    path=path,
                    file_name=path.name,
                    extension=path.suffix,
                    size=stat.st_size,
                    modified_at=None,
                    sha256=FileHasher.sha256(path),
                )
            )

        return files