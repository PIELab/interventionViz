import pylab
from src.PA.PAdata import PAdata

def plot(settings):
	# load interaction data
	data = PAdata(settings['PAfileLoc'])

	scores,dates = segmentPAIntoDays(data)

	pltName = 'physical activity vs day'
	print 'making plot "'+pltName+'"'
	pylab.figure(pltName)
	pylab.plt.bar(dates,scores)

	pylab.plt.ylabel('day')
	pylab.plt.xlabel('PA score')

	pylab.plt.draw()

	# generate daily PA 'score' for each day
def segmentPAIntoDays(PA):
	PAscore = list()
	PAdate  = list()
	for i in range(0,len(PA.time)):
		PAscore.append( getPAscore(PA.vig[i],PA.mod_vig[i],PA.mod[i],PA.light[i],PA.sedentary[i]) )
		PAdate.append(PA.time[i])
	PAscore = PAscore[::-1]	#invert the list to match interaction data
	PAdate  = PAdate[::-1]
	return [PAscore,PAdate]

# return the PA score for given inputs
def getPAscore(vig,mod_vig,mod,light,sed):
	return 4*vig + 3*mod_vig + 2*mod + light - 0.7*sed

