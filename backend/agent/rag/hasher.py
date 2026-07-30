import hashlib


class FileHasher:

    @staticmethod
    def sha256(path):

        digest = hashlib.sha256()

        with open(path, "rb") as file:

            while chunk := file.read(8192):

                digest.update(chunk)

        return digest.hexdigest()