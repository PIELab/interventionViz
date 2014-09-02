# this file defines setup methods and configuration options 

HIGHEST_P_NUMBER = 50

QUALITY_LEVEL = dict(good=3, acceptable=2, partial=1, bad=0)
# good         : no issue observed with data
# acceptable : some issues observed, but data should still be okay in normal analysis
# partial    : some data may be usable, but special analysis may be required
# bad        : there isn't even enough here to use some of it.

DATA_TYPES = dict(avatar_views='viewLog', mMonitor='mMonitor', fitbit='fitbit', metaData='metaData')


class setup:
# performs needed setup for scripts & returns dictionary with settings
#     paramters:
#        dataset - name of dataset to use
#        dataLoc - relative location of participant folders
#
#    returned settings dict items:
#        interactionFileLoc - relative location of interaction data file
#        PAfileLoc          - relative location of physical activity data file

    def __init__(self,dataset='test',dataLoc="./data/",subjectN=None):
        DEFAULT_PARTICIPANT_NUM = 1
        # load appropriate setup function for chosen dataset
        if dataset == 'default':
            self.pid,interactFile,PAfile = self.setupTestData(DEFAULT_PARTICIPANT_NUM)
        elif dataset == 'test' or dataset == 'sample':
            self.pid,interactFile,PAfile = self.setupTestData(subjectN)
        elif dataset == 'USF':
            dataLoc = "../subjects/"
            if subjectN==None:
                self.pid,interactFile,PAfile = self.setupUSFData(self.getParticipantNum())
            else:
                self.pid = str(subjectN)
                self.pid,interactFile,PAfile = self.setupUSFData(subjectN)
        else:
            raise InputError('bad dataset name "'+str(dataset)+'" in settings')

        self.dataLoc = dataLoc
            
        interactFile = dataLoc+self.pid+'/'+interactFile;
        PAfile    = dataLoc+self.pid+'/'+PAfile;
        
        self.dataset = dataset
        self.settings = dict(interactionFileLoc=interactFile,
                    PAfileLoc=PAfile)
                    
    def __getitem__(self,item):
        ''' this is to maintain backwards compatibility '''
        return self.settings[item]
        
    def getFileName(self,type):
        if self.dataset == 'USF':
            prefix = self.dataLoc+self.pid+'/'
            if type == 'viewLog':
                return prefix + "viewTimes.txt"
            elif type == 'mMonitor':
                return prefix + "daily_totals.txt"
            elif type == 'fitbit':
                return prefix + "minuteSteps.csv"
            elif type == 'metaData':
                return prefix + "metaData.csv"
            else:
                raise ValueError('unknown data type "'+str(type)+'"')
        elif self.dataset == 'test':
            prefix = self.dataLoc + self.pid+'/'
            raise NotImplementedError("getFileName('test') not yet implemented")
        else:
            raise ValueError('dataset type "'+str(self.dataset)+'" not recognized')

    def get_pid_list(self, dataset=None):
        set = dataset or self.dataset
        if set == 'USF':
            return [1,2,3,8,10,11,12,13,14,15,21,26,28,32,44,49]  # TODO: add more... <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
        else:
            raise NotImplementedError("cannot get pid list for unknown set " + str(set))

    def get_num_of_participants(self, dataset=None):
        set - dataset or self.dataset
        return len(self.get_pid_list(set))

    def get_exluded_list(self, used_data, min_level=QUALITY_LEVEL['acceptable'], dataset=None):
        """
        returns a list of participants to exclude for analysis based on hard-coded manual quality assessment data

        :param used_data: a list of specifiers indicating which data is to be used in the analysis (that way we can
            exclude subjects with bad data for those fields), use constants defined in DATA_TYPES.
        :param min_level: minimum quality level to include in analysis
        """
        set = dataset or self.dataset
        excludes = [False]*int(self.get_num_of_participants(set))
        # shorthand defs:
        g = QUALITY_LEVEL['good']
        a = QUALITY_LEVEL['acceptable']
        p = QUALITY_LEVEL['partial']
        b = QUALITY_LEVEL['bad']

        if set == 'USF':
            if DATA_TYPES['fitbit'] in used_data:
                qual = [b,b,g,a,g,g,a,g,b,g,a,g,g,a,g,a]  # TODO: add more... <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                for pnum in range(len(excludes)):  # should be len-1?
                    if qual[pnum] >= min_level:
                        excludes[pnum] = True

            if DATA_TYPES['mMonitor'] in used_data:
                qual = [b,b,p,a,p,p,p,p,b,a,b,a,b,b,b,b]  # TODO: add more... <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                for pnum in range(len(excludes)):  # should be len-1?
                    if qual[pnum] >= min_level:
                        excludes[pnum] = True

            if DATA_TYPES['avatar_views'] in used_data:
                qual = [b,b,g,a,g,g,a,g,b,g,a,g,g,a,g,a]  # TODO: add more... <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                for pnum in range(len(excludes)):  # should be len-1?
                    if qual[pnum] >= min_level:
                        excludes[pnum] = True
        else:
            raise NotImplementedError("cannot get exclusions for unknown set " + str(set))

        ex = list()
        subs = self.get_pid_list(set)
        for pnum in range(len(excludes)): # should be len-1?
            if excludes[pnum]:
                ex.append(subs[pnum])
        return ex


    ### PRIVATE METHODS ###

    # setup details for test dataset
    def setupTestData(self,n):
        if int(n) == 1:
            pid = "test1"
            viewLogFile = "dataLog.txt"
            PAfile = 'miles_DAILY_TOTALS.txt'
        elif int(n) == 2:
            pid = "test2"
            viewLogFile = "mirrorMe/dataLog3.txt"
            PAfile = 'miles_DAILY_TOTALS_fixed.txt'
        else:
            raise InputError('test PID in settings not recognized for particpant #'+str(n))
        return [pid,viewLogFile,PAfile]
        
    # detailed setup information for USF dataset
    def setupUSFData(self,n):
        '''
        DEPRECIATED!!! old way of getting the file names for USF dataset use getFileName() now
        '''
        pid = str(n)
        viewLogFile = 'viewTimes.txt'
        PAfile = 'daily_totals.txt'
        return [pid,viewLogFile,PAfile]
        
    def getParticipantNum(self):
        print 'Enter participant number.'
        return raw_input()


class InputError(Exception):
    # Exception raised for errors in the input.
    def __init__(self, value):
        self.value = value
    def __str__(self):
        return repr(self.value)
        

