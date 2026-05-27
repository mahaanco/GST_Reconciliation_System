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

purchase_file = st.sidebar.file_uploader(
    "Upload Purchase Register",
    type=['xlsx', 'csv']
)

gstr2b_file = st.sidebar.file_uploader(
    "Upload GSTR-2B",
    type=['xlsx', 'csv']
)
if purchase_file and gstr2b_file:

    if purchase_file.name.endswith('.csv'):
        purchase_df = pd.read_csv(purchase_file)
    else:
        purchase_df = pd.read_excel(purchase_file)

    if gstr2b_file.name.endswith('.csv'):
        gstr2b_df = pd.read_csv(gstr2b_file)
    else:
        gstr2b_df = pd.read_excel(gstr2b_file)

    purchase_df = standardize_dataframe(purchase_df)
    gstr2b_df = standardize_dataframe(gstr2b_df)

    st.success("Files Processed Successfully")

    recon_engine = GSTReconciliation(
        purchase_df,
        gstr2b_df
    )

    reconciliation_df = recon_engine.exact_match()

    fuzzy_df = recon_engine.fuzzy_match()

    summary_df = ReportGenerator.summary_report(
        reconciliation_df
    )
    st.subheader("Reconciliation Summary")

    col1, col2, col3, col4 = st.columns(4)

    perfect_matches = len(
        reconciliation_df[
            reconciliation_df['MATCH_STATUS'] == 'Perfect Match'
        ]
    )

    value_mismatches = len(
        reconciliation_df[
            reconciliation_df['MATCH_STATUS'] == 'Value Mismatch'
        ]
    )
    missing_in_2b = len(
        reconciliation_df[
            reconciliation_df['MATCH_STATUS'] == 'Missing in 2B'
        ]
    )

    missing_in_books = len(
        reconciliation_df[
            reconciliation_df['MATCH_STATUS'] == 'Missing in Books'
        ]
    )

    col1.metric("Perfect Matches", perfect_matches)
    col2.metric("Value Mismatch", value_mismatches)
    col3.metric("Missing in 2B", missing_in_2b)
    col4.metric("Missing in Books", missing_in_books)

    st.subheader("Summary Chart")

    fig = px.pie(
        summary_df,
        names='Category',
        values='Count',
        title='GST Reconciliation Status'
    )

    st.plotly_chart(fig, use_container_width=True)

    st.subheader("Detailed Reconciliation")

    st.dataframe(
        reconciliation_df,
        use_container_width=True,
        height=500
    )
    st.subheader("Fuzzy Matches")

    st.dataframe(
        fuzzy_df,
        use_container_width=True,
        height=300
    )

    os.makedirs(EXPORT_FOLDER, exist_ok=True)

    export_path = os.path.join(
        EXPORT_FOLDER,
        'GST_Reconciliation_Report.xlsx'
    )
    ReportGenerator.export_excel(
        reconciliation_df,
        fuzzy_df,
        summary_df,
        export_path
    )

    with open(export_path, 'rb') as file:
        st.download_button(
            label='Download Reconciliation Report',
            data=file,
            file_name='GST_Reconciliation_Report.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        )
    
