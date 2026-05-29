import pandas as pd


class ExactMatcher:

    @staticmethod
    def create_key(
        df,
        gstin_col,
        invoice_col
    ):
        result = df.copy()

        result["match_key"] = (
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
    def exact_match(
        source_df,
        target_df
    ):

        source_keys = set(
            source_df["match_key"]
        )

        target_keys = set(
            target_df["match_key"]
        )

        matched_keys = (
            source_keys
            .intersection(target_keys)
        )

        matched = source_df[
            source_df["match_key"]
            .isin(matched_keys)
        ].copy()

        source_only = source_df[
            ~source_df["match_key"]
            .isin(matched_keys)
        ].copy()

        target_only = target_df[
            ~target_df["match_key"]
            .isin(matched_keys)
        ].copy()

        return (
            matched,
            source_only,
            target_only
        )
