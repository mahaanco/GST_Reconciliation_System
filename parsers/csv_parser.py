import pandas as pd


class CSVParser:

    @staticmethod
    def read(file):

        encodings = [
            "utf-8",
            "latin-1",
            "cp1252"
        ]

        for encoding in encodings:

            try:

                file.seek(0)

                return pd.read_csv(
                    file,
                    encoding=encoding
                )

            except Exception:
                pass

        raise ValueError(
            "Unable to read CSV file"
        )
