# this file defines setup methods and configuration options 

HIGHEST_P_NUMBER = 50


class QUALITY_LEVEL(object):
    """
    good         : no issue observed with data
    acceptable : some issues observed, but data should still be okay in normal analysis
    partial    : some data may be usable, but special analysis may be required
    bad        : there isn't even enough here to use some of it.
    """
    good = 3
    acceptable = 2
    partial = 1
    bad = 0


class DATA_TYPES(object):
    avatar_views = 0  # 'viewLog'
    mMonitor = 1  # 'mMonitor'
    fitbit = 2  # 'fitbit'
    metaData = 3  # 'metaData'

    all = [0, 1, 2, 3]


class setup(object):
# performs needed setup for scripts & returns dictionary with settings
#     paramters:
#        dataset - name of dataset to use
#        dataLoc - relative location of participant folders
#
#    returned settings dict items:
#        interactionFileLoc - relative location of interaction data file
#        PAfileLoc          - relative location of physical activity data file

    def __init__(self,dataset='test', data_loc="./data/", subject_n=None):
        # load appropriate setup function for chosen dataset
        self.dataset = dataset
        self.dataLoc = data_loc
        self.settings = dict()

        if subject_n is None:
            subject_n = self.getParicipantNum()

        if dataset == 'default':
            DEFAULT_PARTICIPANT_NUM = 1
            self.pid, interact_file, pa_file = self.setupTestData(DEFAULT_PARTICIPANT_NUM)
            self.settings["interactionFileLoc"] = data_loc+self.pid+'/'+interact_file
            self.settings["PAfileLoc"] = data_loc+self.pid+'/'+pa_file
        elif dataset == 'test' or dataset == 'sample':
            self.pid, interact_file, pa_file = self.setupTestData(str(subject_n))

            self.settings["interactionFileLoc"] = data_loc+self.pid+'/'+interact_file
            self.settings["PAfileLoc"] = data_loc+self.pid+'/'+pa_file
        elif dataset == 'USF':
            self.pid, interact_file, pa_file = self.setupUSFData(str(subject_n))

            self.settings["interactionFileLoc"] = data_loc+self.pid+'/'+interact_file
            self.settings["PAfileLoc"] = data_loc+self.pid+'/'+pa_file
        else:
            raise InputError('bad dataset name "'+str(dataset)+'" in settings')

    def __getitem__(self, item):
        ''' this is to maintain backwards compatibility '''
        return self.settings[item]
        
    def getFileName(self, type):
        """
        depreciated version of get_file_name which takes raw strings to specify data type
        """
        if type == 'viewLog':
            return self.get_file_name(DATA_TYPES.avatar_views)
        elif type == 'mMonitor':
            return self.get_file_name(DATA_TYPES.mMonitor)
        elif type == 'fitbit':
            return self.get_file_name(DATA_TYPES.fitbit)
        elif type == 'metaData':
            return self.get_file_name(DATA_TYPES.metaData)
        else:
            raise ValueError('unknown data type "'+str(type)+'"')

    def get_file_name(self, type):
        if self.dataset == 'USF':
            prefix = self.dataLoc+self.pid+'/'
            if type == DATA_TYPES.avatar_views:
                return prefix + "viewTimes.txt"
            elif type == DATA_TYPES.mMonitor:
                return prefix + "daily_totals.txt"
            elif type == DATA_TYPES.fitbit:
                return prefix + "minuteSteps.csv"
            elif type == DATA_TYPES.metaData:
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
        set = dataset or self.dataset
        return len(self.get_pid_list(set))

    def get_exluded_list(self, used_data=DATA_TYPES.all, min_level=QUALITY_LEVEL.acceptable, dataset=None):
        """
        returns a list of participants to exclude for analysis based on hard-coded manual quality assessment data

        :param used_data: a list of specifiers indicating which data is to be used in the analysis (that way we can
            exclude subjects with bad data for those fields), use constants defined in DATA_TYPES.
        :param min_level: minimum quality level to include in analysis
        """
        # make given list of data a list if you forgot to
        if not hasattr(used_data, "__iter__"):
            used_data = [used_data]

        set = dataset or self.dataset
        subs = self.get_pid_list(set)
        excludes = [False]*int(self.get_num_of_participants(set))
        # shorthand defs:
        g = QUALITY_LEVEL.good
        a = QUALITY_LEVEL.acceptable
        p = QUALITY_LEVEL.partial
        b = QUALITY_LEVEL.bad

        if set == 'USF':
            if DATA_TYPES.fitbit in used_data:
                #print 'checking for fitbit quality'
                qual = [b,b,g,a,g,g,a,g,b,g,a,g,g,a,g,a]  # TODO: add more... <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                for pnum in range(len(excludes)):  # should be len-1?
                    if qual[pnum] < min_level:
                        excludes[pnum] = True
                        # print "-" + str(subs[pnum]) + '|',
                    else:
                        pass # print str(subs[pnum]) + '|',
                #print '\n'

            if DATA_TYPES.mMonitor in used_data:
                #print 'checking for mMonitor quality'
                qual = [b,b,p,a,p,p,p,p,b,a,b,a,b,b,b,b]  # TODO: add more... <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                for pnum in range(len(excludes)):  # should be len-1?
                    if qual[pnum] < min_level:
                        excludes[pnum] = True
                        #print "-" + str(subs[pnum]) + '|',
                    else:
                        pass  # print str(subs[pnum]) + '|',
                #print '\n'


            if DATA_TYPES.avatar_views in used_data:
                #print 'checking avatar view quality'
                qual = [a,b,b,a,g,g,g,a,b,g,p,a,a,a,a,g]  # TODO: add more... <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<
                for pnum in range(len(excludes)):  # should be len-1?
                    if qual[pnum] < min_level:
                        excludes[pnum] = True
                        #print "-" + str(subs[pnum]) + '|',
                    else:
                        pass  # print str(subs[pnum]) + '|',
                #print '\n'

        else:
            raise NotImplementedError("cannot get exclusions for unknown set " + str(set))

        ex = list()
        for pnum in range(len(excludes)):
            if excludes[pnum]:
                ex.append(subs[pnum])
        #print 'excluded: ', ex
        return ex


    ### PRIVATE METHODS ###

    # setup details for test dataset
    def setupTestData(self, n):
        if int(n) == 1:
            pid = "test1"
            view_log_file = "dataLog.txt"
            pa_file = 'miles_DAILY_TOTALS.txt'
            return [pid, view_log_file, pa_file]
        elif int(n) == 2:
            pid = "test2"
            view_log_file = "mirrorMe/dataLog3.txt"
            pa_file = 'miles_DAILY_TOTALS_fixed.txt'
            return [pid, view_log_file, pa_file]

        elif int(n) == 3:
            pid = "controlIntervention"
            event_file = 'log.txt'
            pa_file = 'minuteSteps.csv'
            return [pid, event_file, pa_file]
        else:
            raise InputError('test PID in settings not recognized for particpant #'+str(n))

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
        

