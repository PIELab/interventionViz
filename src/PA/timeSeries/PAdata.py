import dateutil.parser	#for parsing datestrings
import csv		#for csv file reading

class PAdata:
	def __init__(self):
		self.time = list()

		self.nonWear = list()
		self.sedentary = list()
		self.light = list()
		self.mod_vig = list()
		self.unknown = list()

		self.rowCount = 0
		self.count = 0


	def getData(self, PAfileLoc):
		print "loading", PAfileLoc

		# read in csv
		loadingDisplay=""	# this is a simple string to print so you know it's working
		updateFreq = 10	# how many items per display update?

		with open(PAfileLoc, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',')

			for row in spamreader:
				if self.rowCount==0:	#skip header row
					self.rowCount+=1
					continue
				self.rowCount+=1
				# print ', '.join(row)	# print the raw data
				# print row		# print raw data matrix

				self.time.append(dateutil.parser.parse(row[1]))
				self.nonWear.append(float(row[3]))
				self.sedentary.append(float(row[4]))
				self.light.append(float(row[5]))
				self.mod_vig.append(float(row[6]))
				self.unknown.append(float(row[9])*60)	# hrs->min
	

				self.count+=1
				if self.count % updateFreq == 0:
					loadingDisplay+="|"
					print loadingDisplay
		print 'done. '+str(self.count)+' datapoints loaded from '+str(self.rowCount)+' rows.'
