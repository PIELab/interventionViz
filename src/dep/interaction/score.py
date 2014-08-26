import pylab

from src.dep.interaction.interactionData import interactionData


def plot(settings):
	# load interaction data
	interact = interactionData()
	interact.getData(settings['interactionFileLoc'])

	interactScore,interactDate = segmentInteractionIntoDays(interact)

	pltName = 'interaction vs day'
	print 'making plot "'+pltName+'"'
	pylab.figure(pltName)
	pylab.plt.bar(interactDate,interactScore)

	pylab.plt.ylabel('day')
	pylab.plt.xlabel('interaction score')

	pylab.plt.draw()

# take in a full list of interactions and return a list of day scores & dates
def segmentInteractionIntoDays(interact):
	# generate interaction 'score'
	interactScore = list()
	interactDate   = list() # list of interaction data segemented by day
	# gather data from timestamps in interact.x together by day
	i = 0
	while i+1 < len(interact.x)-1:
		score = 0
		#print str(interact.x[i].date()) +'=?='+str(interact.x[i+1].date())
		while interact.x[i].date() == interact.x[i+1].date(): # count up all in same day
			date = interact.x[i]
			#print str(i)
			score += getInfluenceEffect(interact,i)
			i+=1
			if i+1 > len(interact.x)-1:
				break
		score += getInfluenceEffect(interact,i)
		i+=1
		# now score is day's total, add it to the list
		interactScore.append(score)
		interactDate.append(date)
	return [interactScore,interactDate]

# return the influence score for a given interaction descriptor
def getInfluenceEffect(interaction,i):
	return (interaction.a1[i]
	       +interaction.a2[i]
	       +interaction.a3[i]
	       +(interaction.p1[i]
	        +interaction.p2[i]
	        +interaction.p3[i]))	# passive (sedentary) days are added b/c they should already be negative valued

### PRIVATE METHODS ###
