import warnings

import pylab

from src.settings import setup, QUALITY_LEVEL
from src.data.Dataset import Dataset


settings = setup(dataset='USF', dataLoc='../subjects/', subjectN=0)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    data = Dataset(settings, min_quality=QUALITY_LEVEL['acceptable'], trim=True, check=True)
print len(data.subject_data), 'subjects loaded'

print 'plotting fitbit time series'
pylab.plt.figure('fitbit time series')
for sub in data.subject_data:
    sub.fitbit_data.ts.plot()

print 'plotting avatar views time series'
pylab.plt.figure('avatar view time series')
for sub in data.subject_data:
    sub.avatar_view_data.ts.plot()

#pylab.plt.show()

# stacked bar chart & p-value
import src.paired_t_test as paired_t_test
paired_t_test.plot(data)
pylab.plt.show()

#import src.dep.interaction_x_PA.tTest_paired as tTest_dep
#tTest_dep.plot(dataset='USF',dataLoc='../subjects/', paMethod='fitbit', bypass_data_check=True) # use dataset='test' to select sample dataset
#pylab.plt.savefig('tTest_paired.png')
#pylab.show()

# correlation scatterplot
import src.dep.interaction_x_PA.scatterPlot as scatterPlot
scatterPlot.plot( setup(dataset='USF', dataLoc='../subjects/', subjectN=8) )
pylab.plt.savefig('scatterPlot.png')
pylab.show()

# bar graph with active-day sedentary-day average difference in subject PA, separating subjects into 3 groups as explained


# Figure ###: Sum of Step Counts Following An Avatar Viewing (minute-level)
# Figure ###: Sum of Step Counts Following An Avatar Viewing (10m-level)
# Figure ###: Sum of Step Counts Following An Avatar Viewing (hour-level)

# Figure ###: comparison effect size of avatar view events sorted by amount of time after event being analyzed.
# (bar chart, height=effect size=difference/total step count, leftmost=smallest time (~1m), rightmost=most time (~12hrs)


# additional (non-published) diagnostics:
import src.dep.interaction.allOnOne as multiInteract
multiInteract.plot()

import src.dep.interaction.dailyTotalBarDash as dailyInteracts
dailyInteracts.plot()

pylab.show()

import src.data.metaData.compareAllLengths as studyLen
studyLen.show()