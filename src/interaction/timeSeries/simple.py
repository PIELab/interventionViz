# -*- coding: utf-8 -*-
import pylab # for plotting commands & array

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

def plot():
	print "loading", viewFileLoc

	# read in csv
	loadingDisplay=""	# this is a simple string to print so you know it's working
	updateFreq = 2000	# how many items per display update?
	rowCount = 0
	count = 0

	div = 1000	# to reduce the amount of data (we don't really need or have millisecond-accurate readings)
	import csv
	with open(viewFileLoc, 'rb') as csvfile:
		spamreader = csv.reader(csvfile, delimiter=',')
		x = list()
		y = list()
		for row in spamreader:
			if rowCount==0:	#skip header row
				rowCount+=1
				continue
			if rowCount==1:	# set startTime
				startTime = int(round(int(row[0])/div))
			rowCount+=1
			# print ', '.join(row)	# print the raw data
			# print row		# print raw data matrix

			t0 = int(round(int(row[0])/div)-startTime)
			tf = int(round(int(row[1])/div)-startTime)
			t = t0-1 # 0 point before start
			x.append(t/60/60)
			y.append(float(0))
			t = t0	# value point @ start
			x.append(t/60/60)
			y.append(float(activePassiveMap(row[3])))
			t = tf # value point @ end
			x.append(t/60/60)
			y.append(float(activePassiveMap(row[3])))
			t = tf+1 # 0 point after end
			x.append(t/60/60)
			y.append(float(0))

			# old many-point implementation:
#			for time in range(int(round(int(row[0])/div)),int(round(int(row[1])/div))):	# for time span
#				t = time-startTime	#time from start of study
#				hrs = t/60/60
#				x.append(hrs)	# x is time in hrs
#				y.append(float(activePassiveMap(row[3])))
#				count+=1
#				if count % updateFreq == 0:
#					loadingDisplay+="|"
#					print loadingDisplay
	print 'done. '+str(count)+' datapoints loaded from '+str(rowCount)+' rows.'
	print 'making plots...'
	p = pylab.figure('simple')
	# lineGraph = p.add_subplot(211)
	# lineGraph.plot(x,y)
	barGraph = p.add_subplot(111)
	barGraph.bar(x,y,linewidth=0)

	pylab.draw()

