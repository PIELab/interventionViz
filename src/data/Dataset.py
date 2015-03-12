__author__ = 'tylarmurray'

import pandas

from src.settings import QUALITY_LEVEL, DATA_TYPES, setup
from src.data.subject.Subject import Subject
from src.util.timestuff import unix_time_to_nearest_minute_iso8601_string, add_min_to_iso8601_str
import datetime

class TimeWindowError(Exception):
    pass


class Dataset(object):
    """
    defines a set of data with multiple subjects
    """
    def __init__(self, settings, min_quality=QUALITY_LEVEL.acceptable, used_data_types=DATA_TYPES.all, trim=True,
                 check=True, avatar_view_freq=60):
        """
        :param min_quality: minimum quality level of data to be considered in the dataset
        """
        self.settings = settings

        self.pids = settings.get_pid_list()

        self.excluded = settings.get_exluded_list(min_level=min_quality , used_data=used_data_types)

        for pid in list(self.pids):  # note: need to use copy b/c we are modifying as we go
            if pid in self.excluded:
                self.pids.remove(pid)
                #print 'removing ', pid

        set_uses = dict()
        for type in used_data_types:
            set_uses[type] = True

        self.subject_data = list()
        for pid in self.pids:
            self.subject_data.append(Subject(
                setup(dataset=settings.dataset, data_loc=settings.dataLoc, subject_n=pid),
                avatar_view_freq=avatar_view_freq,
                uses=set_uses
            ))
            if trim:
                self.subject_data[-1].trim_data()
            if check:
                self.subject_data[-1].integrity_check()

        print len(self), 'subjects loaded. pids = ', self.pids
        print 'excluding pids ', self.excluded

    def get_view_event_list(self):
        """
        :returns: list of view event information across all participants
        """
        ls = list()
        for sub in self.subject_data:
            ls += sub.avatar_view_data.get_view_event_list()
        return ls

    def get_aggregated_avatar_view_scores(self):
        """
        :returns: list with data from all subjects
        """
        ls = list()
        tm = list()
        for sub in self.subject_data:

            ts = sub.avatar_view_data.get_day_ts_score(start=sub.meta_data.start, end=sub.meta_data.end)

            for i in range(len(ts)):  # for each data point (1 day)
                ls.append(ts[i])
                tm.append(ts.index[i])

        return pandas.Series(data=ls, index=tm)

    def get_steps_after_time(self, time, mins, pnum, verbose=True):
        """
        :param time: time desired (units? format?)
        :param pnum: participant number
        :param mins: number of minutes after event you want
        :return: list of step counts for <mins> minutes after event (len=mins)
        """
        steps = list()
        for i in range(mins):
            try:
                steps.append(self.subject_data[pnum].fitbit_data.ts[time])
            except KeyError as e:
                if verbose:
                    print 'ERR:', e.message
                    print self.subject_data[pnum].fitbit_data.ts[:3]
                    print '...'
                    print self.subject_data[pnum].fitbit_data.ts[-3:]
                raise TimeWindowError("key not found '"+str(e.message)+"'")

            time += datetime.timedelta(minutes=1)

        return steps

    def get_steps_after_event(self, event, mins, overlap_okay=False, shift=0, verbose=False):
        """
        :param event: ViewEvent I'm looking up
        :param mins: number of minutes after event you want
        :param overlap_okay: bool; throw TimeWindowError if number of minutes
        :return: list of step counts for <mins> minutes after event (len=mins)
        """
        if not event.has_next_event:
            raise TimeWindowError('event has no following event, not sure if enough time. exclude?')
        elif (not overlap_okay) and event.time_until_next_event < (mins+shift)*60:  # if not enough time b4 next event
            raise TimeWindowError("insufficient time between events, might want to exclude this one.")
        # implied else:

        # TODO: assert that subject step data is in minute-ts format...

        # get the numerical index of the date in the fitbit data (for easier and faster iteration)

        #print event.tf
        #print unix_time_to_nearest_minute_iso8601_string(event.tf)
        #print event.tf + 60*shift*1000
        ind = unix_time_to_nearest_minute_iso8601_string(event.tf + 60*shift)
        #print ind

        return self.get_steps_after_time(ind, mins, event.pnum, verbose=verbose)


    def get_aggregated_avatar_view_events(self, verbose=True):
        """
        :returns: list with data from all subjects
        """
        ls = list()
        pnum = 0
        for sub in self.subject_data:
            events = sub.avatar_view_data.get_view_event_list(recovery_period=120, min_view_time=0, max_view_time=60)

            for evt in events:
                evt.pnum = pnum

            ls += (events)
            pnum += 1
        if verbose: print len(ls), 'events loaded from dataset'
        return ls

    def get_aggregated_avatar_view_log_points(self):
        """
        :returns: list with data from all subjects
        """
        ls = list()
        for sub in self.subject_data:
            for point in sub.avatar_view_data.log_points:
                ls.append(point.len)
        return ls

    def get_aggregated_avatar_view_days(self):
        """
        :returns: pandas ts with data from all subjects
        """
        ls = list()
        tm = list()
        for sub in self.subject_data:

            ts = sub.avatar_view_data.get_day_ts(start=sub.meta_data.start, end=sub.meta_data.end)

            for i in range(len(ts)):  # for each data point (1 day)
                ls.append(ts[i])
                tm.append(ts.index[i])

        return pandas.Series(data=ls, index=tm)

    def get_aggregated_fitbit_days_ts(self):
        """
        :returns: pandas ts with data from all subjects
        """
        ls = list()
        tm = list()
        for sub in self.subject_data:

            fb_ts = sub.fitbit_data.get_day_ts(start=sub.meta_data.start, end=sub.meta_data.end)

            for i in range(len(fb_ts)):  # for each data point (1 day)
                ls.append(fb_ts[i])
                tm.append(fb_ts.index[i])

        return pandas.Series(data=ls, index=tm)

    def select_events(self, mins, events, day_type, overlap_okay, verbose=False, shift=0):
        """
        returns subselection of events based on given criteria
        :param events: list of ViewEvents to search
        :param day_type: mAvatar.Data.DAY_TYPE to select
        :return: list of ViewEvents which are of given day_type
        """
        steps = list()  # list of lists of steps
        pnums = list()
        skipped = 0  # number of data points skipped
        undata = 0  # number of data points excluded due to selection criteria
        errors = {}
        for evt in events:  # lookup each event and get steps following event
            if evt.activity_type == day_type:
                try:
                    steps.append(self.get_steps_after_event(evt, mins, shift=shift, overlap_okay=overlap_okay))
                    pnums.append(evt.pnum)
                except TimeWindowError as e:  # if not enough time between events error
                    skipped += 1
                    try:  # keep a count of errors encountered
                        errors[e.message[:14]+'...'] += 1  # only use first part of error message (because of keys)
                    except KeyError:  # if this error has not yet been encountered
                        errors[e.message[:14]+'...'] = 1  # add an entry to the dict
                    pass
            else:
                undata += 1

        if verbose: print len(pnums), 'active step lists loaded,', skipped, 'skipped,',undata,'unselected. Error summary:'
        print errors
        return steps, pnums

    def get_aggregated_fitbit_min_ts(self):
        """
        :returns: pandas ts with data from all subjects
        """
        ls = list()
        tm = list()
        for sub in self.subject_data:  # graph & fit all together
            # TODO: assert that fitbit data is @ freq = 1min!!!
            fb_ts = sub.fitbit_data.ts

            for i in range(len(fb_ts)):  # for each data point (1 day)
                ls.append(fb_ts[i])
                tm.append(fb_ts.index[i])

        return pandas.Series(data=ls, index=tm)

    def __len__(self):
        return len(self.subject_data)

    def __iter__(self):
        i = 0
        while True:
            try:
                yield self.subject_data[i]
                i += 1
            except IndexError:
                return

    # though this method was desired, implementation (in this way) was deterimined to be infeasible.
    # def remove_avatar_view_outliers(self, max_view_time=30, replacement_time=5):
    #     """
    #     removes view periods from the avatar view data which are longer than max_view_time
    #     and replaces them with two view periods, once at the start of the event and once at the end.
    #     These two new view periods have a length of replacement_time.
    #     :param max_view_time: [seconds] maximum length to be considered a legitimate viewing.
    #     :param replacement_time: [seconds] length of view periods to be placed @ start & end of excessively long view event
    #     :return:
    #     """
    #
    #     for sub in self.subject_data:
    #         for i in len(sub.avatar_view_data):
    #             try:
    #                 if sub.avatar_view_data[i-max_view_time] == 1:
    #                     pass
    #             except IndexError:
    #                 continue


