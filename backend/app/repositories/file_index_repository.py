from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession

from app.models.indexed_file import IndexedFile


class FileIndexRepository:

    def __init__(
        self,
        db: AsyncSession,
    ):
        self.db = db

    async def get_by_path(
        self,
        path: str,
    ):

        stmt = select(
            IndexedFile
        ).where(
            IndexedFile.path == path
        )

        result = await self.db.execute(stmt)

        return result.scalar_one_or_none()

    async def save(
        self,
        file: IndexedFile,
    ):

        self.db.add(file)

        await self.db.commit()

        await self.db.refresh(file)

        return file