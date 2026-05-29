import json


class ColumnMapper:

    def __init__(
        self,
        mapping_file
    ):

        with open(
            mapping_file,
            "r",
            encoding="utf-8"
        ) as f:

            self.mapping = json.load(f)

    def normalize_name(
        self,
        column_name
    ):

        return (
            str(column_name)
            .strip()
            .lower()
        )

    def map_columns(
        self,
        df
    ):

        mapped = {}

        normalized_columns = {
            self.normalize_name(col): col
            for col in df.columns
        }

        for standard_name, aliases in self.mapping.items():

            found = None

            for alias in aliases:

                alias = alias.lower()

                if alias in normalized_columns:

                    found = normalized_columns[alias]
                    break

            mapped[standard_name] = found

        return mapped

    def validate_mapping(
        self,
        mapped_columns
    ):

        mandatory = [
            "gstin",
            "invoice_number"
        ]

        missing = []

        for field in mandatory:

            if mapped_columns.get(field) is None:

                missing.append(field)

        return missing
