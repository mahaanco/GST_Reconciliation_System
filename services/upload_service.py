from parsers.file_reader import FileReader


class UploadService:

    @staticmethod
    def load(file):

        df = FileReader.read(file)

        return df
