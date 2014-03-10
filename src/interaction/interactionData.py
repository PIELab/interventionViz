# this file defines a data object for avatar interaction data
import datetime

class interactionData:
	def __init__(self,fileName=None):
		self.rowCount = 0
		self.count = 0

		self.t = list()		# raw time value
		self.x = list()		# datetime value (x axis)
		self.p1 = list()	# passives
		self.p2 = list()
		self.p3 = list()
		self.a1 = list()	# actives
		self.a2 = list()
		self.a3 = list()
		self.sl = list()	# sleep?
		self.ER = list()	# error?
		self.v  = list()	# +/- active/sedentary value
		self.b  = list()	# (boolean) +1 when shown 0 when not

		if(fileName!=None):
			self.getData(fileName)

	def logPoint(self,t,tag,value):
		# t = time from start of study
		#hrs = float(t)/60.0/60.0
		#self.x.append(hrs)
		self.t.append(t)
		self.x.append(datetime.datetime.fromtimestamp(t))
		self.p1.append(0)
		self.p2.append(0)
		self.p3.append(0)
		self.a1.append(0)
		self.a2.append(0)
		self.a3.append(0)
		self.sl.append(0)
		self.ER.append(0)

		self.count+=1

		if value==0:
			self.v.append(0)
			self.b.append(0)
			return
		else:
			# passives are negative
			if tag == 'onComputer':
				self.p1[-1] = -1
			elif tag == 'videoGames':
				self.p2[-1] = -1
			elif tag == 'watchingTV':
				self.p3[-1] = -1
			# actives are positive
			elif tag == 'bicycling':
				self.a1[-1] = 1
			elif tag == 'basketball':
				self.a2[-1] = 1
			elif tag == 'running':
				self.a3[-1] = 1
			elif tag == 'inBed':
				self.sl[-1] = (-0.5)
			else:	#ERROR
				self.ER[-1] = (0.5)
		#	y.append(float(activePassiveMap(row[3])))
		
		self.b.append(1)
		self.v.append(self.p1[-1]+self.p2[-1]+self.p3[-1]+self.a1[-1]+self.a2[-1]+self.p3[-1]+self.sl[-1]+self.ER[-1])

	def __len__(self):
		return self.count
		
		
	def getData(self, viewFileLoc):
		import csv
		# read in csv
		loadingDisplay=""	# this is a simple string to print so you know it's working
		updateFreq = 2000	# how many items per display update?
		div = 1000	# to reduce the amount of data (we don't really need millisecond-accurate readings)

#		print "loading", viewFileLoc
		with open(viewFileLoc, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',')
			for row in spamreader:
				if self.rowCount==0:	#skip header row
					self.rowCount+=1
					continue
				if self.rowCount==1:	# set startTime
					startTime = int(round(int(row[0])/div))
				self.rowCount+=1
				# print ', '.join(row)	# print the raw data
				# print row		# print raw data matrix
				t0 = int(round(int(row[0])/div))
				tf = int(round(int(row[1])/div))
				self.logPoint(t0-1,0,0) # 0 before
				self.logPoint(t0,row[3],1) #value @ start
				self.logPoint(tf,row[3],1) #value @ end
				self.logPoint(tf+1,0,0) # 0 after

				if self.count % updateFreq == 0:
					loadingDisplay+="|"
					print loadingDisplay
		print str(self.count)+' datapoints loaded from '+str(self.rowCount)+' rows.'

