import os

import pandas as pd
from pandasql import sqldf
from pathlib import Path

from src.etls.base_etl import BaseETL


class GoldETL(BaseETL):

    def __init__(self, country: bool = False):
        super().__init__()
        self.country = country

    @property
    def input_path(self) -> str:
        return f'{Path(__file__).parent.parent.parent}/datalake/silver/'

    @property
    def destination_path(self) -> str:
        return f'{Path(__file__).parent.parent.parent}/datalake/gold/'

    @property
    def invoice_path(self):
        return f'{self.input_path}{self.spacing_bar}invoices{self.spacing_bar}'

    @property
    def reporting_periods_path(self):
        return f'{self.input_path}{self.spacing_bar}reporting_periods{self.spacing_bar}'

    @staticmethod
    def running_sql_query(query: str):
        return sqldf(query, globals())

    def revenue_recognition_query(self):
        query = ("SELECT ss.reporting_period_start, ss.reporting_period_end,"
                 f"{' ss.country,' if self.country else ''} SUM(ss.amount) AS recognized_revenue "
                 "FROM ("
                 "SELECT rp.reporting_period_start, rp.reporting_period_end,"
                 f" i.amount {',i.country ' if self.country else ''}"
                 "FROM invoices i JOIN reporting_periods rp "
                 "ON i.supply_date_end >= rp.reporting_period_start "
                 "AND i.supply_date_end < rp.reporting_period_end"
                 ") ss "
                 f"GROUP BY ss.reporting_period_start, ss.reporting_period_end{', country' if self.country else ''}"
                 )
        return query

    def etl_revenue_recognition(self):
        query = self.revenue_recognition_query()
        df = self.running_sql_query(query)
        self._store_datatype_parquet(df=df,
                                     filename="revenue_recognition",
                                     folder_name="revenue_recognition")

    def _store_datatype_parquet(self, df: pd.DataFrame, filename: str, folder_name: str):
        final_path = f"{self.destination_path}{self.spacing_bar}{folder_name}{self.spacing_bar}"
        if not os.path.exists(final_path):
            os.makedirs(final_path)
        df.to_parquet(f"{final_path}{self.spacing_bar}{filename}.parquet",
                      engine='fastparquet', index=False)

    def run(self):
        global invoices, reporting_periods
        invoices = pd.read_parquet(self.invoice_path, engine='fastparquet')
        reporting_periods = pd.read_parquet(self.reporting_periods_path, engine='fastparquet')

        self.etl_revenue_recognition()
