# this file defines setup methods and configuration options 

# performs needed setup for scripts
def setup():
	global dataLocation
	dataLocation = "./data/"	# location of participant folders

	global datasetName
	datasetName  = 'USF'		# change this to use a different dataset

	# load appropriate setup function for chosen dataset
	if datasetName == 'test':
		setupTestData(getParticipantNum())
	elif datasetName == 'USF':
		setupUSFData(getParticipantNum())
	else:
		print 'ERR: bad dataset name in settings'

	global viewFileLoc
	global PAfileLoc
	viewFileLoc = dataLocation+pid+'/'+viewLogFile;
	PAfileLoc   = dataLocation+pid+'/'+PAfile;

### PRIVATE METHODS ###

class InputError(Exception):
	# Exception raised for errors in the input.
	def __init__(self, value):
		self.value = value
	def __str__(self):
		return repr(self.value)

def getParticipantNum():
	print 'Enter participant number.'
	return raw_input()

# setup details for test dataset
def setupTestData(n):
	global pid, viewLogFile, PAfile
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
		
		
# detailed setup information for USF dataset
def setupUSFData(n):
	global pid, viewLogFile, PAfile
	if int(n) == 1:
		pid          = "1"# participant folder name
		viewLogFile = "dataLog.txt"	#name of view log file
		PAfile      = "mMonitor/miles (repaired)/DAILY_TOTALS_358344041300005_2013-05-23.txt"	#name of physical activity data file
	elif int(n) == 2:
		pid = '2'
		viewLogFile = "mirrorMe/dataLog_Android_data_eduusfengpieavatars4change.txt"
		PAfile = 'mMonitor/DAILY_TOTALS_354583040636059_2013-06-01.txt'
	elif int(n) == 3:
		pid = '3'
		viewLogFile = "avatarWallpaper/dataLog.txt"
		PAfile      = "miles (repaired)/DAILY_TOTALS_358344041300005_2013-07-10.txt"
	elif int(n) == 8:
		pid = '8'
		viewLogFile = "dataLog.txt"
		PAfile      = "miles/DAILY_TOTALS_358344041300005_2013-08-28.txt"
	elif int(n) == 10:
		pid = '10'
		viewLogFile = "dataLog.txt"
		PAfile      = "miles/DAILY_TOTALS_358344041300005_2013-09-13.txt"
	elif int(n) == 11:
		pid = '11'
		viewLogFile = "dataLog.txt"
		PAfile      = "miles/DAILY_TOTALS_358344041300005_2013-09-25.txt"
	else:
		raise InputError('USF data PID in settings not recognized for particpant #'+str(n))
