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
	pid = str(n)
	viewLogFile = "viewTimes.txt"
	PAfile = "daily_totals.txt"
	return [pid,viewLogFile,PAfile]
