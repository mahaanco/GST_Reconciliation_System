import pandas as pd

from core.matcher import ExactMatcher
from core.fuzzy_matcher import FuzzyMatcher


class Reconciler:

    def __init__(
        self,
        amount_tolerance=1,
        date_tolerance_days=3,
        fuzzy_threshold=95
    ):

        self.amount_tolerance = (
            amount_tolerance
        )

        self.date_tolerance_days = (
            date_tolerance_days
        )

        self.fuzzy_threshold = (
            fuzzy_threshold
        )

    def reconcile(
        self,
        source_df,
        target_df,
        gstin_col,
        invoice_col,
        amount_col=None,
        date_col=None
    ):

        source_df = (
            ExactMatcher.create_key(
                source_df,
                gstin_col,
                invoice_col
            )
        )

        target_df = (
            ExactMatcher.create_key(
                target_df,
                gstin_col,
                invoice_col
            )
        )

        (
            matched,
            source_only,
            target_only
        ) = ExactMatcher.exact_match(
            source_df,
            target_df
        )

        amount_mismatch = (
            self.check_amount_variance(
                matched,
                target_df,
                amount_col
            )
            if amount_col
            else pd.DataFrame()
        )

        date_mismatch = (
            self.check_date_variance(
                matched,
                target_df,
                date_col
            )
            if date_col
            else pd.DataFrame()
        )

        fuzzy_matches = (
            FuzzyMatcher.find_matches(
                source_only,
                target_only,
                gstin_col,
                invoice_col,
                self.fuzzy_threshold
            )
        )

        return {
            "matched": matched,
            "source_only": source_only,
            "target_only": target_only,
            "amount_mismatch":
                amount_mismatch,
            "date_mismatch":
                date_mismatch,
            "fuzzy_matches":
                fuzzy_matches
        }

    def check_amount_variance(
        self,
        matched_df,
        target_df,
        amount_col
    ):

        target_amounts = (
            target_df[
                ["match_key", amount_col]
            ]
            .rename(
                columns={
                    amount_col:
                    "target_amount"
                }
            )
        )

        result = matched_df.merge(
            target_amounts,
            on="match_key",
            how="left"
        )

        result["difference"] = (
            result[amount_col]
            -
            result["target_amount"]
        )

        return result[
            result["difference"]
            .abs()
            >
            self.amount_tolerance
        ]

    def check_date_variance(
        self,
        matched_df,
        target_df,
        date_col
    ):

        target_dates = (
            target_df[
                ["match_key", date_col]
            ]
            .rename(
                columns={
                    date_col:
                    "target_date"
                }
            )
        )

        result = matched_df.merge(
            target_dates,
            on="match_key",
            how="left"
        )

        result["day_difference"] = (
            (
                pd.to_datetime(
                    result[date_col]
                )
                -
                pd.to_datetime(
                    result["target_date"]
                )
            )
            .dt.days
            .abs()
        )

        return result[
            result["day_difference"]
            >
            self.date_tolerance_days
        ]
