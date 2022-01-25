import pandas as pd
import numpy as np

from src.files.base_event import BaseEvent


class ReportingPeriods(BaseEvent):

    def infer_reporting_period_start(self, df: pd.DataFrame) -> pd.DataFrame:
        return self._infer_date_format(df, 'reporting_period_start', '%Y-%m-%d %H:%M:%S')

    def infer_reporting_period_end(self, df: pd.DataFrame) -> pd.DataFrame:
        return self._infer_date_format(df, 'reporting_period_end', '%Y-%m-%d %H:%M:%S')

    @property
    def column_dict(self):
        return {'reporting_period_start': np.object,
                'reporting_period_end': np.object,
                'reporting_period_length': np.int64}

    @property
    def separator(self) -> str:
        return ","
