import streamlit as st

from services.upload_service import (
    UploadService
)

from services.reconciliation_service import (
    ReconciliationService
)

from reports.summary import (
    SummaryGenerator
)

from reports.excel_report import (
    ExcelReportGenerator
)


st.set_page_config(
    page_title="GST Reconciliation System",
    layout="wide"
)

st.title(
    "GST Reconciliation System"
)

st.markdown(
    """
    Supports:

    - Purchase Register vs GSTR-2B
    - Sales Register vs GSTR-1
    - XLSX
    - XLS
    - CSV
    """
)

# --------------------------------------------------
# SIDEBAR
# --------------------------------------------------

st.sidebar.header(
    "Reconciliation Settings"
)



reconciliation_type = (
    st.sidebar.selectbox(
        "Reconciliation Type",
        [
            "Purchase Register vs GSTR-2B",
            "Sales Register vs GSTR-1"
        ]
    )
)

amount_tolerance = (
    st.sidebar.number_input(
        "Amount Tolerance",
        min_value=0.0,
        value=1.0
    )
)

date_tolerance = (
    st.sidebar.number_input(
        "Date Tolerance (Days)",
        min_value=0,
        value=3
    )
)

fuzzy_threshold = (
    st.sidebar.slider(
        "Fuzzy Match Threshold",
        min_value=80,
        max_value=100,
        value=95
    )
)

# --------------------------------------------------
# FILE UPLOAD
# --------------------------------------------------

col1, col2 = st.columns(2)

with col1:

    source_file = (
        st.file_uploader(
            "Upload Source File",
            type=[
                "xlsx",
                "xls",
                "csv"
            ]
        )
    )

with col2:

    target_file = (
        st.file_uploader(
            "Upload Target File",
            type=[
                "xlsx",
                "xls",
                "csv"
            ]
        )
    )

# --------------------------------------------------
# PROCESS
# --------------------------------------------------

if source_file and target_file:

    try:

        source_df = (
            UploadService.load_file(
                source_file
            )
        )

        target_df = (
            UploadService.load_file(
                target_file
            )
        )
        st.subheader("DEBUG - SOURCE COLUMNS")
        st.write(source_df.columns.tolist())

        st.subheader("DEBUG - TARGET COLUMNS")
        st.write(target_df.columns.tolist())

        st.success(
            "Files loaded successfully."
        )st.subheader("Source Columns")
st.write(source_df.columns.tolist())

st.subheader("Target Columns")
st.write(target_df.columns.tolist())

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Source Records",
                len(source_df)
            )

        with col2:

            st.metric(
                "Target Records",
                len(target_df)
            )

        st.divider()

        if st.button(
            "Run Reconciliation",
            use_container_width=True
        ):

            with st.spinner(
                "Running reconciliation..."
            ):

                service = (
                    ReconciliationService()
                )

                results = (
                    service.run(
                        source_df=
                            source_df,

                        target_df=
                            target_df,

                        amount_tolerance=
                            amount_tolerance,

                        date_tolerance=
                            date_tolerance,

                        fuzzy_threshold=
                            fuzzy_threshold
                    )
                )

            st.success(
                "Reconciliation completed."
            )

            # -------------------------------------
            # DASHBOARD METRICS
            # -------------------------------------

            metrics = (
                SummaryGenerator
                .dashboard_metrics(
                    results
                )
            )

            c1, c2, c3, c4 = (
                st.columns(4)
            )

            with c1:
                st.metric(
                    "Total Records",
                    metrics[
                        "total_records"
                    ]
                )

            with c2:
                st.metric(
                    "Matched",
                    metrics[
                        "matched"
                    ]
                )

            with c3:
                st.metric(
                    "Missing",
                    metrics[
                        "missing"
                    ]
                )

            with c4:
                st.metric(
                    "Match %",
                    f"{metrics['match_percentage']}%"
                )

            st.divider()

            # -------------------------------------
            # REPORT DOWNLOAD
            # -------------------------------------

            report_file = (
                ExcelReportGenerator
                .generate(
                    results
                )
            )

            st.download_button(
                label=
                    "Download Excel Report",

                data=
                    report_file,

                file_name=
                    "GST_Reconciliation_Report.xlsx",

                mime=
                    "application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",

                use_container_width=True
            )

            st.divider()

            # -------------------------------------
            # RESULT TABS
            # -------------------------------------

            tabs = st.tabs(
                [
                    "Matched",
                    "Missing In Target",
                    "Missing In Source",
                    "Amount Mismatch",
                    "Date Mismatch",
                    "Fuzzy Matches",
                    "Source Duplicates",
                    "Target Duplicates"
                ]
            )

            with tabs[0]:
                st.dataframe(
                    results[
                        "matched"
                    ],
                    use_container_width=True
                )

            with tabs[1]:
                st.dataframe(
                    results[
                        "source_only"
                    ],
                    use_container_width=True
                )

            with tabs[2]:
                st.dataframe(
                    results[
                        "target_only"
                    ],
                    use_container_width=True
                )

            with tabs[3]:
                st.dataframe(
                    results[
                        "amount_mismatch"
                    ],
                    use_container_width=True
                )

            with tabs[4]:
                st.dataframe(
                    results[
                        "date_mismatch"
                    ],
                    use_container_width=True
                )

            with tabs[5]:
                st.dataframe(
                    results[
                        "fuzzy_matches"
                    ],
                    use_container_width=True
                )

            with tabs[6]:
                st.dataframe(
                    results[
                        "source_duplicates"
                    ],
                    use_container_width=True
                )

            with tabs[7]:
                st.dataframe(
                    results[
                        "target_duplicates"
                    ],
                    use_container_width=True
                )

    except Exception as e:

        st.error(
            str(e)
        )
