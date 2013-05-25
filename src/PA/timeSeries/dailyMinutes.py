# -*- coding: utf-8 -*-

# this script reads in mMonitor's DAILY_TOTALS and creates a graph of physical activity levels for each day based on minutes spent in each class

import pylab # for plotting commands & array

from ...settings import * 
from .PAdata import *

PA = PAdata()
PA.getData(PAfileLoc)


def plot():
	print 'making plots...'
	#p = pylab.figure()
	# lineGraph = p.add_subplot(211)
	# lineGraph.plot(x,y)
	#barGraph = p.add_subplot(111)
	pl1 = pylab.plt.bar(PA.time,PA.sedentary,linewidth=0,color='b')
	base = PA.sedentary
	pl2 = pylab.plt.bar(PA.time,PA.light,linewidth=0,bottom=base,color='indigo')
	base = [base[i] + PA.light[i] for i in range(len(base))]
	pl3 = pylab.plt.bar(PA.time,PA.mod_vig,linewidth=0,bottom=base,color='r')
	base = [base[i] + PA.mod_vig[i] for i in range(len(base))]
	pl4 = pylab.plt.bar(PA.time,PA.nonWear,linewidth=0,bottom=base,color='dimGrey')
	base = [base[i] + PA.nonWear[i] for i in range(len(base))]
	pl5 = pylab.plt.bar(PA.time,PA.unknown,linewidth=0,bottom=base,color='lightGrey')

	pylab.plt.ylabel('amount [min]')
	pylab.plt.legend( (pl1[0],pl2[0],pl3[0],pl4[0],pl5[0]),\
		    ('sedentary','light','mod_vig','nonWear','unknown') )

	pylab.plt.show()

