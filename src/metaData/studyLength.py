''' 
Here we focus on reading and organizing study length data into various data objects.
'''

from datetime import timedelta, datetime
import csv

class studyLength(object):

	def __init__(self,fileLoc=None):
		self.start = None
		self.end   = None
	
		# 0-before, 1 after start, 1 before end, 0 after points 
		# for filled line interval charting:
		self.intervalPoints = list()
		self.intervalTimes  = list()
		
		# list of datetime days in the study
		self.days = list()
		
		# go ahead and load data if file given
		if fileLoc != None:
			self.getData(fileLoc)
		else:
			pass

	def __str__(self):
		'''
		returns a summary of data
		'''
		return self.__repr__() + '\n' \
			+ '  interval: ' + str(self.start) + ' -> ' + str(self.end) + '\n' \
			+ 'total days: ' + str(len(self.days))
			
	def getData(self, fileLoc):
		with open(fileLoc, 'rb') as csvfile:
					currentDay = None
					spamreader = csv.reader(csvfile,delimiter=',')
					rowCount = 0
					for row in spamreader:
						if rowCount==0: # skip header row
							rowCount+=1
							continue
						rowCount+=1
										
						self.start = datetime.strptime(row[0],"%Y-%m-%dT%H:%M:%S")
						self.end   = datetime.strptime(row[1],"%Y-%m-%dT%H:%M:%S")
						
		self.logInterval(self.start,self.end)
						
		self.addDays(self.start,self.end)
			
		return self
		
	def logInterval(self, start,end):
		'''
		logs interval points for time interval between start and end
		'''
		dt = timedelta(seconds=1) # negligably small time for study to switch on/off
		
		# 0 point before start
		self.intervalPoints.append(0)
		self.intervalTimes.append(start-dt)
		
		# 1 point at start
		self.intervalPoints.append(1)
		self.intervalTimes.append(start)
		
		# 1 point at end
		self.intervalPoints.append(1)
		self.intervalTimes.append(end)
		
		# 0 point after end
		self.intervalPoints.append(0)
		self.intervalTimes.append(end+dt)
		
	def addDays(self, start, end):
		''' 
		add the days from start to end to the day listing
		'''
		d = start
		while d <= end:
			self.days.append(d.day)
			d += timedelta(days=1)
		
		# if += 1 day undershot (or nailed) ending time, all is good.
		# if overshot ending time, d.day == end.day and we still need to add that last day
		if d.day == end.day:
			self.days.append(end.day)