__author__ = 'tylar'

import csv
import warnings

from src.settings import setup, QUALITY_LEVEL, DATA_TYPES
from src.data.mAvatar.Data import DAY_TYPE
from src.data.Dataset import Dataset

EXPORTED_FILE_LOC = '../subjects/person_period_days.csv'

settings = setup(dataset='USF', dataLoc='../subjects/', subjectN=0)

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    data = Dataset(settings, min_quality=QUALITY_LEVEL.acceptable, trim=True, check=True,

                   used_data_types=[DATA_TYPES.fitbit, DATA_TYPES.avatar_views], avatar_view_freq=60)

# write the csv file
with open(EXPORTED_FILE_LOC, 'wb') as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(['id,day,intervention,seconds_viewed,step_count'])

    for subN in range(len(data)):
        subject = data.subject_data[subN]
        id = data.pids[subN]

        seconds_viewed = subject.avatar_view_data.get_day_ts(start=subject.meta_data.start, end=subject.meta_data.end)
        step_counts = subject.fitbit_data.get_day_ts(start=subject.meta_data.start, end=subject.meta_data.end)
        inverventions = subject.avatar_view_data.get_day_type_ts(start=subject.meta_data.start, end=subject.meta_data.end)

        # The PA vs. Sed is coded is -0.5 and 0.5:


        assert len(interventions) == len(seconds_viewed)
        assert len(interventions) == len(step_counts)

        # time is centered on the first day of use (i.e., day 1 using the system =0, day 2=1, etc).
        for dayN in range(len(inverventions)):  # for each day in the data...
            writer.writerow([id, dayN, interventions[dayN], seconds_viewed[dayN], step_counts[dayN]])


    # TODO: add:
    # any control variables (are there any factors we measured that might make sense?
    # Don't need them but just thought I'd check) have been checked for normality