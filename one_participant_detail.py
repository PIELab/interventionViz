""" analysis run on just one participant: """

import pylab
from src.settings import setup
from src.subject.Subject import Subject
import warnings

settings = setup(dataset='USF', dataLoc='../subjects/')  # use dataset='test' to select sample dataset

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    sub = Subject(settings)

sub.trim_data()
sub.integrity_check()

#this one isn't very impressive, and I don't think it is working right now anyway
#import src.interaction.timeSeries.simple
#src.interaction.timeSeries.simple.plot()
#pylab.plt.show()

#import src.interaction.timeSeries.multicolorBars
#src.interaction.timeSeries.multicolorBars.plot(settings)
#
#import src.interaction.score
#src.interaction.score.plot(settings)
#
#import src.PA.timeSeries.dailyMinutes
#src.PA.timeSeries.dailyMinutes.plot(settings)
#
#import src.PA.score
#src.PA.score.plot(settings)
#
#import src.interaction_x_PA.timeseries
#src.interaction_x_PA.timeseries.plot(settings)
#
#import src.interaction_x_PA.scatterPlot
#src.interaction_x_PA.scatterPlot.plot(settings)
#
#import src.interaction_x_PA.stackedBars
#src.interaction_x_PA.stackedBars.plot(settings)
#
#pylab.plt.show()
