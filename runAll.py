import pylab
from src.settings import setup

### analysis run on all data: ###

# # t-tests #

import src.interaction_x_PA.tTest_paired as tTest_dep
tTest_dep.plot(dataset='USF',dataLoc='../subjects/') # use dataset='test' to select sample dataset
pylab.plt.savefig('tTest_paired.png')

import src.interaction_x_PA.tTest_indep as tTest_indep
tTest_indep.plot(dataset='USF',dataLoc='../subjects/')
pylab.plt.savefig('tTest_indep.png')

# dashboards #

import src.PA.scatterplotDashboard as PAscatterDash
PAscatterDash.plot()
pylab.savefig('PA_scatterplotDashboard.png',dpi=100)

import src.interaction.scatterplotDashboard as interactionScatterDash
interactionScatterDash.plot()
pylab.savefig('interaction_scatterplotDashboard.png',dpi=100)

import src.interaction.sparkLineDashboard as sparkDash
sparkDash.plot()
pylab.savefig('interaction_sparkLineDashboard.png',dpi=100)

import src.interaction_x_PA.scatterplotDashboard as masterDash
masterDash.plot()
pylab.savefig('masterDash.png',dpi=100)

### analysis run on just one participant: ###

settings = setup(dataset='USF') # use dataset='test' to select sample dataset

#this one isn't very impressive, and I don't think it is working right now anyway
#import src.interaction.timeSeries.simple
#src.interaction.timeSeries.simple.plot()
#pylab.plt.show()

import src.interaction.timeSeries.multicolorBars
src.interaction.timeSeries.multicolorBars.plot(settings)
pylab.plt.savefig('multicolorBars.png')

import src.interaction.score
src.interaction.score.plot(settings)
pylab.plt.savefig('interactionScore.png')

import src.PA.timeSeries.dailyMinutes
src.PA.timeSeries.dailyMinutes.plot(settings)
pylab.plt.savefig('dailyMinutes.png')

import src.PA.score
src.PA.score.plot(settings)
pylab.plt.savefig('PA-Score.png')

import src.interaction_x_PA.timeseries
src.interaction_x_PA.timeseries.plot(settings)
pylab.plt.savefig('interactVsPAtimeseries.png')

import src.interaction_x_PA.scatterPlot
src.interaction_x_PA.scatterPlot.plot(settings)
pylab.plt.savefig('interactVsPAscatterPlot.png')

import src.interaction_x_PA.stackedBars
src.interaction_x_PA.stackedBars.plot(settings)
pylab.plt.savefig('interactVsPAbars.png')

pylab.plt.show()
