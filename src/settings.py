dataLocation = "./data/"	# location of participant folders

def setupTestData(n):
	if n == 1:
		pid = "test1"
		viewLogFile = "dataLog.txt"
		PAfile = 'miles/DAILY_TOTALS_358344041300005_2013-06-16.txt'
	else:
		pid = "test1"
		viewLogFile = "dataLog.txt"
		PAfile = 'miles/DAILY_TOTALS_358344041300005_2013-06-16.txt'
		

pid          = "1"# participant folder name
viewLogFile = "dataLog.txt"	#name of view log file
PAfile      = "mMonitor/miles (repaired)/DAILY_TOTALS_358344041300005_2013-05-23.txt"	#name of physical activity data file


viewFileLoc = dataLocation+pid+'/'+viewLogFile;
PAfileLoc   = dataLocation+pid+'/'+PAfile;
