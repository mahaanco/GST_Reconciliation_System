import pandas as pd


class DuplicateDetector:

    @staticmethod
    def detect(
        df,
        key_column="MATCH_KEY"
    ):

        duplicates = df[
            df.duplicated(
                subset=[key_column],
                keep=False
            )
        ].copy()

        return duplicates.sort_values(
            key_column
        )
