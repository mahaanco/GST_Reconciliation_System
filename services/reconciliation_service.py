from core.mapper import ColumnMapper
from core.reconciler import Reconciler


class ReconciliationService:

    def __init__(self):

        self.mapper = ColumnMapper(
            "config/mapping.json"
        )

        self.engine = Reconciler()
     def run(
    self,
    source_df,
    target_df
):

    source_mapping = self.mapper.map_columns(
        source_df
    )

    target_mapping = self.mapper.map_columns(
        target_df
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

    amount_col = source_mapping.get(
        "gst_amount"
    )

    date_col = source_mapping.get(
        "invoice_date"
    )

    return self.engine.reconcile(
        source_df=source_df,
        target_df=target_df,
        gstin_col=source_mapping["gstin"],
        invoice_col=source_mapping[
            "invoice_number"
        ],
        amount_col=amount_col,
        date_col=date_col
    )

    
