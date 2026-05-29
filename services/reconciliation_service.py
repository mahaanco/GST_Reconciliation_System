from core.mapper import (
    ColumnMapper
)

from core.cleaner import (
    DataCleaner
)

from core.reconciler import (
    Reconciler
)


class ReconciliationService:

    def __init__(
        self,
        mapping_file="config/mapping.json"
    ):

        self.mapper = (
            ColumnMapper(
                mapping_file
            )
        )

    def run(
        self,
        source_df,
        target_df,
        amount_tolerance=1,
        date_tolerance=3,
        fuzzy_threshold=95
    ):

        source_mapping = (
            self.mapper.map_columns(
                source_df
            )
        )

        target_mapping = (
            self.mapper.map_columns(
                target_df
            )
        )

        missing_source = (
            self.mapper.validate_mapping(
                source_mapping
            )
        )

        missing_target = (
            self.mapper.validate_mapping(
                target_mapping
            )
        )

        if missing_source:

            raise ValueError(
                f"Source missing columns: {missing_source}"
            )

        if missing_target:

            raise ValueError(
                f"Target missing columns: {missing_target}"
            )

        source_df = (
            DataCleaner.standardize_dataframe(
                source_df,
                source_mapping
            )
        )

        target_df = (
            DataCleaner.standardize_dataframe(
                target_df,
                target_mapping
            )
        )

        engine = Reconciler(
            amount_tolerance=
            amount_tolerance,

            date_tolerance=
            date_tolerance,

            fuzzy_threshold=
            fuzzy_threshold
        )

        return engine.reconcile(
    source_df=source_df,
    target_df=target_df,

    source_gstin_col=source_mapping["gstin"],
    target_gstin_col=target_mapping["gstin"],

    source_invoice_col=source_mapping["invoice_number"],
    target_invoice_col=target_mapping["invoice_number"],

    source_amount_col=source_mapping.get("gst_amount"),
    target_amount_col=target_mapping.get("gst_amount"),

    source_date_col=source_mapping.get("invoice_date"),
    target_date_col=target_mapping.get("invoice_date")
)
