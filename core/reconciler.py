import pandas as pd

from core.matcher import (
    ExactMatcher
)

from core.duplicate_detector import (
    DuplicateDetector
)

from core.fuzzy_matcher import (
    FuzzyMatcher
)


class Reconciler:

    def __init__(
        self,
        amount_tolerance=1,
        date_tolerance=3,
        fuzzy_threshold=95
    ):

        self.amount_tolerance = (
            amount_tolerance
        )

        self.date_tolerance = (
            date_tolerance
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
            ExactMatcher
            .create_match_key(
                source_df,
                gstin_col,
                invoice_col
            )
        )

        target_df = (
            ExactMatcher
            .create_match_key(
                target_df,
                gstin_col,
                invoice_col
            )
        )

        source_duplicates = (
            DuplicateDetector
            .detect(
                source_df
            )
        )

        target_duplicates = (
            DuplicateDetector
            .detect(
                target_df
            )
        )

        (
            matched,
            source_only,
            target_only
        ) = (
            ExactMatcher.match(
                source_df,
                target_df
            )
        )

        amount_mismatch = (
            self._check_amount_mismatch(
                matched,
                target_df,
                amount_col
            )
            if amount_col
            else pd.DataFrame()
        )

        date_mismatch = (
            self._check_date_mismatch(
                matched,
                target_df,
                date_col
            )
            if date_col
            else pd.DataFrame()
        )

        fuzzy_matches = (
            FuzzyMatcher.match(
                source_only,
                target_only,
                gstin_col,
                invoice_col,
                self.fuzzy_threshold
            )
        )

        return {

            "matched":
                matched,

            "source_only":
                source_only,

            "target_only":
                target_only,

            "amount_mismatch":
                amount_mismatch,

            "date_mismatch":
                date_mismatch,

            "fuzzy_matches":
                fuzzy_matches,

            "source_duplicates":
                source_duplicates,

            "target_duplicates":
                target_duplicates
        }

    def _check_amount_mismatch(
        self,
        matched_df,
        target_df,
        amount_col
    ):

        target_amounts = (
            target_df[
                [
                    "MATCH_KEY",
                    amount_col
                ]
            ]
            .rename(
                columns={
                    amount_col:
                    "TARGET_AMOUNT"
                }
            )
        )

        result = (
            matched_df.merge(
                target_amounts,
                on="MATCH_KEY",
                how="left"
            )
        )

        result[
            "AMOUNT_DIFF"
        ] = (
            result[amount_col]
            -
            result[
                "TARGET_AMOUNT"
            ]
        )

        return result[
            result[
                "AMOUNT_DIFF"
            ].abs()
            >
            self.amount_tolerance
        ]

    def _check_date_mismatch(
        self,
        matched_df,
        target_df,
        date_col
    ):

        target_dates = (
            target_df[
                [
                    "MATCH_KEY",
                    date_col
                ]
            ]
            .rename(
                columns={
                    date_col:
                    "TARGET_DATE"
                }
            )
        )

        result = (
            matched_df.merge(
                target_dates,
                on="MATCH_KEY",
                how="left"
            )
        )

        result[
            "DATE_DIFF"
        ] = (
            (
                pd.to_datetime(
                    result[
                        date_col
                    ]
                )
                -
                pd.to_datetime(
                    result[
                        "TARGET_DATE"
                    ]
                )
            )
            .dt.days
            .abs()
        )

        return result[
            result[
                "DATE_DIFF"
            ]
            >
            self.date_tolerance
        ]
