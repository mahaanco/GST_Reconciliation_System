import streamlit as st

from services.upload_service import (
    UploadService
)

from services.reconciliation_service import (
    ReconciliationService
)

st.set_page_config(
    page_title="GST Reconciliation",
    layout="wide"
)

st.title(
    "GST Reconciliation System"
)

source_file = st.file_uploader(
    "Upload Source File",
    type=["xlsx", "xls", "csv"]
)

target_file = st.file_uploader(
    "Upload Target File",
    type=["xlsx", "xls", "csv"]
)

if (
    source_file
    and
    target_file
):

    source_df = (
        UploadService.load(
            source_file
        )
    )

    target_df = (
        UploadService.load(
            target_file
        )
    )

    st.success(
        "Files uploaded successfully"
    )

    st.write(
        "Source Records:",
        len(source_df)
    )

    st.write(
        "Target Records:",
        len(target_df)
    )

    if st.button(
        "Run Reconciliation"
    ):

        service = (
            ReconciliationService()
        )

        results = (
            service.run(
                source_df,
                target_df
            )
        )

        st.subheader("Summary")

        st.metric(
            "Matched",
            len(
                results["matched"]
            )
        )

        st.metric(
            "Missing in Target",
            len(
                results["source_only"]
            )
        )

        st.metric(
            "Missing in Source",
            len(
                results["target_only"]
            )
        )

        st.dataframe(
            results["matched"]
            .head(50)
        )
