""" analysis run on just one participant: """

import warnings

import pylab

from src.settings import setup
from src.data.subject.Subject import Subject


settings = setup(dataset='USF', dataLoc='../subjects/')  # use dataset='test' to select sample dataset

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    sub = Subject(settings)

sub.trim_data()
sub.integrity_check()

pylab.plt.figure('fitbit time series')
sub.fitbit_data.ts.plot()
pylab.plt.figure('avatar view time series')
sub.avatar_view_data.ts.plot()
pylab.plt.show()

#this one isn't very impressive, and I don't think it is working right now anyway
#import src.interaction.timeSeries.simple
#src.interaction.timeSeries.simple.plot()
#pylab.plt.show()

import src.dep.interaction.timeSeries.multicolorBars
src.dep.interaction.timeSeries.multicolorBars.plot(settings)

import src.dep.interaction.score
src.dep.interaction.score.plot(settings)

import src.dep.PA.timeSeries.dailyMinutes
src.dep.PA.timeSeries.dailyMinutes.plot(settings)

import src.dep.PA.score
src.dep.PA.score.plot(settings)

import src.dep.interaction_x_PA.timeseries
src.dep.interaction_x_PA.timeseries.plot(settings)

import src.dep.interaction_x_PA.scatterPlot
src.dep.interaction_x_PA.scatterPlot.plot(settings)

import src.dep.interaction_x_PA.stackedBars
src.dep.interaction_x_PA.stackedBars.plot(settings)

pylab.plt.show()
