import pandas as pd


class ExcelParser:

    @staticmethod
    def read(file):

        extension = (
            file.name
            .split(".")[-1]
            .lower()
        )

        if extension == "xlsx":
            return pd.read_excel(
                file,
                engine="openpyxl"
            )

        if extension == "xls":
            return pd.read_excel(
                file,
                engine="xlrd"
            )

        raise ValueError(
            "Unsupported Excel format"
        )
