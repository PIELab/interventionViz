# this file defines setup methods and configuration options 

HIGHEST_P_NUMBER = 50

class setup:
# performs needed setup for scripts & returns dictionary with settings
# 	paramters:
#		dataset - name of dataset to use
#		dataLoc - relative location of participant folders
#
#	returned settings dict items:
#		interactionFileLoc - relative location of interaction data file
#		PAfileLoc          - relative location of physical activity data file 

	def __init__(self,dataset='test',dataLoc="./data/",subjectN=None):
		DEFAULT_PARTICIPANT_NUM = 1
		# load appropriate setup function for chosen dataset
		if dataset == 'default':
			pid,interactFile,PAfile = self.setupTestData(DEFAULT_PARTICIPANT_NUM)
		elif dataset == 'test' or dataset == 'sample':
			pid,interactFile,PAfile = self.setupTestData(self.getParticipantNum())
		elif dataset == 'USF':
			dataLoc = "../subjects/"
			if subjectN==None:
				pid,interactFile,PAfile = self.setupUSFData(self.getParticipantNum())
			else:
				self.pid = str(subjectN)
				pid,interactFile,PAfile = self.setupUSFData(subjectN)
		else:
			raise InputError('bad dataset name "'+str(dataset)+'" in settings')

		self.dataLoc = dataLoc
			
		interactFile = dataLoc+pid+'/'+interactFile;
		PAfile    = dataLoc+pid+'/'+PAfile;
		
		self.dataset = dataset
		self.settings = dict(interactionFileLoc=interactFile,
					PAfileLoc=PAfile)
					
	def __getitem__(self,item):
		''' this is to maintain backwards compatibility '''
		return self.settings[item]
		
	def getFileName(self,type):
		prefix = self.dataLoc+self.pid+'/'
		if self.dataset == 'USF':
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
			raise NotImplementedError("getFileName('test') not yet implemented")
		else: 
			raise ValueError('dataset type "'+str(self.dataset)+'" not recognized')
			
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
		

