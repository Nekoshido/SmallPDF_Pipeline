from unittest import TestCase
import pandas as pd
import numpy as np
from pandas.util.testing import assert_frame_equal

from src.files.invoice import Invoice


class InvoiceTest(TestCase):
    invoice = Invoice()

    @staticmethod
    def create_initial_testing_df():
        data = {'plan': ['yearly', 'monthly', 'yearly', 'monthly', 'yearly'],
                'supply_date_start': ['2019-02-06', '2019-04-05', '2019-02-06', '2019-04-05', '2019-02-06'],
                'supply_date_end': ["2020-02-06 00:00:00", "2019-05-06 00:00:00", "2020-02-06 00:00:00",
                                    "2019-05-06 00:00:00", "2020-02-06 00:00:00"],
                'amount': [119, 12, 119, 12, 119],
                'country': [None, None, None, None, None]
                }

        return pd.DataFrame(data)

    @staticmethod
    def create_infer_date_end_testing_df():
        data = {'plan': ['yearly', 'monthly', 'yearly', 'monthly', 'yearly'],
                'supply_date_start': ['2019-02-06', '2019-04-05', '2019-02-06', '2019-04-05', '2019-02-06'],
                'supply_date_end': [np.datetime64("2020-02-06"), np.datetime64("2019-05-06"),
                                    np.datetime64("2020-02-06"), np.datetime64("2019-05-06"),
                                    np.datetime64("2020-02-06")],
                'amount': [119, 12, 119, 12, 119],
                'country': [None, None, None, None, None]
                }

        return pd.DataFrame(data)

    @staticmethod
    def create_infer_date_start_testing_df():
        data = {'plan': ['yearly', 'monthly', 'yearly', 'monthly', 'yearly'],
                'supply_date_start': [np.datetime64('2019-02-06'), np.datetime64('2019-04-05'),
                                      np.datetime64('2019-02-06'), np.datetime64('2019-04-05'),
                                      np.datetime64('2019-02-06')],
                'supply_date_end': ["2020-02-06 00:00:00", "2019-05-06 00:00:00", "2020-02-06 00:00:00",
                                    "2019-05-06 00:00:00", "2020-02-06 00:00:00"],
                'amount': [119, 12, 119, 12, 119],
                'country': [None, None, None, None, None]
                }

        return pd.DataFrame(data)

    def test_infer_supply_date_end(self):
        df = self.create_initial_testing_df()
        expected_result = self.create_infer_date_end_testing_df()
        df_test = self.invoice.infer_supply_date_end(df)
        assert_frame_equal(df_test, expected_result)

    def test_infer_supply_date_start(self):
        df = self.create_initial_testing_df()
        expected_result = self.create_infer_date_start_testing_df()
        df_test = self.invoice.infer_supply_date_start(df)
        assert_frame_equal(df_test, expected_result)

    def test_find_country(self):
        country = "grmany"
        expected_country = "Germany"
        test_country = self.invoice._find_country(country, 'name')
        assert expected_country == test_country

        country = "US"
        expected_country = "United States"
        test_country = self.invoice._find_country(country, 'alpha_2')
        assert expected_country == test_country

        country = "USA"
        expected_country = "United States"
        test_country = self.invoice._find_country(country, 'alpha_3')
        assert expected_country == test_country
