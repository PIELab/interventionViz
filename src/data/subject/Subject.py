from src.data.fitbit.Data import Data as FitbitData
from src.data.mAvatar.Data import Data as AvatarViews
from src.data.subject.MetaData import MetaData
from src.data.event.Data import Data as EventData
from src.settings import DATA_TYPES

__author__ = 'tylarmurray'


class Subject(object):
    """
    subject class for holding/accessing all data related to a study participant.
    """
    def __init__(self,
                 setup,
                 avatar_view_freq=60,
                 uses={
                     DATA_TYPES.fitbit: True,
                     DATA_TYPES.avatar_views: True,
                     DATA_TYPES.event: False
                 }
    ):
        """
        :param setup: settings setup object describing the subject to be set up
        :param uses: dict of used data
        """
        # load meta data
        self.meta_data = MetaData(setup.getFileName('metaData'))

        if DATA_TYPES.fitbit in uses and uses[DATA_TYPES.fitbit]:
            print 'FITBIT SETUP'
            # load fitbit data
            self.fitbit_data = FitbitData(setup.getFileName('fitbit'), meta_data=self.meta_data)

        if DATA_TYPES.avatar_views in uses and uses[DATA_TYPES.avatar_views]:
            # load viewLog data
            self.avatar_view_data = AvatarViews(setup.getFileName('viewLog'), meta_data=self.meta_data,
                                            frequency=avatar_view_freq)
        if DATA_TYPES.event in uses and uses[DATA_TYPES.event]:
            self.event_data = EventData(setup.get_file_name(DATA_TYPES.event), meta_data=self.meta_data)

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
        if self.fitbit_data.has_data_before_start():
            self.fitbit_data.trim_data()
        if self.avatar_view_data.has_data_before_start():
            self.avatar_view_data.trim_data()
        # TODO: add mMonitor trim

        if self.fitbit_data.has_data_after_end():
            self.fitbit_data.trim_data()
        if self.avatar_view_data.has_data_after_end():
            self.avatar_view_data.trim_data()
        # TODO: add mMonitor trim

        return

    def _has_data_before_start(self):
        """
        returns true if data exists before the meta-data study start
        """
        if (self.fitbit_data.has_data_before_start()
                or self.avatar_view_data.has_data_before_start()):  # TODO: add mMonitor data check
            return True
        else:
            return False

    def _has_data_after_end(self):
        """
        returns true if data exists after the meta-data study end
        """
        if (self.fitbit_data.has_data_after_end()
                or self.avatar_view_data.has_data_after_end()):  # TODO: add mMonitor data check
            return True
        else:
            return False