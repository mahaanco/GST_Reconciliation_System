import pandas as pd


class ExcelParser:

    @staticmethod
    def read(file):

        extension = (
            file.name
            .split(".")[-1]
            .lower()
        )

        engine = (
            "openpyxl"
            if extension == "xlsx"
            else "xlrd"
        )

        preview = pd.read_excel(
            file,
            engine=engine,
            header=None,
            nrows=20
        )

        header_row = 0

        for i in range(len(preview)):

            row = [
                str(x).strip().lower()
                for x in preview.iloc[i]
            ]

            if (
                "gstin/uin" in row
                or "gstin" in row
            ):
                header_row = i
                break

        file.seek(0)

        return pd.read_excel(
            file,
            engine=engine,
            header=header_row
        )

df = pd.read_excel(
    file,
    engine="xlrd",
    header=header_row
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
