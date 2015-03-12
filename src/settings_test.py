__author__ = '7yl4r'

import unittest
import warnings

from src.settings import DATA_TYPES, QUALITY_LEVEL
from src.settings import setup as settin

class basic_settings_tester(unittest.TestCase):
    def setUp(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            self.sett = settin(dataset='USF', data_loc='../subjects/', subject_n=0)  # TODO: use test data

    def test_exclude_on_usf_data(self):

        # avatar view data
        lis = self.sett.get_exluded_list(used_data=DATA_TYPES.avatar_views, min_level=QUALITY_LEVEL.good)
        self.assertIn(1, lis)
        self.assertIn(2, lis)
        self.assertIn(3, lis)
        self.assertIn(8, lis)
        self.assertIn(13, lis)
        self.assertIn(14, lis)
        self.assertIn(21, lis)
        #  ... and 26-44
        self.assertNotIn(10, lis)
        self.assertNotIn(11, lis)
        self.assertNotIn(12, lis)
        self.assertNotIn(15, lis)
        self.assertNotIn(49, lis)

        lis = self.sett.get_exluded_list(used_data=DATA_TYPES.avatar_views, min_level=QUALITY_LEVEL.acceptable)
        self.assertNotIn(1, lis)
        self.assertNotIn(8, lis)
        self.assertNotIn(10, lis)
        self.assertNotIn(11, lis)
        self.assertNotIn(12, lis)
        self.assertNotIn(13, lis)
        self.assertNotIn(15, lis)
        self.assertNotIn(26, lis)
        self.assertNotIn(28, lis)
        self.assertNotIn(32, lis)
        self.assertNotIn(44, lis)
        self.assertNotIn(49, lis)

        self.assertIn(2, lis)
        self.assertIn(3, lis)
        self.assertIn(14, lis)


        # fitbit data
        lis = self.sett.get_exluded_list(used_data=DATA_TYPES.fitbit, min_level=QUALITY_LEVEL.acceptable)
        self.assertNotIn(3, lis)
        self.assertNotIn(8, lis)
        self.assertNotIn(10, lis)
        self.assertNotIn(11, lis)
        self.assertNotIn(12, lis)
        self.assertNotIn(13, lis)
        self.assertNotIn(15, lis)
        self.assertNotIn(21, lis)
        self.assertNotIn(26, lis)
        self.assertNotIn(28, lis)
        self.assertNotIn(32, lis)
        self.assertNotIn(44, lis)
        self.assertNotIn(49, lis)

        self.assertIn(1, lis)
        self.assertIn(2, lis)
        self.assertIn(14, lis)



        # mMonitor data
        # TODO

        # all data

        lis = self.sett.get_exluded_list(used_data=DATA_TYPES.all, min_level=QUALITY_LEVEL.acceptable)
        self.assertNotIn(8, lis)
        self.assertNotIn(15, lis)
        self.assertNotIn(26, lis)

        self.assertIn(14, lis)
        self.assertIn(10, lis)

        lis = self.sett.get_exluded_list(used_data=DATA_TYPES.all, min_level=QUALITY_LEVEL.good)
        self.assertEqual(len(lis), 16)
