__author__ = 'tylarmurray'

import dateutil.parser    # for parsing datestrings
from datetime import timedelta
import csv        # for csv file reading
from datetime import datetime
from calendar import timegm
import pandas
from time import strptime, mktime

from src.data.Data import Data as base_data


class Data(base_data):
    """
    fitbit data class for loading, processing, and accessing step counts for one participant in various ways.
    """
    def __init__(self, minute_file, day_file=None, *args, **kwargs):
        """
        :param minute_file: location of file containing minute level step counts.
        :param day_file: location of file containing daily step counts (used only in data validation and (maybe) as a
            shortcut to daily aggregation).
        """
        self.loaded = False

        self.count = 0

        self.time_strs = list()  # list of times which the event occurs
        self.time = list()       # list of datetimes
        self.timestamp = list()  # list of timestamps which go along with events

        super(Data, self).__init__(minute_file, *args, **kwargs)

    def __len__(self):
        """
         returns the length of currently loaded data
        """
        if self.loaded:
            return len(self.time)
        else:
            raise IndexError('data not yet loaded, cannot get len.')

    def load_data(self, file_loc):
        """
        builds the lists of values corresponding to data samples.
        """
        with open(file_loc, 'rb') as csv_file:
            reader = csv.reader(csv_file, delimiter='\t')
            for r_i, row in enumerate(reader):
                if r_i == 0:  # skip header row
                    continue
                if len(row) > 0:
                    date = row[3]
                    time = row[4]
                    self.time_strs.append(date+' '+time.strip())
                    #print self.time_strs[-1]
                    self.timestamp.append(mktime(strptime(self.time_strs[-1], "%b. %d, %Y, %I:%M %p ")))
                    #print self.timestamp[-1]
                    self.time.append(datetime.fromtimestamp(self.timestamp[-1]))
                    #print self.time[-1]  # TODO: self.timestamps = ???
                else:
                    print 'WARN: empty row detected; assuming EOF'
                    break

        self.ts = pandas.Series(data=[1]*len(self.time), index=self.time)
        self.loaded = True
