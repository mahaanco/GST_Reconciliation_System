import pandas as pd


class CSVParser:

    @staticmethod
    def read(file):

        return pd.read_csv(
            file,
            encoding_errors="ignore"
        )
