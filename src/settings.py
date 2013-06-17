dataLocation = "./data/"	# location of participant folders

def setupTestData():
	pid          = "mockParticipant"# participant folder name
	viewLogFile = "dataLog.txt"	#name of view log file
	PAfile      = "miles/DAILY_TOTALS_358344041300005_2012-05-18.txt"	#name of physical activity data file

pid          = "1"# participant folder name
viewLogFile = "dataLog.txt"	#name of view log file
PAfile      = "mMonitor/miles/DAILY_TOTALS_358344041300005_2013-05-23.txt"	#name of physical activity data file

pid = "test1"
viewLogFile = "dataLog.txt"
PAfile = 'miles/DAILY_TOTALS_358344041300005_2013-06-16.txt'

viewFileLoc = dataLocation+pid+'/'+viewLogFile;
PAfileLoc   = dataLocation+pid+'/'+PAfile;
