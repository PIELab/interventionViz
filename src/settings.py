# this file defines setup methods and configuration options 

HIGHEST_P_NUMBER = 15

def setup(dataset='test',dataLoc = "./data/"):
# performs needed setup for scripts & returns dictionary with settings
# 	paramters:
#		dataset - name of dataset to use
#		dataLoc - relative location of participant folders
#
#	returned settings dict items:
#		interactionFileLoc - relative location of interaction data file
#		PAfileLoc          - relative location of physical activity data file 
	DEFAULT_PARTICIPANT_NUM = 1
	# load appropriate setup function for chosen dataset
	if dataset == 'default':
		pid,interactFile,PAfile = setupTestData(DEFAULT_PARTICIPANT_NUM)
	elif dataset == 'test' or dataset == 'sample':
		pid,interactFile,PAfile = setupTestData(getParticipantNum())
	elif dataset == 'USF':
		dataLoc = "../subjects/"
		pid,interactFile,PAfile = setupUSFData(getParticipantNum())
	else:
		raise InputError('bad dataset name "'+str(dataset)+'" in settings')

	interactFile = dataLoc+pid+'/'+interactFile;
	PAfile    = dataLoc+pid+'/'+PAfile;
	return dict(interactionFileLoc=interactFile,
	            PAfileLoc=PAfile)

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
def setupUSFData(n):
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
	elif int(n) == 12:
		pid = '12'
		viewLogFile = "dataLog.txt"
		PAfile      = "miles_FIXED/DAILY_TOTALS_359590044855853_2013-10-24.txt"
	elif int(n) == 13:
		pid = '13'
		viewLogFile = 'dataLog.txt'
	#	PAfile      = "miles2/DAILY_TOTALS_863496013125329_2013-10-31.txt"
	#	PAfile      = "miles/DAILY_TOTALS_358344041300005_2013-10-31.txt"
		PAfile      = "miles/DAILY_TOTALS_358344041300005_2013-10-31_fixed.txt"
	elif int(n) == 14:
		pid = '14'
		viewLogFile = 'dataLog.txt'
		PAfile      = "miles/DAILY_TOTALS_359590044855853_2013-12-06.txt"
	elif int(n) == 15:
		pid = '15'
		viewLogFile = 'dataLog.txt'
		PAfile      = "miles/DAILY_TOTALS_358344041300005_2013-12-02.txt"
	else:
		raise InputError('USF data PID in settings not recognized for particpant #'+str(n))
	return [pid,viewLogFile,PAfile]
