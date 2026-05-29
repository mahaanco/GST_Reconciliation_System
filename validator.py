import re


class GSTValidator:

    GSTIN_PATTERN = (
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

        if not gstin:
            return False

        gstin = str(gstin).strip().upper()

        return bool(
            re.match(
                cls.GSTIN_PATTERN,
                gstin
            )
        )

    @classmethod
    def validate_column(
        cls,
        df,
        gstin_column
    ):

        result = df.copy()

        result["gstin_valid"] = (
            result[gstin_column]
            .apply(
                cls.is_valid_gstin
            )
        )

        return result
