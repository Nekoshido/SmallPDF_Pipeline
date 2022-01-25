import os
from platform import platform

import pandas as pd


class BaseETL:

    def __init__(self):
        self.spacing_bar = self.spacing_bar()

    @property
    def input_path(self) -> str:
        NotImplementedError("Method convert must be implemented")

    @property
    def destination_path(self) -> str:
        NotImplementedError("Method convert must be implemented")

    @staticmethod
    def spacing_bar() -> str:
        return r'\\' if platform == 'Windows' else "/"

    def _store_datatype_parquet(self, df: pd.DataFrame, filename: str, folder_name: str):
        final_path = f"{self.destination_path}{self.spacing_bar}{folder_name}{self.spacing_bar}"
        if not os.path.exists(final_path):
            os.makedirs(final_path)
        df.to_parquet(f"{final_path}{self.spacing_bar}{os.path.split(filename)[1].replace('.csv', '')}.parquet",
                      engine='fastparquet', index=False)

