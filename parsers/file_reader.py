from parsers.excel_parser import (
    ExcelParser
)

from parsers.csv_parser import (
    CSVParser
)


class FileReader:

    SUPPORTED_TYPES = [
        "xlsx",
        "xls",
        "csv"
    ]

    @classmethod
    def read(
        cls,
        file
    ):

        extension = (
            file.name
            .split(".")[-1]
            .lower()
        )

        if extension not in cls.SUPPORTED_TYPES:

            raise ValueError(
                f"Unsupported file type: {extension}"
            )

        if extension in [
            "xlsx",
            "xls"
        ]:

            return ExcelParser.read(
                file
            )

        if extension == "csv":

            return CSVParser.read(
                file
            )

        raise ValueError(
            "Could not process file"
        )
