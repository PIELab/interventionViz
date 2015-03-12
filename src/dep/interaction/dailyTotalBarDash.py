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
			interact = interactionData(fileName=settings.getFileName('viewLog'),timeScale='daily')
			
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

	maxStudyLen = max([len(interact.dailyTotals) for interact in interactions])
	
	# make the plots
	figName = "interactions_sparkBars"
	pylab.figure(figName)
	pylab.subplots_adjust(left=0,bottom=0,right=1,top=1,wspace=0,hspace=0)
	
	num = 0
	for interact in interactions:
		# make all data the same length so bars are sime width
		while len(interact.dailyTotals) < maxStudyLen:
			interact.dailyTotals.append(-1)
		# plot
		pylab.subplot(len(interactions),1,num)
		pylab.bar(range(len(interact.dailyTotals)),interact.dailyTotals,width=.5)
		num += 1
		
