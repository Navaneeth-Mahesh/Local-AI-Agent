from enum import Enum


class FileStatus(Enum):

    NEW = "new"

    MODIFIED = "modified"

    UNCHANGED = "unchanged"

    DELETED = "deleted"

class ChangeDetector:

    @staticmethod
    def detect(
        db_file,
        scanned_file,
    ):

        if db_file is None:
            return FileStatus.NEW

        if db_file.sha256 != scanned_file.sha256:
            return FileStatus.MODIFIED

        return FileStatus.UNCHANGED