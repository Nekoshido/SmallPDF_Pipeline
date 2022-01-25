import glob
import os
import shutil
from pathlib import Path

from src.etls.base_etl import BaseETL


class BronzeETL(BaseETL):

    @property
    def input_path(self) -> str:
        return f'{Path(__file__).parent.parent.parent}/input_data/'

    @property
    def destination_path(self) -> str:
        return f'{Path(__file__).parent.parent.parent}/datalake/bronze/'

    def run(self):
        for filename in glob.iglob(self.input_path + '**/**', recursive=True):
            if filename.endswith('.csv'):
                destination_file_name = f"{self.destination_path}/{os.path.split(filename)[1]}"
                if not os.path.exists(self.destination_path):
                    os.makedirs(self.destination_path)
                shutil.copy(filename, destination_file_name)




