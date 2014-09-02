import unittest

from src.dep.PA import PAdata
from src.settings import DATA_TYPES
from src.settings import setup as settin

import src.dep.PA.score as score


class TestScore(unittest.TestCase):
    #def setUp(self):
    #    self.settings = settin()

    def test_postiveOnlyIsPositive(self):
        return

        #data = PAdata(self.settings.getFileName(type=DATA_TYPES['mMonitor']))
        #
        #PAscore,date = score.segmentPAIntoDays(data,PAscoreFunction=score.getPAscore_postiveOnly)
        #for s in PAscore:
        #    self.assertTrue(s >= 0)

if __name__ == '__main__':
        suite = unittest.TestLoader().loadTestsFromTestCase(TestScatterPlot)
        unittest.TextTestRunner(verbosity=2).run(suite)
