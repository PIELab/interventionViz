import unittest

from src.dep.interaction import interactionData

import src.dep.interaction.score as score


class TestScore(unittest.TestCase):
	def setUp(self):
		from src.settings import setup
		self.settings = setup(dataset='default')

	def test_interactionSegmentation(self):
		interact = interactionData(self.settings['interactionFileLoc'])

		interactScore,interactDate = score.segmentInteractionIntoDays(interact)
		self.assertTrue(len(interactDate) == len(interactScore))
		print 'interactScore='+str(interactScore)
#		import datetime
		print 'interactDate ='+str(interactDate)
#		self.assertTrue(interactDate == [datetime.datetime(2013, 6, 11, 23, 15, 4), datetime.datetime(2013, 6, 12, 23, 38, 9), datetime.datetime(2013, 6, 13, 23, 1, 46), datetime.datetime(2013, 6, 14, 22, 43, 16), datetime.datetime(2013, 6, 15, 23, 46, 3), datetime.datetime(2013, 6, 16, 18, 44, 2), datetime.datetime(2013, 6, 17, 20, 21, 23)])
		self.assertTrue(interactScore == [14, -16, 6, -2, 32])		

if __name__ == '__main__':
		suite = unittest.TestLoader().loadTestsFromTestCase(TestScatterPlot)
		unittest.TextTestRunner(verbosity=2).run(suite)
