__author__ = 'tylarmurray'

from src.fitbit.Data import Data as FitbitData

class Subject(object):
    """
    subject class for holding/accessing all data related to a study participant.
    """
    def __init__(self, setup):
        """
        :param setup: settings setup object describing the subject to be set up
        """
        # load fitbit data
        self.fitbit_data = FitbitData(setup.getFileName('fitbit'))

        # TODO: load viewLog data

        # TODO: load meta data

        # TODO: load mMonitor data

    def integrity_check(self):
        """
        checks data for strangeness
        """
        raise NotImplementedError()
