__author__ = 'tylarmurray'

from src.settings import QUALITY_LEVEL, DATA_TYPES, setup
from src.data.subject.Subject import Subject

class Dataset(object):
    """
    defines a set of data with multiple subjects
    """
    def __init__(self, settings, min_quality=QUALITY_LEVEL.acceptable, used_data_types=DATA_TYPES.all, trim=True, check=True):
        """
        :param min_quality: minimum quality level of data to be considered in the dataset
        """
        self.settings = settings

        self.pids = settings.get_pid_list()

        self.excluded = settings.get_exluded_list(min_level=min_quality , used_data=used_data_types)

        for pid in list(self.pids):  # note: need to use copy b/c we are modifying as we go
            if pid in self.excluded:
                self.pids.remove(pid)
                #print 'removing ', pid

        self.subject_data = list()

        for pid in self.pids:
            self.subject_data.append(Subject(setup(dataset=settings.dataset, dataLoc=settings.dataLoc, subjectN=pid)))
            if trim:
                self.subject_data[-1].trim_data()
            if check:
                self.subject_data[-1].integrity_check()

        print len(self), 'subjects loaded. pids = ', self.pids
        print 'excluding pids ', self.excluded


    def __len__(self):
        return len(self.subject_data)

    def __iter__(self):
        i = 0
        while True:
            try:
                yield self.subject_data[i]
                i += 1
            except IndexError:
                return