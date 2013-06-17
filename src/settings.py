dataLocation = "./data/"	# location of participant folders

def setupTestData(n):
	global pid, viewLogFile, PAfile
	if n == 1:
		pid = "test1"
		viewLogFile = "dataLog.txt"
		PAfile = 'miles_DAILY_TOTALS.txt'
	else:
		print 'test PID in settings.py not recognized; loading test1'
		pid = "test1"
		viewLogFile = "dataLog.txt"
		PAfile = 'miles_DAILY_TOTALS.txt'
		
def setupParticipantData(n):
	global pid, viewLogFile, PAfile
	if n == 1:
		pid          = "1"# participant folder name
		viewLogFile = "dataLog.txt"	#name of view log file
		PAfile      = "mMonitor/miles (repaired)/DAILY_TOTALS_358344041300005_2013-05-23.txt"	#name of physical activity data file
	else:
		print 'PID in settings.py not recognized; loading test data'
		setupTestData(1)
		

setupTestData(1)
#setupParticipantData(1)

viewFileLoc = dataLocation+pid+'/'+viewLogFile;
PAfileLoc   = dataLocation+pid+'/'+PAfile;
