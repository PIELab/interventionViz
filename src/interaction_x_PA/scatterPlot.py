# -*- coding: utf-8 -*-

# this script reads in mMonitor's DAILY_TOTALS and viewLog data, creates a simple 'score' for each, and plots the scores. This function assumes that the data sets come from the EXACT same days (and number of days); no checking is done to verify this, but data with different numbers of days prints a 'arrays must be same size' error.

import pylab # for plotting commands & array

from ..settings import * 
from ..PA.timeSeries.PAdata import *
from ..interaction.timeSeries.multicolorBars import data as interactionData

# load interaction data
interact = interactionData()
interact.getData(viewFileLoc)

# generate interaction 'score'
interactScore = list()
# gather data from timestamps in interact.x together by day
i = 0
while i+1 < len(interact.x)-1:
	score = 0
	print str(interact.x[i].date()) +'=?='+str(interact.x[i+1].date())
	while interact.x[i].date() == interact.x[i+1].date(): # count up all in same day
		print str(i)
		score += interact.a1[i]+interact.a2[i]+interact.a3[i]-(interact.p1[i]+interact.p2[i]+interact.p3[i])
		i+=1
		if i+1 > len(interact.x)-1:
			break
	score += interact.a1[i]+interact.a2[i]+interact.a3[i]-(interact.p1[i]+interact.p2[i]+interact.p3[i])
	i+=1
	# now score is day's total, add it to the list
	interactScore.append(score)


# load PA data
PA = PAdata()
PA.getData(PAfileLoc)

# generate daily PA 'score'
PAscore = list()
for i in range(len(PA.time)):
	PAscore.append(2*PA.mod_vig[i]+PA.light[i]-PA.sedentary[i])

print 'output is ' + str(len(PAscore)) + 'x' + str(len(interactScore))

def plot():
	pltName = 'PA vs interaction'
	print 'making plot "'+pltName+'"'
	pylab.figure(pltName)
	#p = pylab.figure()
	# lineGraph = p.add_subplot(211)
	# lineGraph.plot(x,y)
	#barGraph = p.add_subplot(111)
	pylab.plt.scatter(PAscore,interactScore,color='b')

	pylab.plt.ylabel('physical activity score')
	pylab.plt.xlabel('proteus PA influence')

	pylab.plt.draw()

