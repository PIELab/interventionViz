__author__ = 'tylarmurray'

import dateutil.parser    # for parsing datestrings
from datetime import timedelta
import csv        # for csv file reading
from datetime import datetime
from calendar import timegm
import pandas

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

        self.rowCount = 0
        self.count = 0

        self.time = list()
        self.timestamp = list()

        self.steps = list()  # time-series list of steps, frequency depends on time-scale passed to data getter

        super(Data, self).__init__(minute_file, *args, **kwargs)

    def __len__(self):
        """
         returns the length of currently loaded data
        """
        if self.loaded:
            return len(self.steps)
        else:
            raise IndexError('data not yet loaded, cannot get len.')

    def load_data(self, PAfileLoc):
        """
        builds the lists of values corresponding to data samples.
        """
        self.loaded = True
        return self.getMinuteLevelData(PAfileLoc)

    def getDailyData(self, PAfileLoc):
        with open(PAfileLoc, 'rb') as csvfile:
            currentDay = None
            spamreader = csv.reader(csvfile,delimiter=',')
            for row in spamreader:
                if self.rowCount==0: # skip header row
                    self.rowCount+=1
                    continue
                self.rowCount+=1

                time = getFitbitStrDate(row[0])

                if currentDay != time.day:
                    # start accumulating on new day
                    currentDay = time.day
                    self.time.append(time)
                    self.steps.append(0)
                for min in range(0,59):
                    self.steps[-1] += (int( row[1+min] ))
                    self.count += 1
        return self.steps

    def get_day_sum(self, date):
        """
        returns a sum of all minute level samples for a given day, specified by ISO 8601 date string
        :param data: ISO 8601 date string (ie: '2014-09-30')
        """
        return sum(self.ts[date])

    def get_day_ts(self, start=None, end=None):
        """
        returns pandas time series of value sums over each day
        :param start: datetime obj of first day to include in ts
        :param end: datetime obj of last day to include in ts
        """
        ts = self.ts.resample('D', how='sum')
        if start is not None:
            for i in ts.index:
                if i.to_datetime() < start:
                    ts.pop(i)

        if end is not None:
            for i in ts.index:
                if i > end:
                    ts.pop()
        # print ts
        return ts

    def getMinuteLevelData(self, PAfileLoc):
        with open(PAfileLoc, 'rb') as csvfile:
            spamreader = csv.reader(csvfile,delimiter=',')
            for row in spamreader:
                if self.rowCount==0: # skip header row
                    self.rowCount+=1
                    continue
                self.rowCount+=1

                timestr = row[0]
                # fix the date formatting...
                date, time, ampm = timestr.split()
                m,d,y = date.split('/')
                time = time.zfill(8)
                m = m.zfill(2)
                d = d.zfill(2)
                y = y.zfill(4)
                newTimeStr = y+m+d+'T'+time+ampm

                time = datetime.strptime(newTimeStr, "%Y%m%dT%I:%M:%S%p")

                for minn in range(0, 59):
                    time += timedelta(seconds=1 * 60)
                    self.time.append(time)
                    self.timestamp.append(timegm(time.utctimetuple()))

                    self.steps.append(int(row[1 + minn]))
                    self.count += 1

        self.ts = pandas.Series(data=self.steps, index=self.time)

        return self.ts

def getFitbitStrDate(timeString):
    """
    returns a datetime given fitbit's wierd time string.
    """
    date, time, ampm = timeString.split()
    m,d,y = date.split('/')
    time = time.zfill(8)
    m = m.zfill(2)
    d = d.zfill(2)
    y = y.zfill(4)
    newTimeStr = y+m+d+'T'+time+ampm
    return datetime.strptime(newTimeStr, "%Y%m%dT%I:%M:%S%p")
