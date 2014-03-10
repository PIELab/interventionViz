import pylab
from src.settings import setup, HIGHEST_P_NUMBER, setupUSFData

from src.interaction.interactionData import interactionData
from src.interaction.score import segmentInteractionIntoDays
from src.PA.PAdata import PAdata
from src.PA.score import segmentPAIntoDays,getPAscore_postiveOnly

import src.interaction.timeSeries.multicolorBars

from src.interaction.score import getInfluenceEffect
from src.util import spark
import Image



DATA_LOC = '../subjects/'

def plot():
	# load in all the data
	participants = list()
	interactions = list()

	for pNum in range(HIGHEST_P_NUMBER+1): #cycle through all participants

		pid,interactFile,PAfile = setupUSFData(pNum) # use dataset='test' to select sample dataset
		interactFile = DATA_LOC+pid+'/'+interactFile;
		PAfile    = DATA_LOC+pid+'/'+PAfile;
		settings = dict(interactionFileLoc=interactFile,
					PAfileLoc=PAfile)
					
		try:
			interact = (interactionData(settings['interactionFileLoc']))
			
			# TODO the rest...
		except IOError:
			print 'p '+pid+' interactions file not found'
			continue
			
		# if no problems:
		participants.append(pid)
		interactions.append(interact)
			
		print 'p' + pid + ' data loaded.'
		
	#scale all the data
		#TODO
		
	print '\n ==================================================' 
	print '\t total participants: '+str(len(participants))
	print ' =================================================='
			   
	# shift to time since start...
	for pnum in range(0,len(interactions)):
		start_t = min(interactions[pnum].t)
		for i in range (0, len(interactions[pnum])):
			interactions[pnum].t[i] -= start_t

	# shift all to same daily cycle
	for pnum in range(0,len(interactions)):
		timeOfDay = interactions[pnum].x[0]	#assuming earliest time is first...
		ToD_start = (timeOfDay.hour*60 + timeOfDay.minute) * 60
		for i in range (0, len(interactions[pnum])):
			interactions[pnum].t[i] += ToD_start

	figName = "interaction_sparkLines"
	pylab.figure(figName)
	num = 0
	for interaction in interactions:
		pylab.subplot(len(interactions),1,num)
		pylab.plot(interaction.t,interaction.v)
		num += 1
	fname = DATA_LOC+figName+'.png'
	pylab.plt.savefig(fname, dpi = 1000)
		