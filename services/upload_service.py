from parsers.file_reader import (
    FileReader
)


class UploadService:

    @staticmethod
    def load_file(file):

        return FileReader.read(
            file
        )
