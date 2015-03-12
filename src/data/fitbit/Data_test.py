__author__ = '7yl4r'

import unittest
from datetime import datetime

from src.settings import DATA_TYPES
from src.settings import setup as settin
from src.data.fitbit.Data import Data as FitbitData

class basic_fitbit_data_tester(unittest.TestCase):
    def setUp(self):
        sett = settin(dataset='USF', data_loc='../subjects/', subject_n=15)  # TODO: use dataset='test'
        self.dat = FitbitData(sett.get_file_name(type=DATA_TYPES.fitbit))
        self.days = ['2013-11-21',
                     '2013-11-22',
                     '2013-11-23',
                     '2013-11-24',
                     '2013-11-25',
                     '2013-11-26',
                     '2013-11-27',
                     '2013-11-28',
                     '2013-11-29',
                     '2013-11-30',
                     '2013-12-01',
                     '2013-12-02']
        self.steps = [17570,
                      11703,
                      8376,
                      2460,
                      17674,
                      7472,
                      5016,
                      10533,
                      4876,
                      5799,
                      3506,
                      24407]

    def test_day_sum_equals_resample_sum(self):
        daily = self.dat.get_day_ts(start=datetime(2013, 11, 21, 0, 0), end=datetime(2013, 12, 2, 0, 0))

        for i in range(len(daily)):
            self.assertAlmostEqual(daily[i], self.dat.get_day_sum(self.days[i]))

    def test_resample_minutes_almost_equals_daily_sum(self):
        THRESH = 400  # number of steps allowed to be miscounted in daily sum (WHY???)


        print self.dat.ts.head()

        for i in range(len(self.steps)):
            summ = self.dat.get_day_sum(self.days[i])
            diff = abs(summ - self.steps[i])
            self.assertLess(diff, THRESH, msg='day sum ' + str(summ) + ' not w/in '
                                              + str(THRESH) + ' steps of ' + str(self.steps[i]))