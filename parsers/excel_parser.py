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

        elif extension == "xls":

            return pd.read_excel(
                file,
                engine="xlrd"
            )

        raise ValueError(
            f"Unsupported Excel format: {extension}"
        )

    @staticmethod
    def get_sheet_names(file):

        excel_file = pd.ExcelFile(file)

        return excel_file.sheet_names

    @staticmethod
    def read_sheet(
        file,
        sheet_name
    ):

        return pd.read_excel(
            file,
            sheet_name=sheet_name
        )
