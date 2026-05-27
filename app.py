import streamlit as st
import pandas as pd
import os
import plotly.express as px

from reconciliation_engine import GSTReconciliation
from report_generator import ReportGenerator
from utils import standardize_dataframe
from config import EXPORT_FOLDER

st.set_page_config(
    page_title="GST Reconciliation System",
    layout="wide"
)

st.title("GST Reconciliation Automation System")

st.sidebar.header("Upload Files")


# ==========================================
# SMART FILE READER
# ==========================================
def read_file(file, file_type):

    file_name = file.name.lower()

    try:

        # CSV FILES
        if file_name.endswith(".csv"):

            df = pd.read_csv(file)

        # XLSX FILES
        elif file_name.endswith(".xlsx"):

            if file_type == "purchase":

                # PURCHASE REGISTER
                df = pd.read_excel(
                    file,
                    skiprows=1,
                    engine="openpyxl"
                )

            else:

                # GSTR2B
                df = pd.read_excel(
                    file,
                    skiprows=2,
                    engine="openpyxl"
                )

        # XLS FILES
        elif file_name.endswith(".xls"):

            if file_type == "purchase":

                df = pd.read_excel(
                    file,
                    skiprows=1,
                    engine="xlrd"
                )

            else:

                df = pd.read_excel(
                    file,
                    skiprows=2,
                    engine="xlrd"
                )

        else:

            raise ValueError(
                "Unsupported file format"
            )

        # REMOVE EMPTY ROWS
        df = df.dropna(
            how="all"
        )

        # REMOVE EMPTY COLUMNS
        df = df.dropna(
            axis=1,
            how="all"
        )

        # RESET INDEX
        df.reset_index(
            drop=True,
            inplace=True
        )

        return df

    except Exception as e:

        st.error(
            f"Error reading file: {str(e)}"
        )

        return None


# ==========================================
# FILE UPLOADS
# ==========================================
purchase_file = st.sidebar.file_uploader(
    "Upload Purchase Register",
    type=["xlsx", "xls", "csv"]
)

gstr2b_file = st.sidebar.file_uploader(
    "Upload GSTR-2B",
    type=["xlsx", "xls", "csv"]
)


# ==========================================
# MAIN PROCESS
# ==========================================
if purchase_file and gstr2b_file:

    # READ FILES
    purchase_df = read_file(
        purchase_file,
        "purchase"
    )

    gstr2b_df = read_file(
        gstr2b_file,
        "2b"
    )

    # STOP IF FAILED
    if purchase_df is None or gstr2b_df is None:

        st.stop()

    # STANDARDIZE DATA
    purchase_df = standardize_dataframe(
        purchase_df
    )

    gstr2b_df = standardize_dataframe(
        gstr2b_df
    )

    # REMOVE INVALID RECORDS
    purchase_df = purchase_df[
        (purchase_df["GSTIN"] != "")
        &
        (purchase_df["INVOICE_NO"] != "")
    ]

    gstr2b_df = gstr2b_df[
        (gstr2b_df["GSTIN"] != "")
        &
        (gstr2b_df["INVOICE_NO"] != "")
    ]

    # REMOVE DUPLICATES
    purchase_df = purchase_df.drop_duplicates(
        subset=[
            "GSTIN",
            "INVOICE_NO",
            "GST_AMOUNT"
        ]
    )

    gstr2b_df = gstr2b_df.drop_duplicates(
        subset=[
            "GSTIN",
            "INVOICE_NO",
            "GST_AMOUNT"
        ]
    )

    st.success(
        "Files Processed Successfully"
    )

    # ==========================================
    # RECON ENGINE
    # ==========================================
    recon_engine = GSTReconciliation(
        purchase_df,
        gstr2b_df
    )

    reconciliation_df = recon_engine.exact_match()

    fuzzy_df = recon_engine.fuzzy_match()

    # ==========================================
    # SUMMARY
    # ==========================================
    summary_df = ReportGenerator.summary_report(
        reconciliation_df
    )

    st.subheader(
        "Reconciliation Summary"
    )

    col1, col2, col3, col4 = st.columns(4)

    perfect_matches = len(
        reconciliation_df[
            reconciliation_df["MATCH_STATUS"]
            ==
            "Perfect Match"
        ]
    )

    value_mismatches = len(
        reconciliation_df[
            reconciliation_df["MATCH_STATUS"]
            ==
            "Value Mismatch"
        ]
    )

    missing_in_2b = len(
        reconciliation_df[
            reconciliation_df["MATCH_STATUS"]
            ==
            "Missing in 2B"
        ]
    )

    missing_in_books = len(
        reconciliation_df[
            reconciliation_df["MATCH_STATUS"]
            ==
            "Missing in Books"
        ]
    )

    # KPI CARDS
    col1.metric(
        "Perfect Matches",
        perfect_matches
    )

    col2.metric(
        "Value Mismatch",
        value_mismatches
    )

    col3.metric(
        "Missing in 2B",
        missing_in_2b
    )

    col4.metric(
        "Missing in Books",
        missing_in_books
    )

    # ==========================================
    # CHART
    # ==========================================
    st.subheader("Summary Chart")

    fig = px.pie(
        summary_df,
        names="Category",
        values="Count",
        title="GST Reconciliation Status"
    )

    st.plotly_chart(
        fig,
        use_container_width=True
    )

    # ==========================================
    # DATA TABLES
    # ==========================================
    st.subheader(
        "Detailed Reconciliation"
    )

    st.dataframe(
        reconciliation_df,
        use_container_width=True,
        height=500
    )

    st.subheader(
        "Fuzzy Matches"
    )

    st.dataframe(
        fuzzy_df,
        use_container_width=True,
        height=300
    )

    # ==========================================
    # EXPORT REPORT
    # ==========================================
    os.makedirs(
        EXPORT_FOLDER,
        exist_ok=True
    )

    export_path = os.path.join(
        EXPORT_FOLDER,
        "GST_Reconciliation_Report.xlsx"
    )

    ReportGenerator.export_excel(
        reconciliation_df,
        fuzzy_df,
        summary_df,
        export_path
    )

    # ==========================================
    # DOWNLOAD BUTTON
    # ==========================================
    with open(export_path, "rb") as file:

        st.download_button(
            label="Download Reconciliation Report",
            data=file,
            file_name="GST_Reconciliation_Report.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
        )
