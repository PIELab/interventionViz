import pylab

#import src.interaction.timeSeries.simple
#interaction.timeSeries.simple.plot()

import src.interaction.timeSeries.multicolorBars
src.interaction.timeSeries.multicolorBars.plot()

import src.PA.timeSeries.dailyMinutes
src.PA.timeSeries.dailyMinutes.plot()

import src.interaction_x_PA.scatterPlot
src.interaction_x_PA.scatterPlot.plot()

pylab.plt.show()
