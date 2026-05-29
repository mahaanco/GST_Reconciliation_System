from parsers.excel_parser import ExcelParser
from parsers.csv_parser import CSVParser


class FileReader:

    @staticmethod
    def read(file):

        extension = (
            file.name
            .split(".")[-1]
            .lower()
        )

        if extension in [
            "xlsx",
            "xls"
        ]:
            return ExcelParser.read(file)

        if extension == "csv":
            return CSVParser.read(file)

        raise ValueError(
            f"Unsupported file type: {extension}"
        )
