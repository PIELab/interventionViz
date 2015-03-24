import pylab
import warnings

import pandas

from src.settings import setup, QUALITY_LEVEL, DATA_TYPES
from src.data.mAvatar.Data import DAY_TYPE
from src.data.Dataset import Dataset

import src.day_step_compare as day_step_compare
from src.post_view_event_steps_bars import plot_minutes, PLOT_TYPES
import sample_intervention
import knowMe


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
# roughly in reverse order that they appear in the paper...

# TODO: fig line graph of controlData avg(intervention)-avg(control)

print 'mAvatar active-sedentary comparison...'


#[8, 10, 11, 12, 13, 15, 26, 28, 32, 44, 49]
day_step_compare.plot_all_avg_diffs(data)

pylab.show()
# TODO: pass variables into this...
day_step_compare.plot_individual_mirrors_together(data)
pylab.show()

# TODO: shift view to a little bit before the event by modifying plot_minutes to take another parameter
print 'mAvatar post-event graphs comparison lines vs stack bars...'
# TODO: variance of the sum is NOT the sum of the variances.
plot_minutes(data, MINS=60, verbose=False, overlap_okay=True,
             selected_activity_type=DAY_TYPE.active, type=PLOT_TYPES.lines)
pylab.show()
# plot_minutes(data, MINS=60, verbose=False, overlap_okay=True,
#              selected_activity_type=DAY_TYPE.active, type=PLOT_TYPES.bars)
# pylab.show()

print 'control data all events...'
sample_intervention.plot_all_events()
pylab.show()

print 'control avg...'
sample_intervention.makePlot(type=PLOT_TYPES.lines)
pylab.show()
print 'control stackPlot...'
sample_intervention.makePlot(type=PLOT_TYPES.bars)
pylab.show()import sample_intervention


print 'knowMe stackPlot...'
knowMe.makePlot()
pylab.show()

# TODO http://matplotlib.org/examples/pylab_examples/arrow_demo.html maybe?
