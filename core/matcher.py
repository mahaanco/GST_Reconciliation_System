import pandas as pd


class ExactMatcher:

    @staticmethod
    def create_match_key(
        df,
        gstin_col,
        invoice_col
    ):

        result = df.copy()

        result["MATCH_KEY"] = (
            result[gstin_col]
            .astype(str)
            .str.upper()
            .str.strip()
            +
            "_"
            +
            result[invoice_col]
            .astype(str)
            .str.upper()
            .str.strip()
        )

        return result

    @staticmethod
    def match(
        source_df,
        target_df
    ):

        source_keys = set(
            source_df["MATCH_KEY"]
        )

        target_keys = set(
            target_df["MATCH_KEY"]
        )

        matched_keys = (
            source_keys
            .intersection(
                target_keys
            )
        )

        matched = source_df[
            source_df["MATCH_KEY"]
            .isin(matched_keys)
        ].copy()

        source_only = source_df[
            ~source_df["MATCH_KEY"]
            .isin(matched_keys)
        ].copy()

        target_only = target_df[
            ~target_df["MATCH_KEY"]
            .isin(matched_keys)
        ].copy()

        return (
            matched,
            source_only,
            target_only
        )
