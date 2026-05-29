import pandas as pd
import re


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

        return str(gstin).upper().strip()

    @staticmethod
    def clean_amount(value):

        try:
            return round(
                float(value),
                2
            )

        except:
            return 0.0

    @staticmethod
    def clean_date(date_value):

        try:
            return pd.to_datetime(
                date_value,
                errors="coerce"
            )

        except:
            return pd.NaT

    @staticmethod
    def standardize_dataframe(df):

        df = df.copy()

        for col in df.columns:

            if df[col].dtype == "object":

                df[col] = (
                    df[col]
                    .astype(str)
                    .str.strip()
                )

        return df
