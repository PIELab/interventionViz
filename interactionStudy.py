import pylab
from src.settings import setup

### analysis run on all data: ###

import src.interaction_x_PA.tTest_paired as tTest_dep
tTest_dep.plot(dataset='USF',dataLoc='../subjects/', paMethod='fitbit') # use dataset='test' to select sample dataset
pylab.plt.savefig('tTest_paired.png')

pylab.show()


import src.interaction.scatterplotDashboard as interactionScatterDash
interactionScatterDash.plot()

import src.interaction.sparkLineDashboard as sparkDash
sparkDash.plot()

import src.interaction.allOnOne as multiInteract
multiInteract.plot()

import src.interaction.dailyTotalBarDash as dailyInteracts
dailyInteracts.plot()

pylab.show()
