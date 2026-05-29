import pandas as pd


class SummaryGenerator:

    @staticmethod
    def generate(results):

        summary = pd.DataFrame([
            {
                "Category": "Matched",
                "Count": len(results["matched"])
            },
            {
                "Category": "Missing in Source",
                "Count": len(results["target_only"])
            },
            {
                "Category": "Missing in Target",
                "Count": len(results["source_only"])
            },
            {
                "Category": "Amount Mismatch",
                "Count": len(results["amount_mismatch"])
            },
            {
                "Category": "Date Mismatch",
                "Count": len(results["date_mismatch"])
            },
            {
                "Category": "Fuzzy Matches",
                "Count": len(results["fuzzy_matches"])
            }
        ])

        return summary
