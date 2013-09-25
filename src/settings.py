dataLocation = "./data/"	# location of participant folders

def setupTestData(n):
	global pid, viewLogFile, PAfile
	if n == 1:
		pid = "test1"
		viewLogFile = "dataLog.txt"
		PAfile = 'miles_DAILY_TOTALS.txt'
	elif n == 2:
		pid = "test2"
		viewLogFile = "mirrorMe/dataLog3.txt"
		PAfile = 'miles_DAILY_TOTALS_fixed.txt'
	else:
		print 'ERR: test PID in settings.py not recognized; loading test1!\n\n'
		pid = "test1"
		viewLogFile = "dataLog.txt"
		PAfile = 'miles_DAILY_TOTALS.txt'
		
def setupParticipantData(n):
	global pid, viewLogFile, PAfile
	if n == 1:
		pid          = "1"# participant folder name
		viewLogFile = "dataLog.txt"	#name of view log file
		PAfile      = "mMonitor/miles (repaired)/DAILY_TOTALS_358344041300005_2013-05-23.txt"	#name of physical activity data file
	elif n == 2:
		pid = '2'
		viewLogFile = "mirrorMe/dataLog_Android_data_eduusfengpieavatars4change.txt"
		PAfile = 'mMonitor/DAILY_TOTALS_354583040636059_2013-06-01.txt'
	elif n == 3:
		pid = '3'
		viewLogFile = "avatarWallpaper/dataLog.txt"
		PAfile      = "miles/DAILY_TOTALS_358344041300005_2013-07-10.txt"
	elif n == 8:
		pid = '8'
		viewLogFile = "dataLog.txt"
		PAfile      = "miles/DAILY_TOTALS_358344041300005_2013-08-28.txt"
	elif n == 10:
		pid = '10'
		viewLogFile = "dataLog.txt"
		PAfile      = "miles/DAILY_TOTALS_358344041300005_2013-09-13.txt"
	elif n == 11:
		pid = '11'
		viewLogFile = "dataLog.txt"
		PAfile      = "miles/DAILY_TOTALS_358344041300005_2013-09-25.txt"
	else:
		print 'ERR:PID in settings.py not recognized; loading test data!\n\n'
		setupTestData(1)
		

setupTestData(2)
#setupParticipantData(11)

viewFileLoc = dataLocation+pid+'/'+viewLogFile;
PAfileLoc   = dataLocation+pid+'/'+PAfile;
