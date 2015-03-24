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


### START ACTUAL VISUALS ###

# plot all event responses together
# ctrl
print 'control data all events...'
sample_intervention.plot_all_events()
pylab.show()
# knowMe
# TODO
# mAvatar
# TODO

# plot participant averages & global average response (lines)
# ctrl
print 'control avg...'
sample_intervention.makePlot(type=PLOT_TYPES.lines)
pylab.show()
# knowMe
print 'knowMe stackPlot...'
knowMe.makePlot(type=PLOT_TYPES.lines)
pylab.show()
# mAvatar
# looking at sedentary, active, or all not very interesting


# plot stackGraphs of event response
# ctrl
print 'control stackPlot...'
sample_intervention.makePlot(type=PLOT_TYPES.bars)
pylab.show()
# knowMe
print 'knowMe stackPlot...'
knowMe.makePlot(type=PLOT_TYPES.bars)
pylab.show()
# mAvatar
# looking at sedentary, active, or all not very interesting

# plot differences
# ctrl real vs random pt
# TODO: fig line graph of controlData avg(intervention)-avg(control)
# knowMe intervention vs other sms
# TODO: knowMe control/experimental?
# mAvatar sedentary vs active avatar
plot_difference(data, MINS=60, shift=-30, verbose=False, overlap_okay=True,
                control_event=DAY_TYPE.sedentary, experimental_event=DAY_TYPE.active, type=PLOT_TYPES.lines)
pylab.show()


# TODO http://matplotlib.org/examples/pylab_examples/arrow_demo.html maybe?
