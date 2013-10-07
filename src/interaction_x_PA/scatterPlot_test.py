import unittest
import src.interaction_x_PA.scatterPlot as sPlot

class TestScatterPlot(unittest.TestCase):
	def setUp(self):
		from src.settings import setup
		self.settings = setup(dataset='default')

	def test_interactionSegmentation(self):

		from src.interaction.timeSeries.multicolorBars import data as interactionData
		interact = interactionData()
		interact.getData(self.settings['interactionFileLoc'])
		interactDate,interactScore = sPlot.segmentInteractionIntoDays(interact)

		self.assertTrue(self.settings!=None)

if __name__ == '__main__':
		suite = unittest.TestLoader().loadTestsFromTestCase(TestSequenceFunctions)
		unittest.TextTestRunner(verbosity=2).run(suite)
