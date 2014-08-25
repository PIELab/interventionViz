import pylab
from src.settings import setup

### analysis run on all data: ###

# t-tests #

import src.interaction_x_PA.tTest_paired as tTest_dep
tTest_dep.plot(dataset='USF',dataLoc='../subjects/') # use dataset='test' to select sample dataset
pylab.plt.savefig('tTest_paired.png')

import src.interaction_x_PA.tTest_indep as tTest_indep
tTest_indep.plot(dataset='USF',dataLoc='../subjects/')
pylab.plt.savefig('tTest_indep.png')

pylab.show()

# dashboards #

import src.PA.scatterplotDashboard as PAscatterDash
PAscatterDash.plot()

import src.interaction.scatterplotDashboard as interactionScatterDash
interactionScatterDash.plot()

import src.interaction.sparkLineDashboard as sparkDash
sparkDash.plot()

import src.interaction.allOnOne as multiInteract
multiInteract.plot()

import src.interaction.dailyTotalBarDash as dailyInteracts
dailyInteracts.plot()

import src.interaction_x_PA.scatterplotDashboard as masterDash
masterDash.plot()

pylab.show()
