import pylab
import warnings

import pandas

from src.settings import setup, QUALITY_LEVEL, DATA_TYPES
from src.data.mAvatar.Data import DAY_TYPE
from src.data.Dataset import Dataset

import src.day_step_compare as day_step_compare
from src.post_view_event_steps_bars import plot_minutes, PLOT_TYPES, plot_difference

import sample_intervention
import knowMe

# some optional tests:
# from src.post_view_event_steps_bars import test_get_avg_list
# test_get_avg_list()

#knowMe.makePlots(type=PLOT_TYPES.bars, show=True, pre_win=10, post_win=40)
#knowMe.makePlots(type=PLOT_TYPES.bars, show=True)

### USF mAVATAR DATA LOADING ###
settings = setup(dataset='USF', data_loc='../subjects/', subject_n=0)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    data = Dataset(settings, min_quality=QUALITY_LEVEL.acceptable, trim=True, check=True,

                   used_data_types=[DATA_TYPES.fitbit, DATA_TYPES.avatar_views], avatar_view_freq=60)

UP_TO_DATE = True  # true if software versions are good
if pandas.version.version < '0.12.0':
    UP_TO_DATE = False
    print '\n\nWARN: Some analysis cannot be completed due to outdated pandas version ' + pandas.version.version + '\n\n'


# comparison of events selected with/without overlap from mAvatar dataset
# to demonstrate difference (especially at high time intervals like no-overlap for 3hrs around event)
#plot_minutes(data, MINS=12*60, overlap_okay=True, shift=-6*60, edgecolor='none')
#pylab.show()
plot_minutes(data, MINS=60, overlap_okay=True, shift=-30, edgecolor='none')
pylab.show()
#plot_minutes(data, MINS=60, overlap_okay=False, shift=-30)
#pylab.show()


### START ACTUAL VISUALS ###

# plot_minutes(data, MINS=80, shift=-20, overlap_okay=True, selected_activity_type=DAY_TYPE.active)
# pylab.show()
#
# knowMe.makePlot(type=PLOT_TYPES.bars)
# pylab.show()

# plot all event responses together
# print 'big control stackPlot with colored bars'
# sample_intervention.makePlot(type=PLOT_TYPES.bars, pre_win=15*60, post_win=15*60, color_events=True)
# pylab.show()

# print 'control data all events...'
# sample_intervention.plot_all_events()
# pylab.figure('smoothed')
sample_intervention.plot_all_events(smooth=7)
pylab.show()
# knowMe
# TODO: (maybe... not expecting anything interesting)
# mAvatar
# TODO: (maybe... not expecting anything interesting)

# # plot participant averages & global average response (lines)
# # ctrl
# print 'control avg...'
# sample_intervention.makePlot(type=PLOT_TYPES.lines)
# pylab.show()
# # knowMe
print 'knowMe lines...'
knowMe.makePlot(type=PLOT_TYPES.lines, selected_data='int_acc_cnts', smooth=7)
pylab.show()
# mAvatar
# looking at sedentary, active, or all not very interesting

#
# # plot stackGraphs of event response
# # ctrl
# print 'control stackPlot...'
# sample_intervention.makePlot(type=PLOT_TYPES.bars, pre_win=20, post_win=60, color_events=False)
# pylab.show()
# # knowMe
# print 'knowMe stackPlot...'
# knowMe.makePlot(type=PLOT_TYPES.bars)
# pylab.show()
# # mAvatar
# # looking at sedentary, active, or all not very interesting

# # plot differences
# # ctrl real vs random pt
# sample_intervention.makePlot(type=PLOT_TYPES.lines, comparison=True)
# # knowMe intervention vs other sms
# # TODO: knowMe control/experimental?
# # mAvatar sedentary vs active avatar
plot_difference(data, MINS=60, shift=-30, verbose=False, overlap_okay=True, smooth=7,
                control_event=DAY_TYPE.sedentary, experimental_event=DAY_TYPE.active, type=PLOT_TYPES.lines)
pylab.show()


# TODO http://matplotlib.org/examples/pylab_examples/arrow_demo.html maybe?
