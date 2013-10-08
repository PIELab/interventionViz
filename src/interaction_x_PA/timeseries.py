# -*- coding: utf-8 -*-

import pylab # for plotting commands & array

from src.PA.PAdata import PAdata
from src.interaction.timeSeries.multicolorBars import interactionData
from src.interaction.score import segmentInteractionIntoDays
from src.PA.score import segmentPAIntoDays
from matplotlib.dates import date2num


def plot(settings):
	# load interaction data
	interact = interactionData(settings['interactionFileLoc'])
	interactScore,interactDate = segmentInteractionIntoDays(interact)

	# load PA data
	PA = PAdata(settings['PAfileLoc'])
	PAscore,PAdate = segmentPAIntoDays(PA)

	pltName = 'user PA and avatar influence vs time'
	barWidth= 0.2
	print 'making plot "'+pltName+'"'
	pylab.figure(pltName)
	p1 = pylab.plt.bar(date2num(interactDate)+barWidth/2.0, interactScore, color='g', width=barWidth,linewidth=0)
	p2 = pylab.plt.bar(date2num(PAdate)      -barWidth/2.0, PAscore      , color='b', width=barWidth,linewidth=0)
	pylab.plt.legend( (p1,p2), ('avatar influence', 'subject PA') )

	pylab.plt.ylabel('PA score & interaction score')
	pylab.plt.xlabel('time')

	pylab.plt.draw()
