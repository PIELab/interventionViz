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
	PA_participants = list()
	PA = list()
	for pNum in range(HIGHEST_P_NUMBER+1): #cycle through all participants
		
		settings = setup(dataset='USF', dataLoc=DATA_LOC, subjectN=pNum)
			
		try:
			pid = pNum
			fName = settings.getFileName('fitbit')
			pa = PAdata(fName,method='fitbit',timeScale='minute')
		except IOError:
			print 'p '+str(pid)+' PA file "'+ fName +'" not found'
			continue
			
		# if no problems:
		PA_participants.append(pid)
		PA.append(pa)
			
#		print 'p' + pid + ' data loaded.'
		
	interact_participants = list()
	interactions = list()
	for pNum in range(HIGHEST_P_NUMBER+1): #cycle through all participants

		settings = setup(dataset='USF', dataLoc=DATA_LOC, subjectN=pNum)
					
		try:
			pid = pNum
		
			fName = settings.getFileName('viewLog')
			interact = (interactionData(fName))
		except IOError:
			print 'p '+str(pid)+' interactions file not found'
			continue
			
		# if no problems:
		interact_participants.append(pid)
		interactions.append(interact)
			
#		print 'p' + pid + ' data loaded.'
		
		
		
	
	#scale all the data
	PAscaler = 1.0/50.0
	for pnum in range (0,len(PA)):
		for i in range(0,len(PA[pnum])):
			PA[pnum].steps[i] *= PAscaler
   
	# shift to time since start...
	# for pnum in range(0,len(PA)):
		# start_t = min(PA[pnum].timestamp)
		# for i in range (0, len(PA[pnum])):
			# PA[pnum].timestamp[i] -= start_t
	
	# for pnum in range(0,len(interactions)):		
		# start_t = min(interactions[pnum].t)
		# for i in range (0, len(interactions[pnum])):
			# interactions[pnum].t[i] -= start_t

	# # shift all to same daily cycle
	# for pnum in range(0,len(PA)):
		# timeOfDay = PA[pnum].time[0]	#assuming earliest time is first...
		# for i in range (0, len(PA[pnum])):
			# PA[pnum].time[i] += timeOfDay
			
		# timeOfDay = interactions[pnum].t[0] #assuming earliest time is first...
		# ToD_start = (timeOfDay.hour*60 + timeOfDay.minute) * 60
		# for i in range (0, len(interactions[pnum])):
			# interactions[pnum].t[i] += ToD_start

#	class Bunch:
#		''' bunches! makes a dictionary look like a class! bam! '''
#		__init__ = lambda self, **kw: setattr(self, '__dict__', kw)
	
	# make the plots
	figName = "scatterplot_masterdash"
	pylab.figure(figName)
	pylab.subplots_adjust(left=0,bottom=0,right=1,top=1,wspace=0,hspace=0)
	num = 0
	max_p = max(max(PA_participants),max(interact_participants))+1
	pCount = max(len(PA_participants),len(interact_participants))+1
	actualCount = 1
	for i in range(max_p):
		pylab.subplot(pCount,1,actualCount)
		try:
			pa = PA[PA_participants.index(num)]
		except ValueError as m:
			print 'p' + m.message + ' of PA'
			pa = None # Bunch(time=0,steps=0)
		try:
			interact = interactions[interact_participants.index(num)]
		except ValueError as m:
			print 'p' + m.message + ' of interactions'
			interact = None # Bunch(t=0,v=0)
			
		num += 1
			
		isData = False
		try:
			pylab.scatter(pa.timestamp, pa.steps, marker='x', color = 'b')
			isData = True
		except AttributeError as e:
			pass
		try:
			pylab.scatter(interact.t, interact.v, marker='+', color='r')
			isData = True
		except AttributeError as e:
			pass
			
		if isData:
			actualCount += 1


		