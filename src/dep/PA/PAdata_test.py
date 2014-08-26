import unittest

from src.dep.PA.PAdata import PAdata


class TestPAdata(unittest.TestCase):
	def setUp(self):
		from src.settings import setup
		self.settings = setup(dataset='default')

	def test_dataLooksGood(self):
		PA = PAdata(self.settings['PAfileLoc'])
		self.assertTrue( PA.count    == 5)
		self.assertTrue(PA.rowCount == 6)

		self.assertTrue(PA.sedentary== [161.0, 0.0, 0.0, 324.0, 43.0])
		self.assertTrue(PA.light    == [64.0, 0.0, 25.0, 191.0, 17.0])
		self.assertTrue(PA.mod      == [43.0, 0.0, 9.0, 40.0, 4.0])
		self.assertTrue(PA.mod_vig  == [0.0, 0.0, 0.0, 0.0, 0.0])
		self.assertTrue(PA.vig      == [0.0, 0.0, 0.0, 0.0, 0.0])
		self.assertTrue(PA.nonWear  == [27.0, 0.0, 233.0, 884.0, 227.0])
		self.assertTrue(PA.unknown  == [1145.4, 1440.0, 1173.0, 0.6, 1148.4])
		import datetime
		self.assertTrue(PA.time     == [datetime.datetime(2013, 6, 16, 0, 0), 
		                                datetime.datetime(2013, 6, 15, 0, 0), 
		                                datetime.datetime(2013, 6, 14, 0, 0), 
		                                datetime.datetime(2013, 6, 13, 0, 0), 
		                                datetime.datetime(2013, 6, 12, 0, 0)])

if __name__ == '__main__':
		suite = unittest.TestLoader().loadTestsFromTestCase(TestPAdata)
		unittest.TextTestRunner(verbosity=2).run(suite)
