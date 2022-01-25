import pandas as pd
import numpy as np
import pycountry as pc

from src.files.base_event import BaseEvent

from difflib import SequenceMatcher
from typing import List


class Invoice(BaseEvent):

    def infer_supply_date_start(self, df: pd.DataFrame) -> pd.DataFrame:
        return self._infer_date_format(df, 'supply_date_start', '%Y-%m-%d')

    def infer_supply_date_end(self, df: pd.DataFrame) -> pd.DataFrame:
        return self._infer_date_format(df, 'supply_date_end', '%Y-%m-%d %H:%M:%S')

    @staticmethod
    def _get_most_similar(word: str, wordlist: List):
        top_similarity = 0.0
        most_similar_word = word
        for candidate in wordlist:
            similarity = SequenceMatcher(a=word, b=candidate).ratio()
            if similarity > top_similarity:
                top_similarity = similarity
                most_similar_word = candidate
        return most_similar_word

    def _find_country(self, country, atr: str) -> str:
        list_country = [getattr(c, atr) for c in list(pc.countries)]
        best_candidate = self._get_most_similar(country, list_country)
        kwargs = {atr: best_candidate}
        return pc.countries.get(**kwargs).name

    def _country_switcher_corrector(self, country: str):
        if country != country or not country:
            return None
        if 1 < len(country) < 4:
            country = country.upper()
            return self._find_country(country, f'alpha_{len(country)}')
        else:
            country = country.lower().capitalize()
            return self._find_country(country, 'name')

    def correct_mispelled_country(self, df: pd.DataFrame) -> pd.DataFrame:
        df["country"].fillna(np.nan).replace([np.nan], ["None"])
        df['country'] = df['country'].apply(self._country_switcher_corrector)
        return df

    @staticmethod
    def filter_nulls_by_columns(df: pd.DataFrame):
        columns_not_nulls = ['plan', 'supply_date_start', 'supply_date_end', 'amount']
        for column in columns_not_nulls:
            df = df[~df[column].isnull()]
        return df

    @property
    def column_dict(self):
        return {'plan': np.object,
                'supply_date_start': np.object,
                'supply_date_end': np.object,
                'amount': np.float64,
                'country': np.object}

    @property
    def separator(self) -> str:
        return ";"
