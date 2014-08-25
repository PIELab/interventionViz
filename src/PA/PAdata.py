# this file defines a data object for physical activity data

import dateutil.parser    #for parsing datestrings
from datetime import timedelta
import csv        #for csv file reading
from datetime import datetime
from calendar import timegm

DEFAULT_METHOD = 'mMonitor'
DEFAULT_TIMESCALE = 'daily'

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

class PAdata:
    def __init__(self,PAfile=None, method=DEFAULT_METHOD, timeScale=DEFAULT_TIMESCALE):
        self.loaded = False
    
        self.time = list()
        self.timestamp = list()
        
        self.steps = list() # time-series list of steps, frequency depends on time-scale passed to data getter

        # daily intensity estimations
        self.nonWear = list()
        self.sedentary = list()
        self.light = list()
        self.mod   = list()
        self.vig   = list()
        self.mod_vig = list()
        self.unknown = list()

        self.rowCount = 0
        self.count = 0
        
        if PAfile != None:
            self.sourceFile = PAfile
            self.getData(PAfile,method,timeScale)
            self.loaded = True 
            
    def __len__(self):
        return self.count
    
    def reset(self):
        ''' 
        clears all data in the object and resets counters
        '''
        self = PAdata(self.sourceFile)

    def getData(self, PAfileLoc, method=DEFAULT_METHOD, timeScale=DEFAULT_TIMESCALE):
        '''
        results in a list of values corresponding to days in the study. 
        Dates of the days are included in 'self.time'.
        '''
        if self.loaded == True:
            self.reset()
            
        if timeScale == 'daily':
            self.getDailyData(PAfileLoc,method)
        elif timeScale == 'minute':
            self.getMinuteLevelData(PAfileLoc,method)
        else:
            raise ValueError('data timescale "'+str(timeScale)+'" not recognized')
            
    ### PRIVATE METHODS ###
            
    def getMinuteLevelData(self,PAfileLoc,method=DEFAULT_METHOD):
        if method=='fitbit':
            self.getMinuteLevelFitbitData(PAfileLoc)
        elif method=='mMonitor':
            raise NotImplementedError('minute timescale data getter for mMonitor not yet implemented')

    def getDailyData(self, PAfileLoc, method=DEFAULT_METHOD):
        if method=='fitbit':
            self.getDailyLevelFitbitData(PAfileLoc)
        elif method=='mMonitor':
            self.getDailymMonitorData(PAfileLoc)
        else:
            raise ValueError('data getter method "'+str(method)+'" not recognized')
        
    def getDailyLevelFitbitData(self, PAfileLoc):
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
        
    def getMinuteLevelFitbitData(self, PAfileLoc):
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