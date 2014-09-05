__author__ = 'tylar'

from datetime import datetime

def unix_time_to_nearest_minute_iso8601_string(timestamp):
    """
    converts ts->string and rounds to nearest minute
    :param timestamp: [ms]
    :return: ISO 8601 datetime string, eg: "2014-08-28 01:32:00"
    """
    timestamp/1000
    sec = timestamp % 60
    if sec < 30:
        timestamp -= sec  # round down
    else:
        timestamp += 60-sec  # round up

    return datetime.fromtimestamp(timestamp)#.strftime("%Y-%m-%d %H:%M:%S")

def add_min_to_iso8601_str(mins=1):
    """
    adds a minute to the given iso8601 string and returns
    :param mins:
    :return:
    """
    raise NotImplementedError()