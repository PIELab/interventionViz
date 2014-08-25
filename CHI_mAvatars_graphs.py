import pylab
from src.settings import setup

# TODO: load the data
# from src.data_set.DataSet import DataSet
# data = DataSet(settin)
from src.subject.Subject import Subject
settin = setup(dataset='USF', dataLoc='../subjects/', subjectN=8)
sub = Subject(settin)


# stacked bar chart & p-value
import src.interaction_x_PA.tTest_paired as tTest_dep
tTest_dep.plot(dataset='USF',dataLoc='../subjects/', paMethod='fitbit', bypass_data_check=True) # use dataset='test' to select sample dataset
pylab.plt.savefig('tTest_paired.png')
pylab.show()

# correlation scatterplot
import src.interaction_x_PA.scatterPlot as scatterPlot
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
import src.interaction.allOnOne as multiInteract
multiInteract.plot()

import src.interaction.dailyTotalBarDash as dailyInteracts
dailyInteracts.plot()

pylab.show()

import src.metaData.compareAllLengths as studyLen
studyLen.show()