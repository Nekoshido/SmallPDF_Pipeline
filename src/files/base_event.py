import pandas as pd


class BaseEvent:

    @property
    def column_dict(self) -> dict:
        NotImplementedError("Method convert must be implemented")

    @property
    def separator(self) -> str:
        NotImplementedError("Method convert must be implemented")

    def read_csv_schema(self, input_path: str) -> pd.DataFrame:
        df = pd.read_csv(input_path, sep=self.separator)
        for key in self.column_dict.keys():
            if key not in df:
                df[key] = None
        return df.astype(self.column_dict)

    @staticmethod
    def _infer_date_format(df: pd.DataFrame, column_to_infer: str, date_format: str) -> pd.DataFrame:
        df[column_to_infer] = pd.to_datetime(df[column_to_infer], format=date_format, errors='coerce')
        return df
