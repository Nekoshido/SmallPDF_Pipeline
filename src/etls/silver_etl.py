import glob
import os
import re
from pathlib import Path
from typing import Tuple, AnyStr

from src.etls.base_etl import BaseETL
from src.files.invoice import Invoice
from src.files.reporting_periods import ReportingPeriods


class SilverETL(BaseETL):

    @property
    def input_path(self) -> str:
        return f'{Path(__file__).parent.parent.parent}/datalake/bronze/'

    @property
    def destination_path(self) -> str:
        return f'{Path(__file__).parent.parent.parent}/datalake/silver/'

    def etl_invoices(self, filename: str, folder_name: str):
        invoice = Invoice()
        dataframe = invoice.read_csv_schema(filename)
        df2 = invoice.infer_supply_date_start(dataframe)
        df3 = invoice.infer_supply_date_end(df2)
        df4 = invoice.filter_nulls_by_columns(df3)
        df5 = df4.loc[df3['plan'].isin(['yearly', 'monthly'])]
        df6 = invoice.correct_mispelled_country(df5)
        self._store_datatype_parquet(df6, filename, folder_name)

    def etl_reporting_periods(self, filename: str, folder_name: str):
        reporting_periods = ReportingPeriods()
        dataframe = reporting_periods.read_csv_schema(filename)
        df2 = reporting_periods.infer_reporting_period_start(dataframe)
        df3 = reporting_periods.infer_reporting_period_end(df2)
        self._store_datatype_parquet(df3, filename, folder_name)

    @staticmethod
    def find_folder_name(file_path: Tuple[AnyStr, AnyStr]) -> AnyStr:
        name_list = file_path[1].split(".")[0].split("_")
        return '_'.join([element for element in name_list if not bool(re.search(r'\d', element))])

    def run(self):
        for filename in glob.iglob(self.input_path + '**/**', recursive=True):
            if filename.endswith('.csv'):
                file_path = os.path.split(filename)
                folder_name = self.find_folder_name(file_path)
                if folder_name == 'invoices':
                    self.etl_invoices(filename, folder_name)
                elif folder_name == 'reporting_periods':
                    self.etl_reporting_periods(filename, folder_name)
