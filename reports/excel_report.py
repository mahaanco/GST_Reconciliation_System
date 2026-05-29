import io
import pandas as pd

from reports.summary import SummaryGenerator


class ExcelReportGenerator:

    @staticmethod
    def generate(results):

        output = io.BytesIO()

        with pd.ExcelWriter(
            output,
            engine="xlsxwriter"
        ) as writer:

            workbook = writer.book

            header_format = workbook.add_format({
                "bold": True,
                "border": 1
            })

            summary_df = (
                SummaryGenerator.generate(
                    results
                )
            )

            summary_df.to_excel(
                writer,
                sheet_name="Summary",
                index=False
            )

            worksheet = (
                writer.sheets["Summary"]
            )

            for col_num, value in enumerate(
                summary_df.columns.values
            ):
                worksheet.write(
                    0,
                    col_num,
                    value,
                    header_format
                )

            ExcelReportGenerator.write_sheet(
                writer,
                results["matched"],
                "Matched",
                header_format
            )

            ExcelReportGenerator.write_sheet(
                writer,
                results["source_only"],
                "Missing_in_Target",
                header_format
            )

            ExcelReportGenerator.write_sheet(
                writer,
                results["target_only"],
                "Missing_in_Source",
                header_format
            )

            ExcelReportGenerator.write_sheet(
                writer,
                results["amount_mismatch"],
                "Amount_Mismatch",
                header_format
            )

            ExcelReportGenerator.write_sheet(
                writer,
                results["date_mismatch"],
                "Date_Mismatch",
                header_format
            )

            ExcelReportGenerator.write_sheet(
                writer,
                results["fuzzy_matches"],
                "Fuzzy_Matches",
                header_format
            )

        output.seek(0)

        return output

    @staticmethod
    def write_sheet(
        writer,
        df,
        sheet_name,
        header_format
    ):

        if df.empty:
            df = pd.DataFrame({
                "Message": [
                    "No records found"
                ]
            })

        df.to_excel(
            writer,
            sheet_name=sheet_name,
            index=False
        )

        worksheet = (
            writer.sheets[sheet_name]
        )

        for col_num, value in enumerate(
            df.columns.values
        ):
            worksheet.write(
                0,
                col_num,
                value,
                header_format
            )

        for idx, col in enumerate(df.columns):

            max_len = max(
                len(str(col)),
                df[col]
                .astype(str)
                .map(len)
                .max()
            )

            worksheet.set_column(
                idx,
                idx,
                min(max_len + 5, 40)
            )
