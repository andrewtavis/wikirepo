"""
Functions querying time information

Contents
--------
  0. No Class
      interval_to_col_name
      truncate_date
      truncate_date_col
      incl_intervals
      make_timespan
      latest_date
      earliest_date
      truncated_latest_date
      truncated_earliest_date
"""

from datetime import datetime, date
from dateutil.rrule import rrule, YEARLY, MONTHLY, WEEKLY, DAILY


def interval_to_col_name(interval):
    """
    Queries the proper name of the column for timespans given an interval
    """
    interval = interval.lower()

    if interval == "yearly":
        return "year"
    elif interval == "monthly":
        return "month"
    elif interval == "weekly":
        return "week"
    elif interval == "daily":
        return "day"


def truncate_date(d, interval=None):
    """
    Truncates a date object given an interval
    """
    if interval is not None:
        if type(d) != str:  # hasn't been formatted already
            if type(d) == tuple:
                d = datetime.strptime(f"{d[0]}-{d[1]}-{d[2]}", "%Y-%m-%d").date()

            if interval == "yearly":
                return d.strftime("%Y")

            elif interval == "monthly":
                return d.strftime("%Y-%m")

            elif interval == "weekly":
                return d.strftime("%Y-%W")

            elif interval == "daily":
                return d.strftime("%Y-%m-%d")

        else:
            return d

    else:
        return d


def truncate_date_col(df, col, interval):
    """
    Truncates the date column of a df based on a provided interval
    """
    df[col] = df[col].map(lambda x: truncate_date(d=x, interval=interval))

    return df


def incl_intervals():
    """
    Queries the included intervals

    Note: timespans will not be able to be queried if their interval is not included
    """
    return ["yearly", "monthly", "weekly", "daily"]


def make_timespan(timespan=None, interval=None):
    """
    Queries a timespan given user input of strings, ints, or time values

    Parameters
    ----------
        timespan : two element tuple or list : contains datetime.date or tuple (default=None: (date.today(), date.today()))
            A tuple or list that defines the start and end dates to be queried
            Note 1: if True, then the full timespan from 1-1-1 to the current day will be queried
            Note 2: passing a single entry will query for that date only

        interval : str
            The time interval over which queries will be made
            Note 1: see data.time_utils for options
            Note 2: if None, then only the most recent data will be queried

    Returns
    -------
        formatted_timespan : list (contains datetime.date)
            The timespan formatted going back in time
    """
    if interval == None and timespan == None:
        # Most recent data wanted
        return

    order = -1  # default order is decreasing in time

    if timespan == None:
        timespan = (date.today(), date.today())
    if timespan == True:
        timespan = (date.min, date.today())
    elif len(timespan) == 1:
        timespan = (timespan[0], timespan[0])
    elif type(timespan) == date:
        timespan = (timespan, timespan)
    elif timespan[0] > timespan[1]:
        timespan = (timespan[1], timespan[0])
        order = (
            1  # user wants the dates to be increasing in df rows instead of the default
        )
    else:
        ValueError("An invalid value was passed to the 'timespan' argument.")

    if type(timespan[0]) == date:
        start_dt = timespan[0]
    elif type(timespan[0]) == tuple:
        start_dt = date(*timespan[0])

    if type(timespan[1]) == date:
        end_dt = timespan[1]
    elif type(timespan[1]) == tuple:
        end_dt = date(*timespan[1])

    if interval == "yearly":
        return [dt.date() for dt in rrule(YEARLY, dtstart=start_dt, until=end_dt)][
            ::order
        ]

    elif interval == "monthly":
        return [dt.date() for dt in rrule(MONTHLY, dtstart=start_dt, until=end_dt)][
            ::order
        ]

    elif interval == "weekly":
        return [dt.date() for dt in rrule(WEEKLY, dtstart=start_dt, until=end_dt)][
            ::order
        ]

    elif interval == "daily":
        return [dt.date() for dt in rrule(DAILY, dtstart=start_dt, until=end_dt)][
            ::order
        ]


def latest_date(timespan):
    """
    Returns the latest date in a timespan
    """
    if timespan[1] > timespan[0]:
        return timespan[1]
    else:
        return timespan[0]


def earliest_date(timespan):
    """
    Returns the earliest date in a timespan
    """
    if timespan[0] < timespan[1]:
        return timespan[0]
    else:
        return timespan[1]


def truncated_latest_date(timespan, interval):
    """
    Returns the truncated latest date in a timespan
    """
    return truncate_date(latest_date(timespan), interval=interval)


def truncated_earliest_date(timespan, interval):
    """
    Returns the truncated earliest date in a timespan
    """
    return truncate_date(earliest_date(timespan), interval=interval)
