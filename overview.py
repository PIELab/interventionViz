import pylab

### analysis run on all data: ###

# t-tests #

import src.dep.interaction_x_PA.tTest_paired as tTest_dep
tTest_dep.plot(dataset='USF',dataLoc='../subjects/') # use dataset='test' to select sample dataset
pylab.plt.savefig('tTest_paired.png')

import src.dep.interaction_x_PA.tTest_indep as tTest_indep
tTest_indep.plot(dataset='USF',dataLoc='../subjects/')
pylab.plt.savefig('tTest_indep.png')

pylab.show()

# dashboards #

import src.dep.PA.scatterplotDashboard as PAscatterDash
PAscatterDash.plot()

import src.dep.interaction.scatterplotDashboard as interactionScatterDash
interactionScatterDash.plot()

import src.dep.interaction.sparkLineDashboard as sparkDash
sparkDash.plot()

import src.dep.interaction.allOnOne as multiInteract
multiInteract.plot()

import src.dep.interaction.dailyTotalBarDash as dailyInteracts
dailyInteracts.plot()

import src.dep.interaction_x_PA.scatterplotDashboard as masterDash
masterDash.plot()

pylab.show()
