import pylab
from src.settings import setup, HIGHEST_P_NUMBER

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
	PA = list()

	for pNum in range(HIGHEST_P_NUMBER+1): #cycle through all participants
		
		settings = setup(dataset='USF', dataLoc=DATA_LOC, subjectN=pNum)
			
		try:
			pid = str(pNum)
			fName = settings.getFileName('fitbit')
			pa = PAdata(fName,method='fitbit',timeScale='minute')
			
			# TODO the rest...
		except IOError:
			print 'p '+pid+' PA file "'+ fName +'" not found'
			continue
			
		# if no problems:
		participants.append(pid)
		PA.append(pa)
			
		print 'p' + pid + ' data loaded.'
		
	#scale all the data
		#TODO
		
	print '\n ==================================================' 
	print '\t total participants: '+str(len(participants))
	print ' =================================================='
   
	# shift to time since start...
#	for pnum in range(0,len(PA)):
#		start_t = min(PA[pnum].time)
#		for i in range (0, len(PA[pnum])):
#			PA[pnum].time[i] -= start_t

#	# shift all to same daily cycle
#	for pnum in range(0,len(PA)):
#		timeOfDay = PA[pnum].time[0]	#assuming earliest time is first...
#		ToD_start = (timeOfDay.hour*60 + timeOfDay.minute) * 60
#		for i in range (0, len(PA[pnum])):
#			PA[pnum].time[i] += ToD_start
	
	# make the plots
	figName = "PA_sparkScatterplot"
	pylab.figure(figName)
	num = 0
	for pa in PA:
		pylab.subplot(len(PA),1,num)
		pylab.scatter(pa.time, pa.steps, marker='x', color='b')
		num += 1

		