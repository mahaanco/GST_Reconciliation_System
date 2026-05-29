from rapidfuzz import fuzz
import pandas as pd


class FuzzyMatcher:

    @staticmethod
    def match(
        source_df,
        target_df,
        gstin_col,
        invoice_col,
        threshold=95
    ):

        matches = []

        target_groups = (
            target_df.groupby(
                gstin_col
            )
        )

        for _, source_row in (
            source_df.iterrows()
        ):

            gstin = source_row[
                gstin_col
            ]

            if (
                gstin
                not in
                target_groups.groups
            ):
                continue

            candidates = (
                target_groups
                .get_group(gstin)
            )

            source_invoice = str(
                source_row[
                    invoice_col
                ]
            )

            for _, target_row in (
                candidates.iterrows()
            ):

                target_invoice = str(
                    target_row[
                        invoice_col
                    ]
                )

                score = fuzz.ratio(
                    source_invoice,
                    target_invoice
                )

                if score >= threshold:

                    matches.append(
                        {
                            "GSTIN": gstin,
                            "SOURCE_INVOICE":
                                source_invoice,
                            "TARGET_INVOICE":
                                target_invoice,
                            "SCORE":
                                score
                        }
                    )

        return pd.DataFrame(
            matches
        )
