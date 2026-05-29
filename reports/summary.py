import pandas as pd


class SummaryGenerator:

    @staticmethod
    def generate_summary(results):

        summary = pd.DataFrame([
            {
                "Category": "Matched",
                "Count": len(results.get("matched", []))
            },
            {
                "Category": "Missing In Target",
                "Count": len(results.get("source_only", []))
            },
            {
                "Category": "Missing In Source",
                "Count": len(results.get("target_only", []))
            },
            {
                "Category": "Amount Mismatch",
                "Count": len(results.get("amount_mismatch", []))
            },
            {
                "Category": "Date Mismatch",
                "Count": len(results.get("date_mismatch", []))
            },
            {
                "Category": "Fuzzy Matches",
                "Count": len(results.get("fuzzy_matches", []))
            },
            {
                "Category": "Source Duplicates",
                "Count": len(results.get("source_duplicates", []))
            },
            {
                "Category": "Target Duplicates",
                "Count": len(results.get("target_duplicates", []))
            }
        ])

        return summary

    @staticmethod
    def dashboard_metrics(results):

        matched = len(results["matched"])

        missing = (
            len(results["source_only"])
            +
            len(results["target_only"])
        )

        total = matched + missing

        match_percentage = (
            round(
                (matched / total) * 100,
                2
            )
            if total > 0
            else 0
        )

        return {
            "total_records": total,
            "matched": matched,
            "missing": missing,
            "match_percentage": match_percentage
        }

    @staticmethod
    def vendor_summary(
        df,
        gstin_col,
        amount_col=None
    ):

        if df.empty:

            return pd.DataFrame()

        if (
            amount_col
            and
            amount_col in df.columns
        ):

            return (
                df.groupby(gstin_col)
                .agg(
                    Invoice_Count=(
                        gstin_col,
                        "count"
                    ),
                    Total_Amount=(
                        amount_col,
                        "sum"
                    )
                )
                .reset_index()
                .sort_values(
                    "Total_Amount",
                    ascending=False
                )
            )

        return (
            df.groupby(gstin_col)
            .size()
            .reset_index(
                name="Invoice_Count"
            )
            .sort_values(
                "Invoice_Count",
                ascending=False
            )
        )
