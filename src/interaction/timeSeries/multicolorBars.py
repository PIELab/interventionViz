# -*- coding: utf-8 -*-

# creates a stacked bar graph of subject exposure to avatar

import pylab # for plotting commands & array
from src.interaction.interactionData import interactionData

def plot(settings):
	viewData = interactionData(settings['interactionFileLoc'])

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
	pylab.plt.legend( (pl1[0]      ,pl1[1]      ,pl1[2]      ,pl1[3]     ,pl1[4]      ,pl1[5]   ,pl1[6] ,pl1[7]),\
	                  ('onComputer','videoGames','watchingTV','bicycling','basketBall','running','sleep','ERROR'),\
	                   'best')

	pylab.plt.draw()

