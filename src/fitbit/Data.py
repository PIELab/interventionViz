__author__ = 'tylarmurray'

import dateutil.parser    #for parsing datestrings
from datetime import timedelta
import csv        #for csv file reading
from datetime import datetime
from calendar import timegm

from src.Data import Data as base_data

class Data(base_data):
    """
    fitbit data class for loading, processing, and accessing step counts for one participant in various ways.
    """
    def __init__(self, minute_file, day_file=None, frequency="minute"):
        """
        :param settings: a dictionary (or settings class) with at least the following values:
            * dataLoc
            * pNum
        :param frequency: string indicating desired frequency of samples. Can be:
            * daily
            * minute
        """
        self.loaded = False

        self.rowCount = 0
        self.count = 0

        self.time = list()
        self.timestamp = list()

        self.steps = list() # time-series list of steps, frequency depends on time-scale passed to data getter

        self.frequency = frequency

        super(Data, self).__init__(self.minute_file)

    def __len__(self):
        """
         returns the length of currently loaded data
        """
        if self.loaded:
            return len(self.steps)
        else:
            raise IndexError('data not yet loaded, cannot get len.')

    def load_data(self, PAfileLoc, timeScale=None):
        '''
        builds the lists of values corresponding to data samples.
        '''
        time_scale = timeScale or self.frequency

        if self.loaded == True:
            self.reset()

        if time_scale == 'daily':
            self.getDailyData(PAfileLoc)
            self.loaded = True
        elif time_scale == 'minute':
            self.getMinuteLevelData(PAfileLoc)
            self.loaded = True
        else:
            raise ValueError('data timescale "' + str(time_scale) + '" not recognized')

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

                for min in range(0,59):
                    self.time.append( time+timedelta(seconds=1*60) )
                    self.timestamp.append(timegm(self.time[-1].utctimetuple()))

                    self.steps.append(int( row[1+min] ))
                    self.count += 1
        return self

    def getDailymMonitorData(self, PAfileLoc):
        print "loading", PAfileLoc
        # read in csv
        loadingDisplay=""    # this is a simple string to print so you know it's working
        updateFreq = 10    # how many items per display update?

        with open(PAfileLoc, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')

            for row in spamreader:
                if self.rowCount==0:    #skip header row
                    self.rowCount+=1
                    continue
                self.rowCount+=1
                # print ', '.join(row)    # print the raw data
                # print row        # print raw data matrix

                self.time.append(dateutil.parser.parse(row[1]))
                self.nonWear.append(float(row[3]))
                self.sedentary.append(float(row[4]))
                self.light.append(float(row[5]))
                self.mod.append(float(row[6]))
                self.vig.append(float(row[7]))
                self.mod_vig.append(float(row[8]))
                # 9 total min
                # 10 total hour
                self.unknown.append(float(row[11])*60)    # hrs->min

                self.count+=1
                if self.count % updateFreq == 0:
                    loadingDisplay+="|"
                    print loadingDisplay
        print 'done. '+str(self.count)+' datapoints loaded from '+str(self.rowCount)+' rows.'
        return self

    def get_earliest_sample(self):
        try:
            return self._earliest
        except AttributeError:
            i = self.time.index(min(self.time))
            return dict(t=self.time[i], v=self.steps[i])

    def get_latest_sample(self):
        try:
            return self._latest
        except AttributeError:
            i = self.time.index(max(self.time))
            return dict(t=self.time[i], v=self.steps[i])

def getFitbitStrDate(timeString):
    '''
    returns a datetime given fitbit's wierd time string.
    '''
    date, time, ampm = timeString.split()
    m,d,y = date.split('/')
    time = time.zfill(8)
    m = m.zfill(2)
    d = d.zfill(2)
    y = y.zfill(4)
    newTimeStr = y+m+d+'T'+time+ampm
    return datetime.strptime(newTimeStr, "%Y%m%dT%I:%M:%S%p")
