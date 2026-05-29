import pandas as pd


class SummaryGenerator:
    """
    Generates reconciliation summaries for reporting
    and dashboard visualization.
    """

    @staticmethod
    def generate(results):
        """
        Generates count-based summary.
        """

        return pd.DataFrame(
            [
                {
                    "Category": "Matched",
                    "Count": len(results.get("matched", pd.DataFrame()))
                },
                {
                    "Category": "Missing in Source",
                    "Count": len(results.get("target_only", pd.DataFrame()))
                },
                {
                    "Category": "Missing in Target",
                    "Count": len(results.get("source_only", pd.DataFrame()))
                },
                {
                    "Category": "Amount Mismatch",
                    "Count": len(results.get("amount_mismatch", pd.DataFrame()))
                },
                {
                    "Category": "Date Mismatch",
                    "Count": len(results.get("date_mismatch", pd.DataFrame()))
                },
                {
                    "Category": "Fuzzy Matches",
                    "Count": len(results.get("fuzzy_matches", pd.DataFrame()))
                }
            ]
        )

    @staticmethod
    def generate_amount_summary(
        results,
        amount_column
    ):
        """
        Generates amount-wise summary.
        """

        categories = {
            "Matched": "matched",
            "Missing in Source": "target_only",
            "Missing in Target": "source_only",
            "Amount Mismatch": "amount_mismatch",
            "Date Mismatch": "date_mismatch",
            "Fuzzy Matches": "fuzzy_matches"
        }

        rows = []

        for display_name, key in categories.items():

            df = results.get(
                key,
                pd.DataFrame()
            )

            if (
                not df.empty
                and amount_column in df.columns
            ):
                amount = (
                    pd.to_numeric(
                        df[amount_column],
                        errors="coerce"
                    )
                    .fillna(0)
                    .sum()
                )
            else:
                amount = 0

            rows.append(
                {
                    "Category": display_name,
                    "Amount": round(
                        amount,
                        2
                    )
                }
            )

        return pd.DataFrame(rows)

    @staticmethod
    def generate_vendor_summary(
        df,
        gstin_column,
        amount_column
    ):
        """
        Vendor-wise GST summary.
        Useful for vendor follow-up reports.
        """

        if df.empty:
            return pd.DataFrame(
                columns=[
                    gstin_column,
                    "Invoice_Count",
                    "Total_Amount"
                ]
            )

        result = (
            df.groupby(gstin_column)
            .agg(
                Invoice_Count=(
                    gstin_column,
                    "count"
                ),
                Total_Amount=(
                    amount_column,
                    "sum"
                )
            )
            .reset_index()
            .sort_values(
                "Total_Amount",
                ascending=False
            )
        )

        result["Total_Amount"] = (
            result["Total_Amount"]
            .round(2)
        )

        return result

    @staticmethod
    def generate_status_summary(
        results
    ):
        """
        Consolidated status table.
        """

        rows = []

        status_mapping = {
            "MATCHED": "matched",
            "MISSING_IN_SOURCE": "target_only",
            "MISSING_IN_TARGET": "source_only",
            "AMOUNT_MISMATCH": "amount_mismatch",
            "DATE_MISMATCH": "date_mismatch",
            "FUZZY_MATCH": "fuzzy_matches"
        }

        for status, key in status_mapping.items():

            count = len(
                results.get(
                    key,
                    pd.DataFrame()
                )
            )

            rows.append(
                {
                    "Status": status,
                    "Count": count
                }
            )

        return pd.DataFrame(rows)

    @staticmethod
    def generate_dashboard_metrics(
        results
    ):
        """
        Generates dashboard KPIs.
        Returns dictionary.
        """

        matched = len(
            results.get(
                "matched",
                pd.DataFrame()
            )
        )

        source_only = len(
            results.get(
                "source_only",
                pd.DataFrame()
            )
        )

        target_only = len(
            results.get(
                "target_only",
                pd.DataFrame()
            )
        )

        amount_mismatch = len(
            results.get(
                "amount_mismatch",
                pd.DataFrame()
            )
        )

        date_mismatch = len(
            results.get(
                "date_mismatch",
                pd.DataFrame()
            )
        )

        fuzzy_matches = len(
            results.get(
                "fuzzy_matches",
                pd.DataFrame()
            )
        )

        total_records = (
            matched
            + source_only
            + target_only
        )

        match_percentage = (
            round(
                (
                    matched
                    / total_records
                )
                * 100,
                2
            )
            if total_records > 0
            else 0
        )

        return {
            "total_records": total_records,
            "matched": matched,
            "source_only": source_only,
            "target_only": target_only,
            "amount_mismatch": amount_mismatch,
            "date_mismatch": date_mismatch,
            "fuzzy_matches": fuzzy_matches,
            "match_percentage": match_percentage
        }
