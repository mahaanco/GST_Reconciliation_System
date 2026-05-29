import re
import pandas as pd


class DataCleaner:

    @staticmethod
    def clean_invoice_number(invoice):

        if pd.isna(invoice):
            return ""

        invoice = str(invoice).upper().strip()

        invoice = re.sub(
            r'[^A-Z0-9]',
            '',
            invoice
        )

        return invoice

    @staticmethod
    def clean_gstin(gstin):

        if pd.isna(gstin):
            return ""

        return (
            str(gstin)
            .upper()
            .strip()
        )

    @staticmethod
    def clean_amount(value):

        try:
            return round(
                float(value),
                2
            )
        except Exception:
            return 0.0

    @staticmethod
    def clean_date(value):

        try:
            return pd.to_datetime(
            value,
            errors="coerce",
            dayfirst=True
     )
        except Exception:
            return pd.NaT

    @classmethod
    def standardize_dataframe(
        cls,
        df,
        column_mapping
    ):
        """
        Standardizes critical columns.
        """

        df = df.copy()

        if column_mapping.get("gstin"):
            df[
                column_mapping["gstin"]
            ] = (
                df[
                    column_mapping["gstin"]
                ]
                .apply(
                    cls.clean_gstin
                )
            )

        if column_mapping.get(
            "invoice_number"
        ):
            df[
                column_mapping[
                    "invoice_number"
                ]
            ] = (
                df[
                    column_mapping[
                        "invoice_number"
                    ]
                ]
                .apply(
                    cls.clean_invoice_number
                )
            )

        if column_mapping.get(
            "gst_amount"
        ):
            df[
                column_mapping[
                    "gst_amount"
                ]
            ] = (
                df[
                    column_mapping[
                        "gst_amount"
                    ]
                ]
                .apply(
                    cls.clean_amount
                )
            )

        if column_mapping.get(
            "invoice_date"
        ):
            df[
                column_mapping[
                    "invoice_date"
                ]
            ] = (
                df[
                    column_mapping[
                        "invoice_date"
                    ]
                ]
                .apply(
                    cls.clean_date
                )
            )

        return df
