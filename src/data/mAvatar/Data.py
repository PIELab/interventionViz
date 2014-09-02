__author__ = 'tylarmurray'

import dateutil.parser    #for parsing datestrings
import csv        #for csv file reading
from datetime import datetime
import calendar
import pandas
import warnings

from src.data.Data import Data as base_data

SEDENTARY = ['watchingTV', 'onComputer', 'videoGames']
ACTIVE = ['running', 'basketball', 'bicycling']
SLEEP = ['inBed']
SECONDS_PER_VIEW_UNIT = 3 # num of sec of constant view time before adding another viewTime
# NOTE: only actually in seconds (if div=1000) between points


class DAY_TYPE(object):
    active = 1
    sedentary = -1
    neutral = 0


class Data(base_data):
    """
    fitbit data class for loading, processing, and accessing step counts for one participant in various ways.
    """
    def __init__(self, file_name, frequency='raw', *args, **kwargs):
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

        super(Data, self).__init__(file_name, *args, **kwargs)
        self.loaded = True

    def __len__(self):
        """
         returns the length of currently loaded data
        """
        if self.loaded:
            return len(self.views)
        else:
            raise IndexError('data not yet loaded, cannot get len.')

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

    def load_data(self, file_loc):
        if self.meta_data is None:
            raise ValueError('meta data is needed to load mAvatar view data')
        else:
            self.loaded = True
            return self.load_minute_data(file_loc,
                                         calendar.timegm(self.meta_data.start.timetuple()),
                                         calendar.timegm(self.meta_data.end.timetuple()))

    def get_data(self, viewFileLoc, frequency=None):
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

    def get_day_type(self, date):
        """
        returns type for given day
            :param date: ISO 8601 date str of day in question (ie 2014-09-30)
            :returns: one of the values in DAY_TYPE
        """
        try:
            if sum(self.active_ts[date]) > 0:
                return DAY_TYPE.active
            elif sum(self.sedentary_ts[date]) > 0:
                return DAY_TYPE.sedentary
            else:
                warnings.warn(date + ' has no active nor sed values')
                return DAY_TYPE.neutral
        except TypeError as e:
            print 'ERROR getting day type for ', date
            print self.active_ts
            print self.active_ts[date]
            print self.sedentary_ts
            print self.sedentary_ts[date]
            raise e
    def get_day_type_ts(self, start=None, end=None):
        """
        returns a pandas time series with f=1day, and value as one of DAY_TYPE values
            :param start: datetime obj of first day to include in ts
            :param end: datetime obj of last day to include in ts
        """
        day_ts = self.get_day_ts(start,end)
        types = list()
        for day in day_ts.index:
            daystr = str(day.year) + '-' + str(day.month) + '-' + str(day.day)
            types.append(self.get_day_type(daystr))
        print types

        return pandas.Series(data=types, index=day_ts.index)

    def get_day_ts(self, start=None, end=None):
        """
        returns a pandas time series with f=1day, and value = sum of all seconds avatar is displayed
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


    def load_minute_data(self, view_file_loc, start_time, end_time, verbose=False):
        """
        loads minute-frequency time series
        """
        time_cursor = start_time  # time (minute) we are currently looking at (should be on the minute XX:00:00)
        count = 0  # number of minutes
        tims = list()  # times
        view = list()  # total of all views, regardless of type
        act = list()  # active interactions
        sed = list()  # sedentary interactions
        sle = list()  # sleeping interactions

        div = 1000  # divsor on the timestamps (1000 converts ms to s)

        if verbose: print 'reading', start_time, 'thru', end_time
        with open(view_file_loc, 'rb') as csvfile:
            spamreader = csv.reader(csvfile, delimiter=',')
            for row in spamreader:
                self.rowCount += 1
                if self.rowCount == 1:    #skip header row
                    continue
                if verbose: print ', '.join(row)    # print the raw data
                # print row        # print raw data matrix
                t0 = int(round(int(row[0]) / div))
                tf = int(round(int(row[1]) / div))
                ss = int(row[3] in SEDENTARY)  # 1 if row is sedentary, else 0
                aa = int(row[3] in ACTIVE)  # 1 if row is active, else 0
                sl = int(row[3] in SLEEP)  # 1 if row is sleeping, else 0

                while True:  # loop through this as long as needed to eat up this data row
                    if (time_cursor-start_time)%600 == 0:
                        if verbose: print time_cursor, '\r',

                    if time_cursor > end_time:  # if time cursor has passed end of study
                        warnings.warn('point @ t=' + str(t0) + '-' + str(tf) + ' ignored (after study end)')
                        break
                    elif t0 > time_cursor + 60:  # if not yet to logged point
                        tims.append(datetime.fromtimestamp(time_cursor))
                        sed.append(0)
                        act.append(0)
                        sle.append(0)
                        view.append(0)
                        count += 1
                        time_cursor += 60
                        continue
                    elif t0 < time_cursor:  # if in the middle of a logged point
                        if tf < time_cursor:  # logged point is entirely before this minute, ignore it?
                            warnings.warn('point @ t=' + str(t0) + '-' + str(tf) + 'ignored (before study start)')
                            break
                        else:
                            if count == 0:  # if this is the first point (data from before study start)
                                warnings.warn(str(time_cursor - t0) + 's before study_start ignored')

                            if tf > time_cursor + 60:  # if logged point extends beyond this minute
                                # logged point encapsulates the entire minute
                                tims.append(datetime.fromtimestamp(time_cursor))
                                sed.append(ss * 60)
                                act.append(aa * 60)
                                sle.append(sl * 60)
                                view.append(60)
                                count += 1
                                time_cursor += 60
                                continue
                            else:  # previously entered logged point ends in this minute
                                tims.append(datetime.fromtimestamp(time_cursor))
                                sec = tf - time_cursor
                                sed.append(ss * sec)
                                act.append(aa * sec)
                                sle.append(sl * sec)
                                view.append(sec)
                                count += 1
                                time_cursor += 60
                                break
                    elif tf > time_cursor + 60:  # if new logged point extends beyond this minute
                        tims.append(datetime.fromtimestamp(time_cursor))
                        sec = 60 - (t0 - time_cursor)
                        sed.append(ss * sec)
                        act.append(aa * sec)
                        sle.append(sl * sec)
                        view.append(sec)
                        count += 1
                        time_cursor += 60
                        continue
                    elif tf <= time_cursor + 60:  # if logged point is entirely encapsulated in this minute
                        tims.append(datetime.fromtimestamp(time_cursor))
                        sec = tf - t0
                        sed.append(ss * sec)
                        act.append(aa * sec)
                        sle.append(sl * sec)
                        view.append(sec)
                        count += 1
                        time_cursor += 60
                        break
                    else:
                        raise AssertionError("I don't know how we got here...")

        # fill in zeros until the study end
        while time_cursor < end_time:
            tims.append(datetime.fromtimestamp(time_cursor))
            sed.append(0)
            act.append(0)
            sle.append(0)
            view.append(0)
            count += 1
            time_cursor += 60

        self.ts = pandas.Series(data=view, index=tims)
        self.active_ts = pandas.Series(data=act, index=tims)
        self.sedentary_ts = pandas.Series(data=sed, index=tims)
        self.sleep_ts = pandas.Series(data=sle, index=tims)
        print str(count) + ' minutes loaded'

    def getRawData(self, viewFileLoc):
        ''' returns a data set with one point at each visibility changed event '''
        # read in csv
        #loadingDisplay=""    # this is a simple string to print so you know it's working
        #updateFreq = 100    # how many items per display update?
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

                #if self.count % updateFreq == 0:
                #    loadingDisplay+="|"
                #    print loadingDisplay
        print str(self.count)+' datapoints loaded from '+str(self.rowCount)+' rows.'
        return self
