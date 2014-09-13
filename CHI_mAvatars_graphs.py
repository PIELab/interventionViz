import warnings

import pylab
import pandas

from src.settings import setup, QUALITY_LEVEL, DATA_TYPES
from src.data.mAvatar.Data import DAY_TYPE
from src.data.Dataset import Dataset


settings = setup(dataset='USF', dataLoc='../subjects/', subjectN=0)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    data = Dataset(settings, min_quality=QUALITY_LEVEL.acceptable, trim=True, check=True,

                   used_data_types=[DATA_TYPES.fitbit, DATA_TYPES.avatar_views], avatar_view_freq=60)

UP_TO_DATE = True  # true if software versions are good
if pandas.version.version < '0.12.0':
    UP_TO_DATE = False
    print '\n\nWARN: Some analysis cannot be completed due to outdated pandas version ' + pandas.version.version + '\n\n'


###################
### BEGIN plots ###
###################


import src.after_view_event_step_compare_scatter as after_event_scatter
after_event_scatter.plot_individuals_together(data, MINS=60, overlap_okay=True)
pylab.show()
after_event_scatter.plot_individuals(data, MINS=360, overlap_okay=True, show_dots=False)
pylab.show()
after_event_scatter.plot_individuals(data, MINS=60, overlap_okay=True, show_dots=True)
pylab.show()
after_event_scatter.plot(data, MINS=60, overlap_okay=True, selected_event_type=None)
pylab.show()

import src.after_view_event_evaluation as step_x_view_score
step_x_view_score.plot_all_participant_scores(data, MINS=180, overlap_okay=True)
pylab.show()

if UP_TO_DATE:
    # correlation scatterplot
    import src.scatterplot as scatterplot
    scatterplot.plot(data)
    pylab.show()

    # stacked bar chart & p-value
    import src.paired_t_test as paired_t_test
    paired_t_test.plot(data)
    pylab.plt.show()

# plot histogram of view event lengths
events = data.get_aggregated_avatar_view_events()
lens = [event.length for event in events]
pylab.hist(lens, 100, histtype='stepfilled')
pylab.show()

if UP_TO_DATE:
    # avatar view "score"
    data.get_aggregated_avatar_view_scores().hist(bins=20, histtype='stepfilled')
    pylab.gcf().canvas.set_window_title('avatar view "score"')
    pylab.plt.show()

    #'daily step counts'
    data.get_aggregated_fitbit_days_ts().hist(bins=20, histtype='stepfilled')
    pylab.gcf().canvas.set_window_title('daily step counts')
    pylab.plt.show()

    data.get_aggregated_avatar_view_days().hist(bins=20, histtype='stepfilled')#'daily avatar view s')
    pylab.gcf().canvas.set_window_title('fitbit days step counts')
    pylab.plt.show()

# data.get_aggregated_fitbit_min_ts().hist(bins=50, histtype='stepfilled')#'minute step counts')
# pylab.gcf().canvas.set_window_title('fitbit minute step counts')
# pylab.plt.show()
#
#
#
#
# avatar_view_log_points = data.get_aggregated_avatar_view_log_points()#'avatar log points')
# pylab.hist(avatar_view_log_points, 100, histtype='stepfilled')
# pylab.gcf().canvas.set_window_title('avatar view logged points')
# pylab.plt.show()
#
#
# print 'plotting fitbit time series'
# pylab.plt.figure('fitbit time series')
# for sub in data.subject_data:
#    sub.fitbit_data.ts.plot()
#
# print 'plotting avatar views time series'
# pylab.plt.figure('avatar view time series')
# for sub in data.subject_data:
#    sub.avatar_view_data.ts.plot()
#
# pylab.plt.show()



# plot histogram of time between view events
intervals = list()
for event in events:
    try:
        intervals.append(event.time_until_next_event)
    except AttributeError:
        pass
pylab.hist(intervals, 100, histtype='stepfilled')
pylab.gcf().canvas.set_window_title('time between view events')
pylab.show()


import src.post_view_event_steps_bars as post_event_steps
# stacked bar chart for every view event, step counts in following 10m... aka:
# Figure ###: Sum of Step Counts Following An Avatar Viewing (minute-level)

### NO OVERLAP ALLOWED ###
# post_event_steps.plot_minutes(data, MINS=10, overap_okay=False, selected_event_type=None)
# pylab.show()
#
# post_event_steps.plot_minutes(data, MINS=10, overap_okay=False, selected_activity_type=DAY_TYPE.active)
# pylab.gcf().canvas.set_window_title('active')
# pylab.show()
#
# post_event_steps.plot_minutes(data, MINS=10, overap_okay=False, selected_activity_type=DAY_TYPE.sedentary)
# pylab.gcf().canvas.set_window_title('sedentary')
# pylab.show()
#
# post_event_steps.plot_minutes(data, MINS=10, overap_okay=False, selected_activity_type=DAY_TYPE.neutral)
# pylab.gcf().canvas.set_window_title('neutral')
# pylab.show() # this graph should be blank if phone got enough use...
#
# ## Figure ###: Sum of Step Counts Following An Avatar Viewing (hour-level)
# post_event_steps.plot_minutes(data, MINS=60, overap_okay=False)
# pylab.show()

post_event_steps.plot_minutes(data, MINS=60, overap_okay=False, selected_activity_type=DAY_TYPE.active)
pylab.gcf().canvas.set_window_title('active')
pylab.show()

post_event_steps.plot_minutes(data, MINS=60, overap_okay=False, selected_activity_type=DAY_TYPE.sedentary)
pylab.gcf().canvas.set_window_title('sedentary')
pylab.show()

post_event_steps.plot_minutes(data, MINS=60, overap_okay=False, selected_activity_type=DAY_TYPE.neutral)
pylab.gcf().canvas.set_window_title('neutral')
pylab.show() # this graph should be blank if phone got enough use...


post_event_steps.plot_minutes(data, MINS=60*3, overap_okay=False)
pylab.show()

post_event_steps.plot_minutes(data, MINS=60*6, overap_okay=False)
pylab.show()


### OVERLAP ALLOWED ###
post_event_steps.plot_minutes(data, MINS=10, overap_okay=True)
pylab.show()

## Figure ###: Sum of Step Counts Following An Avatar Viewing (hour-level)
post_event_steps.plot_minutes(data, MINS=60, overap_okay=True)
pylab.show()

post_event_steps.plot_minutes(data, MINS=60*3, overap_okay=True)
pylab.show()

# this is a huge amount of data that is likely to cause a python MemoryError
post_event_steps.plot_minutes(data, MINS=60*6, overap_okay=True)
pylab.show()


# Figure ###: comparison effect size of avatar view events sorted by amount of time after event being analyzed.
# (bar chart, height=effect size=difference/total step count, leftmost=smallest time (~1m), rightmost=most time (~12hrs)

# bar graph with active-day sedentary-day average difference in subject PA, separating subjects into 3 groups as explained

# additional (non-published) diagnostics:
import src.dep.interaction.allOnOne as multiInteract
multiInteract.plot()

import src.dep.interaction.dailyTotalBarDash as dailyInteracts
dailyInteracts.plot()
pylab.show()


import src.data.metaData.compareAllLengths as studyLen
studyLen.show()