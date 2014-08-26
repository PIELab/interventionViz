__author__ = 'tylarmurray'

from src.fitbit.Data import Data as FitbitData
from src.mAvatar.Data import Data as AvatarViews
from src.subject.MetaData import MetaData

class Subject(object):
    """
    subject class for holding/accessing all data related to a study participant.
    """
    def __init__(self, setup):
        """
        :param setup: settings setup object describing the subject to be set up
        """
        # load meta data
        self.meta_data = MetaData(setup.getFileName('metaData'))

        # load fitbit data
        print 'subject init'
        self.fitbit_data = FitbitData(setup.getFileName('fitbit'), meta_data=self.meta_data)
        print self.fitbit_data

        # load viewLog data
        self.avatar_view_data = AvatarViews(setup.getFileName('viewLog'), meta_data=self.meta_data)


        # TODO: load mMonitor data

    def integrity_check(self):
        """
        checks data for strangeness, raises errors if encountered
        """
        if (self._has_data_after_end()
            or self._has_data_before_start()):
            raise AssertionError('data found outside study start/end bounds.')
        else:
            print 'data passes integrity check'

    def trim_data(self):
        """
        trims off any data which is:
            > prior to study start
            > after study end
        """
        if self._has_data_before_start():
            raise NotImplementedError('TODO: trim before')
        if self._has_data_after_end():
            raise NotImplementedError('TODO: trim after')

        return

    def _has_data_before_start(self):
        """
        returns true if data exists before the meta-data study start
        """
        if (self.fitbit_data.get_earliest_sample()['t'] < self.meta_data.start
            or self.avatar_view_data.get_earliest_sample()['t'] < self.meta_data.start):  # TODO: add mMonitor data check
            return True
        else:
            return False
    def _has_data_after_end(self):
        """
        returns true if data exists after the meta-data study end
        """
        if (self.fitbit_data.get_latest_sample()['t'] > self.meta_data.end
            or self.avatar_view_data.get_latest_sample()['t'] > self.meta_data.end):  # TODO: add mMonitor data check
            return True
        else:
            return False