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

print "loading", viewFileLoc

# read in csv
loadingDisplay=""	# this is a simple string to print so you know it's working
updateFreq = 2000	# how many items per display update?
rowCount = 0
count = 0

div = 1000	# to reduce the amount of data (we don't really need or have millisecond-accurate readings)
import csv
with open(fileLoc, 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	x = list()
	p1 = list()
	p2 = list()
	p3 = list()
	a1 = list()
	a2 = list()
	a3 = list()
	sl = list()
	ER = list()
	for row in spamreader:
		if rowCount==0:	#skip header row
			rowCount+=1
			continue
		if rowCount==1:	# set startTime
			startTime = int(int(row[0])/div)
		rowCount+=1
		# print ', '.join(row)	# print the raw data
		# print row		# print raw data matrix
		for time in range(int(int(row[0])/div),int(int(row[1])/div)):	# for time span
			t = time-startTime	#time from start of study
			hrs = t/60/60
			x.append(hrs)	# x is time in hrs
			p1.append(0)
			p2.append(0)
			p3.append(0)
			a1.append(0)
			a2.append(0)
			a3.append(0)
			sl.append(0)
			ER.append(0)

			tag = row[3]
			# passives are negative
			if tag == 'onComputer':
				p1[-1] = -1
			elif tag == 'videoGames':
				p2[-1] = -1
			elif tag == 'watchingTV':
				p3[-1] = -1
			# actives are positive
			elif tag == 'bicyling':
				a1[-1] = 1
			elif tag == 'playingBasketball':
				a2[-1] = 1
			elif tag == 'running':
				a3[-1] = 1
			elif tag == 'inBed':
				sl[-1] = (-0.5)
			else:	#ERROR
				ER[-1] = (0.5)
		#	y.append(float(activePassiveMap(row[3])))
			count+=1
			if count % updateFreq == 0:
				loadingDisplay+="|"
				print loadingDisplay
print 'done. '+str(count)+' datapoints loaded from '+str(rowCount)+' rows.'
print 'making plots...'
#p = pylab.figure()
# lineGraph = p.add_subplot(211)
# lineGraph.plot(x,y)
#barGraph = p.add_subplot(111)
pl1 = pylab.plt.bar(x,p1,linewidth=0,color='b')
pl2 = pylab.plt.bar(x,p2,linewidth=0,color='oliveDrab')
pl3 = pylab.plt.bar(x,p3,linewidth=0,color='indigo')
pl4 = pylab.plt.bar(x,a1,linewidth=0,color='r')
pl5 = pylab.plt.bar(x,a2,linewidth=0,color='orange')
pl6 = pylab.plt.bar(x,a1,linewidth=0,color='orangeRed')
pl7 = pylab.plt.bar(x,sl,linewidth=0,color='g')
pl8 = pylab.plt.bar(x,ER,linewidth=0,color='deepPink')

#,p2,p3,a1,a2,a3,sl,ER


pylab.plt.show()

