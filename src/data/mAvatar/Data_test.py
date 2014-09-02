__author__ = '7yl4r'

import unittest
import warnings

from src.settings import DATA_TYPES
from src.settings import setup as settin
from src.data.mAvatar.Data import Data, DAY_TYPE
from src.data.subject.MetaData import MetaData

class basic_avatar_view_data_tester(unittest.TestCase):
    def setUp(self):
        with warnings.catch_warnings():
            warnings.simplefilter("ignore")
            sett = settin(dataset='USF', dataLoc='../subjects/', subjectN=10)  # TODO: use test data
            self.dat = Data(sett.get_file_name(type=DATA_TYPES.avatar_views),
                            meta_data=MetaData(sett.get_file_name(type=DATA_TYPES.metaData)))

    def test_day_type_works_on_test_data(self):
        self.assertEqual(self.dat.get_day_type('2013-09-04'), DAY_TYPE.active)
        self.assertEqual(self.dat.get_day_type('2013-09-05'), DAY_TYPE.sedentary)
        self.assertEqual(self.dat.get_day_type('2013-09-06'), DAY_TYPE.active)
        self.assertEqual(self.dat.get_day_type('2013-09-07'), DAY_TYPE.sedentary)
        self.assertEqual(self.dat.get_day_type('2013-09-08'), DAY_TYPE.active)
        self.assertEqual(self.dat.get_day_type('2013-09-09'), DAY_TYPE.sedentary)
        self.assertEqual(self.dat.get_day_type('2013-09-10'), DAY_TYPE.active)
        self.assertEqual(self.dat.get_day_type('2013-09-11'), DAY_TYPE.sedentary)
        self.assertEqual(self.dat.get_day_type('2013-09-12'), DAY_TYPE.active)
        self.assertEqual(self.dat.get_day_type('2013-09-13'), DAY_TYPE.sedentary)