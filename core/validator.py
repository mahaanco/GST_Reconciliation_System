import re
import pandas as pd


class GSTValidator:

    GSTIN_REGEX = (
        r'^[0-9]{2}'
        r'[A-Z]{5}'
        r'[0-9]{4}'
        r'[A-Z]{1}'
        r'[1-9A-Z]{1}'
        r'Z'
        r'[0-9A-Z]{1}$'
    )

    @classmethod
    def is_valid_gstin(
        cls,
        gstin
    ):

        if pd.isna(gstin):
            return False

        gstin = (
            str(gstin)
            .upper()
            .strip()
        )

        return bool(
            re.match(
                cls.GSTIN_REGEX,
                gstin
            )
        )

    @classmethod
    def validate_dataframe(
        cls,
        df,
        gstin_column
    ):

        result = df.copy()

        result[
            "GSTIN_VALID"
        ] = (
            result[gstin_column]
            .apply(
                cls.is_valid_gstin
            )
        )

        return result

    @classmethod
    def get_invalid_records(
        cls,
        df,
        gstin_column
    ):

        validated = (
            cls.validate_dataframe(
                df,
                gstin_column
            )
        )

        return validated[
            validated[
                "GSTIN_VALID"
            ] == False
        ]
