import calendar
import collections
import datetime

Key = collections.namedtuple('Key', ['start', 'duration'])

DAYS_IN_WEEK = 7


def create_plan(start, end):
    """Takes in a datetime range, and returns the minimum number of
       hourly, daily, and weekly date ranges that can be used to
       represent the range.

    The start datetime is inclusive, whereas the end is exclusive.
    """
    
    def has_day_resolution(dt):
        return not (dt.minute or dt.second or dt.microsecond)

    if not has_day_resolution(start) or not has_day_resolution(end):
        raise ValueError(
            'Query planning is only supported for datetime ranges '
            'that have an hourly resolution; received [{0}, {1}).'.format(
                start, end))
    
    head, curr, tail = [], [], []
    
    if end - start >= datetime.timedelta(weeks=1):
        weekday = calendar.weekday(start.year, start.month, start.day)
        days_until_next_week = datetime.timedelta(days=DAYS_IN_WEEK - weekday)
        next_week = (datetime.datetime(
            year=start.year, month=start.month, day=start.day) +
                     days_until_next_week)
        if next_week - start == datetime.timedelta(weeks=1):
            next_week = start
        else:
            head = create_plan(start, next_week)

        while next_week + datetime.timedelta(weeks=1) <= end:
            curr.append(Key(next_week, '1w'))
            next_week += datetime.timedelta(weeks=1)
        
        tail = create_plan(next_week, end)
        
    elif end - start >= datetime.timedelta(days=1):
        next_day = (datetime.datetime(
            year=start.year, month=start.month, day=start.day) +
                    datetime.timedelta(days=1))
        if next_day - start == datetime.timedelta(days=1):
            next_day = start
        else:
            head = create_plan(start, next_day)

        while next_day + datetime.timedelta(days=1) <= end:
            curr.append(Key(next_day, '1d'))
            next_day += datetime.timedelta(days=1)

        tail = create_plan(next_day, end)

    elif end - start >= datetime.timedelta(hours=1):
        next_hour = start
        while next_hour + datetime.timedelta(hours=1) <= end:
            curr.append(Key(next_hour, '1h'))
            next_hour += datetime.timedelta(hours=1)
    
    return head + curr + tail
