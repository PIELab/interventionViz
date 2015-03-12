import pylab

from src.settings import setup, HIGHEST_P_NUMBER
from src.interaction.interactionData import interactionData


DATA_LOC = '../subjects/'

def plot():
	### analysis run on each participant and displayed together ###
	# load in all the data
	participants = list()
	interactions = list()

	for pNum in range(HIGHEST_P_NUMBER+1): #cycle through all participants

		settings = setup(dataset='USF', data_loc=DATA_LOC, subject_n=pNum)

		pid = str(pNum)
					
		try:
			interact = (interactionData(settings.getFileName('viewLog')))
			
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

	# figName = "all_interactions_x_time"
	# pylab.figure(figName)
	# pylab.plot(interactions[0].x,interactions[0].v,
			   # interactions[1].x,interactions[1].v,
			   # interactions[2].x,interactions[2].v,
			   # interactions[3].x,interactions[3].v,
			   # interactions[4].x,interactions[4].v,
			   # interactions[5].x,interactions[5].v,
			   # interactions[6].x,interactions[6].v,
			   # interactions[7].x,interactions[7].v,
			   # interactions[8].x,interactions[8].v,
			   # interactions[9].x,interactions[9].v,
			   # interactions[10].x,interactions[10].v)	#TODO: add more if applicable
	# fname = DATA_LOC+figName+'.png'
	# pylab.plt.savefig(fname, dpi = 100)
			   
			   
	# shift to time since start...
	for pnum in range(0,len(interactions)):
		start_t = min(interactions[pnum].t)
		for i in range (0, len(interactions[pnum])):
			interactions[pnum].t[i] -= start_t
		
	# figName = "all_interactions_x_time_since_study_start"
	# pylab.figure(figName)
	# pylab.plot(interactions[0].t,interactions[0].v,
			   # interactions[1].t,interactions[1].v,
			   # interactions[2].t,interactions[2].v,
			   # interactions[3].t,interactions[3].v,
			   # interactions[4].t,interactions[4].v,
			   # interactions[5].t,interactions[5].v,
			   # interactions[6].t,interactions[6].v,
			   # interactions[7].t,interactions[7].v,
			   # interactions[8].t,interactions[8].v,
			   # interactions[9].t,interactions[9].v,
			   # interactions[10].t,interactions[10].v)	#TODO: add more if applicable
	# fname = DATA_LOC+figName+'.png'
	# pylab.plt.savefig(fname, dpi = 100)

	# shift all to same daily cycle
	for pnum in range(0,len(interactions)):
		timeOfDay = interactions[pnum].x[0]	#assuming earliest time is first...
		ToD_start = (timeOfDay.hour*60 + timeOfDay.minute) * 60
		for i in range (0, len(interactions[pnum])):
			interactions[pnum].t[i] += ToD_start
			
	figName = "all_interactions_x_time_of_day_since_study_start"
	pylab.figure(figName)
	try:
		assert(len(interactions) == 15)
	except AssertionError as e:
		print 'len(interactions)=',len(interactions)
		raise
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
			   interactions[10].t,interactions[10].v,
			   interactions[11].t,interactions[11].v,
			   interactions[12].t,interactions[12].v,
			   interactions[13].t,interactions[13].v,
               interactions[14].t,interactions[14].v)	#TODO: add more if applicable
	fname = DATA_LOC+figName+'.png'
	pylab.plt.savefig(fname, dpi = 100)
		
