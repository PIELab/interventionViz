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

### analysis run on all data: ###

import src.interaction_x_PA.tTest_paired as tTest_dep
tTest_dep.plot(dataset='USF',dataLoc=DATA_LOC) # use dataset='test' to select sample dataset
pylab.plt.savefig(DATA_LOC+'tTest_paired.png')

import src.interaction_x_PA.tTest_indep as tTest_indep
tTest_indep.plot(dataset='USF',dataLoc=DATA_LOC)
pylab.plt.savefig(DATA_LOC+'tTest_indep.png')

def updateChart(figName,plotter,settings,pid):
	fname = DATA_LOC+pid+'/'+figName+'.png'
	pylab.plt.figure(figName)
	plotter(settings)
	pylab.plt.savefig(fname, dpi = 100)

### analysis run on each participant and displayed together ###
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

figName = "all_interactions_x_time"
pylab.figure(figName)
pylab.plot(interactions[0].x,interactions[0].v,
           interactions[1].x,interactions[1].v,
		   interactions[2].x,interactions[2].v,
		   interactions[3].x,interactions[3].v,
		   interactions[4].x,interactions[4].v,
		   interactions[5].x,interactions[5].v,
		   interactions[6].x,interactions[6].v,
		   interactions[7].x,interactions[7].v,
		   interactions[8].x,interactions[8].v,
		   interactions[9].x,interactions[9].v,
		   interactions[10].x,interactions[10].v)	#TODO: add more if applicable
fname = DATA_LOC+figName+'.png'
pylab.plt.savefig(fname, dpi = 100)
		   
		   
# shift to time since start...
for pnum in range(0,len(interactions)):
	start_t = min(interactions[pnum].t)
	for i in range (0, len(interactions[pnum])):
		interactions[pnum].t[i] -= start_t
	
figName = "all_interactions_x_time_since_study_start"
pylab.figure(figName)
pylab.plot(interactions[0].t,interactions[0].v,
           interactions[1].t,interactions[1].v,
		   interactions[2].t,interactions[2].v,
		   interactions[3].t,interactions[3].v,
		   interactions[4].t,interactions[4].v,
		   interactions[5].t,interactions[5].v,
		   interactions[6].t,interactions[6].v,
		   interactions[7].t,interactions[7].v,
		   interactions[8].t,interactions[8].v,
		   interactions[9].t,interactions[9].v,
		   interactions[10].t,interactions[10].v)	#TODO: add more if applicable
fname = DATA_LOC+figName+'.png'
pylab.plt.savefig(fname, dpi = 100)

# shift all to same daily cycle
for pnum in range(0,len(interactions)):
	timeOfDay = interactions[pnum].x[0]	#assuming earliest time is first...
	ToD_start = (timeOfDay.hour*60 + timeOfDay.minute) * 60
	for i in range (0, len(interactions[pnum])):
		interactions[pnum].t[i] += ToD_start
		
figName = "all_interactions_x_time_of_day_since_study_start"
pylab.figure(figName)
pylab.plot(interactions[0].t,interactions[0].v,
           interactions[1].t,interactions[1].v,
		   interactions[2].t,interactions[2].v,
		   interactions[3].t,interactions[3].v,
		   interactions[4].t,interactions[4].v,
		   interactions[5].t,interactions[5].v,
		   interactions[6].t,interactions[6].v,
		   interactions[7].t,interactions[7].v,
		   interactions[8].t,interactions[8].v,
		   interactions[9].t,interactions[9].v,
		   interactions[10].t,interactions[10].v)	#TODO: add more if applicable
fname = DATA_LOC+figName+'.png'
pylab.plt.savefig(fname, dpi = 100)

figName = "interaction_sparkLines"
pylab.figure(figName)
num = 0
for interaction in interactions:
	pylab.subplot(len(interactions),1,num)
	pylab.plot(interaction.t,interaction.v)
	num += 1
fname = DATA_LOC+figName+'.png'
pylab.plt.savefig(fname, dpi = 1000)



pylab.show()
		
		


# make all the charts
#height = 14 #height of one image
#width  = 2  #width of one image
#count = 0
#fname = DATA_LOC+'/interactionSparks.png'
#total_w = (max([max(influ.t) for influ in interactions]) - min([min(influ.t) for influ in interactions]))/100 - 1
#outputImage = Image.new("RGB", (total_w, height*len(participants)), 'white') 

#while len(participants) != 0: #cycle through all participants
#	assert len(participants) == len(interactions) 
#	pid = participants.pop()
#	interaction = interactions.pop()
#	print 'working on p '+pid+'...'
	
	
	#	from src.interaction_x_PA.timeseries import plot as interaction_x_PA
	#	updateChart('interaction_x_PA.timeSeries',interaction_x_PA,settings)
	
#	pylab.plt.plot(interaction.x,interaction.b)
#	pylab.plt.show()
	
#	# build a timeseries list for given interactions
#	ts = [0]
#	tt = min(interaction.t)
#	nextT = 0
#	while tt <= max(interaction.t):
#		if tt == interaction.t[nextT]:
#			ts.append(interaction.v[nextT]*50)
#			nextT+=1
#		else:
#			ts.append(ts[-1])
#		tt+=1	
#	outputImage.paste(spark.sparkline_smooth(ts),(0,height*count))
#	count+=1

#outputImage.save(fname)
		
