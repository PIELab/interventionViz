__author__ = 'tylarmurray'

from src.settings import QUALITY_LEVEL, setup
from src.data.subject.Subject import Subject

class Dataset(object):
    """
    defines a set of data with multiple subjects
    """
    def __init__(self, settings, min_quality=QUALITY_LEVEL['acceptable'], trim=True, check=True):
        """
        :param min_quality: minimum quality level of data to be considered in the dataset
        """
        self.settings = settings

        self.pids = settings.get_pid_list()

        self.subject_data = list()

        for pid in self.pids:
            self.subject_data.append(Subject(setup(dataset=settings.dataset, dataLoc=settings.dataLoc, subjectN=pid)))
            if trim:
                self.subject_data[-1].trim_data()
            if check:
                self.subject_data[-1].integrity_check()