import pylab
from src.settings import setup

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

import src.interaction_x_PA.scatterPlot
src.interaction_x_PA.scatterPlot.plot(settings)
pylab.plt.savefig('interactVsPAscatterPlot.png')

pylab.plt.show()
