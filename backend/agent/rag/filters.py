SUPPORTED_EXTENSIONS = {
    ".txt",
    ".md",
    ".pdf",
    ".docx",
    ".py",
    ".json",
    ".yaml",
    ".yml",
}


class FileFilter:

    @staticmethod
    def supported(path):

        return (
            path.suffix.lower()
            in SUPPORTED_EXTENSIONS
        )