# -*- coding: utf-8 -*-

# this script reads in mMonitor's DAILY_TOTALS and creates a graph of physical activity levels for each day based on minutes spent in each class

import pylab # for plotting commands & array
from ...settings import * 
import dateutil.parser	#for parsing datestrings

print "loading", PAfileLoc

# read in csv
loadingDisplay=""	# this is a simple string to print so you know it's working
updateFreq = 10	# how many items per display update?
rowCount = 0
count = 0

div = 1000	# to reduce the amount of data (we don't really need or have millisecond-accurate readings)
import csv
with open(PAfileLoc, 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	x = list()	# x is day
	# 'y's are PA classes:
	nonWear = list()
	sedentary = list()
	light = list()
	mod_vig = list()
	unknown = list()

	for row in spamreader:
		if rowCount==0:	#skip header row
			rowCount+=1
			continue
		rowCount+=1
		# print ', '.join(row)	# print the raw data
		# print row		# print raw data matrix

		x.append(dateutil.parser.parse(row[1]))	# x is day
		nonWear.append(float(row[3]))
		sedentary.append(float(row[4]))
		light.append(float(row[5]))
		mod_vig.append(float(row[6]))
		unknown.append(float(row[9])*60)	# hrs->min
		

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
pl1 = pylab.plt.bar(x,sedentary,linewidth=0,color='b')
base = sedentary
pl2 = pylab.plt.bar(x,light,linewidth=0,bottom=base,color='indigo')
base = [base[i] + light[i] for i in range(len(base))]
pl3 = pylab.plt.bar(x,mod_vig,linewidth=0,bottom=base,color='r')
base = [base[i] + mod_vig[i] for i in range(len(base))]
pl4 = pylab.plt.bar(x,nonWear,linewidth=0,bottom=base,color='dimGrey')
base = [base[i] + nonWear[i] for i in range(len(base))]
pl5 = pylab.plt.bar(x,unknown,linewidth=0,bottom=base,color='lightGrey')

pylab.plt.ylabel('amount [min]')
pylab.plt.legend( (pl1[0],pl2[0],pl3[0],pl4[0],pl5[0]),\
            ('sedentary','light','mod_vig','nonWear','unknown') )

pylab.plt.show()

