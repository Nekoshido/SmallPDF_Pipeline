from unittest import TestCase
import pandas as pd
import numpy as np
from pandas._testing import assert_frame_equal

from src.files.reporting_periods import ReportingPeriods


class InvoiceTest(TestCase):
    reporting_periods = ReportingPeriods()

    @staticmethod
    def create_initial_testing_df():
        data = {'reporting_period_start': ["2019-05-01 00:00:00", "2019-06-01 00:00:00", "2019-07-01 00:00:00",
                                           "2019-08-01 00:00:00", "2020-09-01 00:00:00"],
                'reporting_period_end': ["2019-06-01 00:00:00", "2019-07-01 00:00:00", "2019-08-01 00:00:00",
                                         "2019-09-01 00:00:00", "2019-10-01 00:00:00"],
                'reporting_period_length': [31, 30, 31, 30, 31]
                }
        return pd.DataFrame(data)

    @staticmethod
    def create_reporting_period_start_testing_df():
        data = {'reporting_period_start': [np.datetime64("2019-05-01 00:00:00"), np.datetime64("2019-06-01 00:00:00"),
                                           np.datetime64("2019-07-01 00:00:00"), np.datetime64("2019-08-01 00:00:00"),
                                           np.datetime64("2020-09-01 00:00:00")],
                'reporting_period_end': ["2019-06-01 00:00:00", "2019-07-01 00:00:00", "2019-08-01 00:00:00",
                                         "2019-09-01 00:00:00", "2019-10-01 00:00:00"],
                'reporting_period_length': [31, 30, 31, 30, 31]
                }
        return pd.DataFrame(data)

    @staticmethod
    def create_reporting_period_end_testing_df():
        data = {'reporting_period_start': ["2019-05-01 00:00:00", "2019-06-01 00:00:00", "2019-07-01 00:00:00",
                                           "2019-08-01 00:00:00", "2020-09-01 00:00:00"],
                'reporting_period_end': [np.datetime64("2019-06-01 00:00:00"), np.datetime64("2019-07-01 00:00:00"),
                                         np.datetime64("2019-08-01 00:00:00"), np.datetime64("2019-09-01 00:00:00"),
                                         np.datetime64("2019-10-01 00:00:00")],
                'reporting_period_length': [31, 30, 31, 30, 31]
                }
        return pd.DataFrame(data)

    def test_infer_supply_date_start(self):
        df = self.create_initial_testing_df()
        expected_result = self.create_reporting_period_start_testing_df()
        df_test = self.reporting_periods.infer_reporting_period_start(df)
        assert_frame_equal(df_test, expected_result)

    def test_infer_supply_end_start(self):
        df = self.create_initial_testing_df()
        expected_result = self.create_reporting_period_end_testing_df()
        df_test = self.reporting_periods.infer_reporting_period_end(df)
        assert_frame_equal(df_test, expected_result)

