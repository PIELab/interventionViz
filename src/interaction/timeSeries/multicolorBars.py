# -*- coding: utf-8 -*-

# creates a stacked bar graph of subject exposure to avatar

import pylab # for plotting commands & array

import datetime

from ...settings import * 

def activePassiveMap(tag):
	# passives are negative
	if tag == 'onComputer':
		return -1
	elif tag == 'videoGames':
		return -2
	elif tag == 'watchingTV':
		return -3
	# actives are positive
	elif tag == 'bicyling':
		return 1
	elif tag == 'playingBasketball':
		return 2
	elif tag == 'running':
		return 3
	elif tag == 'inBed':
		return -0.2
	else:
		return 0.5

class data:
	def __init__(self):
		self.rowCount = 0
		self.count = 0

		self.x = list()
		self.p1 = list()
		self.p2 = list()
		self.p3 = list()
		self.a1 = list()
		self.a2 = list()
		self.a3 = list()
		self.sl = list()
		self.ER = list()

	def getData(self, viewFileLoc):
		import csv
		# read in csv
		loadingDisplay=""	# this is a simple string to print so you know it's working
		updateFreq = 2000	# how many items per display update?
		div = 1000*60	# to reduce the amount of data (we don't really need millisecond-accurate readings)

		print "loading", viewFileLoc
		with open(viewFileLoc, 'rb') as csvfile:
			spamreader = csv.reader(csvfile, delimiter=',')

			for row in spamreader:
				if self.rowCount==0:	#skip header row
					self.rowCount+=1
					continue
				if self.rowCount==1:	# set startTime
					startTime = int(int(row[0])/div)
				self.rowCount+=1
				# print ', '.join(row)	# print the raw data
				# print row		# print raw data matrix
				for time in range(int(int(row[0])/div),int(int(row[1])/div)):	# for time span
				#	t = time-startTime	#time from start of study
				#	hrs = t/60/60
				#	x.append(hrs)	# x is time in hrs
					self.x.append(datetime.datetime.fromtimestamp(time*60))	
					self.p1.append(0)
					self.p2.append(0)
					self.p3.append(0)
					self.a1.append(0)
					self.a2.append(0)
					self.a3.append(0)
					self.sl.append(0)
					self.ER.append(0)

					tag = row[3]
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
					self.count+=1
					if self.count % updateFreq == 0:
						loadingDisplay+="|"
						print loadingDisplay
		print 'done. '+str(self.count)+' datapoints loaded from '+str(self.rowCount)+' rows.'

def plot():
	viewData = data()
	viewData.getData(viewFileLoc)

	print 'making plots...'
	pylab.figure('multicolorBars')
	#p = pylab.figure()
	# lineGraph = p.add_subplot(211)
	# lineGraph.plot(x,y)
	#barGraph = p.add_subplot(111)
	#TODO: maybe these shouldn't stack??? actually, it shouldn't be a problem anyway, since they should never be concurrent...
	pl1 = pylab.plt.bar(viewData.x,viewData.p1,linewidth=0,color='b')
	base = viewData.p1
	pl2 = pylab.plt.bar(viewData.x,viewData.p2,linewidth=0,bottom=base,color='oliveDrab')
	base = [base[i] + viewData.p2[i] for i in range(len(base))]
	pl3 = pylab.plt.bar(viewData.x,viewData.p3,linewidth=0,bottom=base,color='indigo')
	base = [base[i] + viewData.p3[i] for i in range(len(base))]
	pl4 = pylab.plt.bar(viewData.x,viewData.a1,linewidth=0,bottom=base,color='r')
	base = [base[i] + viewData.a1[i] for i in range(len(base))]
	pl5 = pylab.plt.bar(viewData.x,viewData.a2,linewidth=0,bottom=base,color='orange')
	base = [base[i] + viewData.a2[i] for i in range(len(base))]
	pl6 = pylab.plt.bar(viewData.x,viewData.a1,linewidth=0,bottom=base,color='orangeRed')
	base = [base[i] + viewData.a3[i] for i in range(len(base))]
	pl7 = pylab.plt.bar(viewData.x,viewData.sl,linewidth=0,bottom=base,color='g')
	base = [base[i] + viewData.sl[i] for i in range(len(base))]
	pl8 = pylab.plt.bar(viewData.x,viewData.ER,linewidth=0,bottom=base,color='deepPink')

	pylab.plt.xlabel('time [hrs]')
	pylab.plt.legend( (pl1[0]      ,pl2[0]      ,pl3[0]      ,pl4[0]     ,pl5[0]      ,pl6[0]   ,pl7[0] ,pl8[0]),\
		          ('onComputer','videoGames','watchingTV','bicycling','basketBall','running','sleep','ERROR') )

	pylab.plt.draw()

