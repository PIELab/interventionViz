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

# return the PA score for given inputs. 
# Weights here are chosen in an attempt to spread typical data across + and - values 
def getPAscore(vig,mod_vig,mod,light,sed):
	return 4*vig + 3*mod_vig + 2*mod + light - 0.7*sed

# return the PA score for given inputs.
# sedentary data here is not considered, so all values returned will be positive.
def getPAscore_postiveOnly(vig,mod_vig,mod,light,sed):
	return 4*vig + 3*mod_vig + 2*mod + light

	# generate daily PA 'score' for each day
def segmentPAIntoDays(PA,PAscoreFunction=getPAscore):
	PAscore = list()
	PAdate  = list()
	for i in range(0,len(PA.time)):
		PAscore.append( PAscoreFunction(PA.vig[i],PA.mod_vig[i],PA.mod[i],PA.light[i],PA.sedentary[i]) )
		PAdate.append(PA.time[i])
	PAscore = PAscore[::-1]	#invert the list to match interaction data
	PAdate  = PAdate[::-1]
	return [PAscore,PAdate]

# generate daily PA 'score' for each day
def segmentPAIntoDays_postiveOnly(PA):
	PAscore = list()
	PAdate  = list()
	for i in range(0,len(PA.time)):
		PAscore.append( getPAscore(PA.vig[i],PA.mod_vig[i],PA.mod[i],PA.light[i],PA.sedentary[i]) )
		PAdate.append(PA.time[i])
	PAscore = PAscore[::-1]	#invert the list to match interaction data
	PAdate  = PAdate[::-1]
	return [PAscore,PAdate]

