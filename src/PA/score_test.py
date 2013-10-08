import unittest
import src.PA.score as score

class TestScore(unittest.TestCase):
	def setUp(self):
		from src.settings import setup
		self.settings = setup(dataset='default')

	def test_postiveOnlyIsPositive(self):
		from src.PA.PAdata import PAdata
		data = PAdata(self.settings['PAfileLoc'])

		PAscore,date = score.segmentPAIntoDays(data,PAscoreFunction=score.getPAscore_postiveOnly)
		for s in PAscore:
			self.assertTrue(s >= 0)		

if __name__ == '__main__':
		suite = unittest.TestLoader().loadTestsFromTestCase(TestScatterPlot)
		unittest.TextTestRunner(verbosity=2).run(suite)
