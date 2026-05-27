import pandas as pd
from datetime import datetime


class ReportGenerator:

    @staticmethod
    def summary_report(df):

        summary = df['MATCH_STATUS'].value_counts().reset_index()
        summary.columns = ['Category', 'Count']

        return summary
    @staticmethod
    def export_excel(reconciliation_df, fuzzy_df, summary_df, file_path):

        with pd.ExcelWriter(file_path, engine='xlsxwriter') as writer:

            reconciliation_df.to_excel(
                writer,
                sheet_name='Reconciliation',
                index=False
            )

            fuzzy_df.to_excel(
                writer,
                sheet_name='Fuzzy Matches',
                index=False
            )
            fuzzy_df.to_excel(
                writer,
                sheet_name='Fuzzy Matches',
                index=False
            )

            summary_df.to_excel(
                writer,
                sheet_name='Summary',
                index=False
            )
