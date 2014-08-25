__author__ = 'tylarmurray'

import dateutil.parser    #for parsing datestrings
import csv        #for csv file reading
from datetime import datetime

from src.Data import Data as base_data

SECONDS_PER_VIEW_UNIT = 3 # num of sec of constant view time before adding another viewTime
# NOTE: only actually in seconds (if div=1000) between points

class Data(base_data):
    """
    fitbit data class for loading, processing, and accessing step counts for one participant in various ways.
    """
    def __init__(self, file_name, frequency='raw'):
        """
        :param file_name: file to load data from
        :param frequency: string indicating desired frequency of samples. Can be:
            * daily : 1 sample/day
            * minute: 1 sample/min
            * raw: 1 time per sample (VERY different, not really a frequency)
        """
        self.loaded = False

        self.rowCount = 0
        self.count = 0
        self.startTime = None

        # time-series style data:
        self.frequency = frequency
        self.time = list()
        self.timestamp = list()
        self.views = list()  # time-series list views, frequency depends on time-scale passed to data getter

        self.viewMarkerColor = list()  # list of marker colors to show at self.viewTimes

        # the folowing are all lists for storing the 'raw' data,
        # which has two points at each visibiltiyChanged event;
        # one for previous state and one for new state.
        self.viewTimes = list()    # ???
        self.t = list()     # raw time value
        self.x = list()     # datetime value (x axis)
        self.p1 = list()    # passives
        self.p2 = list()
        self.p3 = list()
        self.a1 = list()    # actives
        self.a2 = list()
        self.a3 = list()
        self.sl = list()    # sleep?
        self.ER = list()    # error?
        self.v  = list()    # +/- active/sedentary value

        super(Data, self).__init__(file_name)
        self.loaded = True

    def __len__(self):
        """
         returns the length of currently loaded data
        """
        if self.loaded:
            return len(self.views)
        else:
            raise IndexError('data not yet loaded, cannot get len.')

    def get_earliest_sample(self):
        try:
            return self._earliest
        except AttributeError:
            i = self.x.index(min(self.x))
            return dict(t=self.x[i])

    def get_latest_sample(self):
        try:
            return self._latest
        except AttributeError:
            i = self.x.index(max(self.x))
            return dict(t=self.x[i])


    def reset(self, frequency=None):
        '''
        clears all data in the object and resets counters
        '''
        freq = frequency or self.frequency
        self = Data(self.minute_file, frequency=freq)

    def getColorFor(self,tag):
        ''' returns color marker 'r' for active, 'b' for sedentary, gray for sleeping or null. '''
        if (tag == 'onComputer'
          or tag == 'videoGames'
          or tag == 'watchingTV'):
            return 'b'
        elif (tag == 'bicycling'
          or tag == 'basketball'
          or  tag == 'running'):
            return 'r'
        elif tag == 'inBed':
            return '0.5'
        elif tag == 'null':
            return '0.25'
        else:
            raise ValueError('unidentified activity tag "'+str(tag)+'"')

    def logPoint(self,t,tag,value):
        # t = time from start of study
        #hrs = float(t)/60.0/60.0
        #self.x.append(hrs)
        self.t.append(t)
        self.x.append(datetime.fromtimestamp(t))
        self.p1.append(0)
        self.p2.append(0)
        self.p3.append(0)
        self.a1.append(0)
        self.a2.append(0)
        self.a3.append(0)
        self.sl.append(0)
        self.ER.append(0)

        self.count+=1

        if value==0:
            self.v.append(0)
            return
        else:
            # passives are negative
            if tag == 'onComputer':
                self.p1[-1] = -1
            elif tag == 'videoGames':
                self.p2[-1] = -1
            elif tag == 'watchingTV':
                self.p3[-1] = -1
            # actives are positive
            elif tag == 'bicycling':
                self.a1[-1] = 1
            elif tag == 'basketball':
                self.a2[-1] = 1
            elif tag == 'running':
                self.a3[-1] = 1
            elif tag == 'inBed':
                self.sl[-1] = (-0.5)
            else:    #ERROR
                self.ER[-1] = (0.5)

        self.v.append(self.p1[-1]+self.p2[-1]+self.p3[-1]+self.a1[-1]+self.a2[-1]+self.p3[-1]+self.sl[-1]+self.ER[-1])

    def load_data(self, viewFileLoc, frequency=None):
        '''
        return the interaction data in given format.
        params:
            :param viewFileloc: ("viewTimes") file path
            :param frequency: granularity of data returned
                >> raw   : points for each visibility changed event
                >> daily : one point per day with total views for that day
                >> minute: 1 sample/min
        '''
        timeScale = frequency or self.frequency

        if self.loaded:
           self.reset(frequency=timeScale)

        if timeScale == 'raw':
            # return data points in default format
            return self.getRawData(viewFileLoc)
        elif timeScale == 'daily':
            # return daily total interactions
            return self.getDailyData(viewFileLoc)
        else:
            raise NotImplementedError('timeScale "'+str(timeScale)+'" not recognized')


    def getDailyData(self,viewFileLoc):
        ''' returns a time series list with f=1day, and value = sum of all seconds avatar is displayed '''
        currentDay = None
        div = 1000    # to reduce the amount of data (we don't really need millisecond-accurate readings)
        with open(viewFileLoc, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                if self.rowCount==0: #skip header row
                    self.rowCount+=1
                    continue
                t0 = int(round(int(row[0])/div))
                tf = int(round(int(row[1])/div))

                if datetime.datetime.fromtimestamp(tf).day != currentDay:
                    self.views.append(0)
                    currentDay = datetime.datetime.fromtimestamp(tf).day

                self.views[-1] += tf - t0

                self.rowCount+=1
        print sum(self.views), 's of view time across ', len(self.views), ' days loaded.'
        return self.views

    def getRawData(self, viewFileLoc):
        ''' returns a data set with one point at each visibility changed event '''
        # read in csv
        loadingDisplay=""    # this is a simple string to print so you know it's working
        updateFreq = 2000    # how many items per display update?
        div = 1000    # to reduce the amount of data (we don't really need millisecond-accurate readings)

#        print "loading", viewFileLoc
        with open(viewFileLoc, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                if self.rowCount==0:    #skip header row
                    self.rowCount+=1
                    continue
                if self.rowCount==1:    # set startTime
                    self.startTime = int(round(int(row[0])/div))
                self.rowCount+=1
                # print ', '.join(row)    # print the raw data
                # print row        # print raw data matrix
                t0 = int(round(int(row[0])/div))
                tf = int(round(int(row[1])/div))
                self.logPoint(t0-1,0,0) # 0 before
                self.logPoint(t0,row[3],1) #value @ start
                # 1 value / n sec in middle for viewCount
                t = t0
                while t < tf:
                    self.viewTimes.append(t)
                    self.viewMarkerColor.append(self.getColorFor(row[3]))
                    t += SECONDS_PER_VIEW_UNIT
                self.logPoint(tf,row[3],1) #value @ end
                self.logPoint(tf+1,0,0) # 0 after

                if self.count % updateFreq == 0:
                    loadingDisplay+="|"
                    print loadingDisplay
        print str(self.count)+' datapoints loaded from '+str(self.rowCount)+' rows.'
        return self

