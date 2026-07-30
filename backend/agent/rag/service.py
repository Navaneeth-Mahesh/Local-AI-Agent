from pathlib import Path

from agent.rag.scanner import FileScanner


class FileIndexService:

    async def index(
        self,
        root,
    ):

        scanned_files = self._scanner.scan(root)

        for scanned in scanned_files:

            existing = await self._repository.get_by_path(
                str(scanned.path)
            )

            status = ChangeDetector.detect(
                existing,
                scanned,
            )

            if status.name == "NEW":
                ...

            elif status.name == "MODIFIED":
                ...

            else:
                continue