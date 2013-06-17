# -*- coding: utf-8 -*-

# creates a stacked bar graph of subject exposure to avatar

import pylab # for plotting commands & array

import datetime

from ...settings import * 

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

	def logPoint(self,t,tag,value):
		# t = time from start of study
		hrs = float(t)/60.0/60.0
		self.x.append(hrs)
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


	def getData(self, viewFileLoc):
		import csv
		# read in csv
		loadingDisplay=""	# this is a simple string to print so you know it's working
		updateFreq = 2000	# how many items per display update?
		div = 1000	# to reduce the amount of data (we don't really need millisecond-accurate readings)

		print "loading", viewFileLoc
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
				t0 = int(round(int(row[0])/div)-startTime)
				tf = int(round(int(row[1])/div)-startTime)
				self.logPoint(t0-1,0,0) # 0 before
				self.logPoint(t0,row[3],1) #value @ start
				self.logPoint(tf,row[3],1) #value @ end
				self.logPoint(tf+1,0,0) # 0 after

				if self.count % updateFreq == 0:
					loadingDisplay+="|"
					print loadingDisplay
		print 'done. '+str(self.count)+' datapoints loaded from '+str(self.rowCount)+' rows.'

def plot():
	viewData = data()
	viewData.getData(viewFileLoc)

	print 'making plots...'
	pylab.figure('multicolorBars')
	#barGraph = p.add_subplot(111)
	#TODO: maybe these shouldn't stack??? actually, it shouldn't be a problem anyway, since they should never be concurrent...
	pl1 = pylab.plt.plot(viewData.x,viewData.p1,'b',\
	                     viewData.x,viewData.p2,'oliveDrab',\
	                     viewData.x,viewData.p3,'indigo',\
	                     viewData.x,viewData.a1,'r',\
	                     viewData.x,viewData.a2,'orange',\
	                     viewData.x,viewData.a3,'orangeRed',\
	                     viewData.x,viewData.sl,'g',\
	                     viewData.x,viewData.ER,'deepPink')

#	pl2 = pylab.plt.fill(viewData.x,viewData.p2,linewidth=0,color='oliveDrab')
#	pl3 = pylab.plt.fill(viewData.x,viewData.p3,linewidth=0,color='indigo')
#	pl4 = pylab.plt.fill(viewData.x,viewData.a1,linewidth=0,color='r')
#	pl6 = pylab.plt.fill(viewData.x,viewData.a3,linewidth=0,color='orangeRed')
#	pl7 = pylab.plt.fill(viewData.x,viewData.sl,linewidth=0,color='g')
#	pl8 = pylab.plt.fill(viewData.x,viewData.ER,linewidth=0,color='deepPink')

	pylab.plt.xlabel('time [hrs]')
#	pylab.plt.legend( (pl1[0]      ,pl2[0]      ,pl3[0]      ,pl4[0]     ,pl5[0]      ,pl6[0]   ,pl7[0] ,pl8[0]),\
#	          ('onComputer','videoGames','watchingTV','bicycling','basketBall','running','sleep','ERROR') )

	pylab.plt.draw()

