import pylab
from src.settings import setup

### analysis run on all data: ###

# dashboards #

import src.interaction.scatterplotDashboard as interactionScatterDash
interactionScatterDash.plot()

import src.interaction.sparkLineDashboard as sparkDash
sparkDash.plot()

import src.interaction.allOnOne as multiInteract
multiInteract.plot()

import src.interaction.dailyTotalBarDash as dailyInteracts
dailyInteracts.plot()

pylab.show()


### analysis run on just one participant: ###

settings = setup(dataset='USF') # use dataset='test' to select sample dataset

#this one isn't very impressive, and I don't think it is working right now anyway
#import src.interaction.timeSeries.simple
#src.interaction.timeSeries.simple.plot()
#pylab.plt.show()

import src.interaction.timeSeries.multicolorBars
src.interaction.timeSeries.multicolorBars.plot(settings)

import src.interaction.score
src.interaction.score.plot(settings)

pylab.plt.show()
