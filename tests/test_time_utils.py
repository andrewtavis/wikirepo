"""
Time Utilities Tests
--------------------
"""

from datetime import datetime, date

import pytest
import pandas as pd

from wikirepo.data import time_utils


def test_interval_to_col_name():
    assert time_utils.interval_to_col_name("yearly") == "year"
    assert time_utils.interval_to_col_name("monthly") == "month"
    assert time_utils.interval_to_col_name("weekly") == "week"
    assert time_utils.interval_to_col_name("daily") == "day"


def test_truncate_date():
    d = date(2021, 1, 1)
    d_tup = (2021, 1, 1)
    assert time_utils.truncate_date(d=d_tup, interval="yearly") == "2021"
    assert time_utils.truncate_date(d=d, interval="yearly") == "2021"
    assert time_utils.truncate_date(d=d, interval="monthly") == "2021-01"
    assert time_utils.truncate_date(d=d, interval="weekly") == "2021-00"
    assert time_utils.truncate_date(d=d, interval="daily") == "2021-01-01"
    assert time_utils.truncate_date(d="2021", interval="Yearly") == "2021"
    assert time_utils.truncate_date(d="2021", interval=None) == "2021"
    with pytest.raises(AssertionError):
        assert time_utils.truncate_date(d="2021", interval=5) == "2021"


def test_truncate_date_col():
    df = pd.DataFrame([date(2021, 1, 1), date(2021, 1, 1)], columns=["time"])
    df = time_utils.truncate_date_col(df=df, col="time", interval="yearly")

    assert list(df["time"]) == ["2021", "2021"]


def test_incl_intervals():
    assert time_utils.incl_intervals() == ["yearly", "monthly", "weekly", "daily"]


def test_make_timespan():
    assert time_utils.make_timespan(timespan=None, interval=None) == None

    assert time_utils.make_timespan(timespan=date(2021, 1, 1), interval="yearly") == [
        date(2021, 1, 1)
    ]

    assert time_utils.make_timespan(
        timespan=(date(2021, 1, 1), date(2021, 1, 1)), interval="yearly"
    ) == [date(2021, 1, 1)]

    assert time_utils.make_timespan(
        timespan=(date(2020, 1, 1), date(2021, 1, 1)), interval="yearly"
    ) == [date(2021, 1, 1), date(2020, 1, 1)]

    assert time_utils.make_timespan(
        timespan=(date(2021, 1, 1), date(2020, 1, 1)), interval="yearly"
    ) == [date(2020, 1, 1), date(2021, 1, 1)]

    with pytest.raises(AssertionError):
        assert time_utils.make_timespan(
            timespan=(date(2021, 1, 1), date(2020, 1, 1)), interval="year"
        ) == [date(2020, 1, 1), date(2021, 1, 1)]

    assert time_utils.make_timespan(
        timespan=(date(2021, 1, 1), date(2021, 3, 1)), interval="monthly"
    ) == [date(2021, 3, 1), date(2021, 2, 1), date(2021, 1, 1)]

    assert time_utils.make_timespan(
        timespan=(date(2021, 1, 1), date(2021, 2, 1)), interval="weekly"
    ) == [
        date(2021, 1, 29),
        date(2021, 1, 22),
        date(2021, 1, 15),
        date(2021, 1, 8),
        date(2021, 1, 1),
    ]

    assert time_utils.make_timespan(
        timespan=(date(2021, 1, 1), date(2021, 1, 7)), interval="daily"
    ) == [
        date(2021, 1, 7),
        date(2021, 1, 6),
        date(2021, 1, 5),
        date(2021, 1, 4),
        date(2021, 1, 3),
        date(2021, 1, 2),
        date(2021, 1, 1),
    ]


def test_latest_date():
    timespan = (date(2021, 1, 1), date(2021, 1, 2))
    assert time_utils.latest_date(timespan=timespan) == date(2021, 1, 2)
    assert time_utils.latest_date(timespan=timespan[::-1]) == date(2021, 1, 2)


def test_earliest_date():
    timespan = (date(2021, 1, 1), date(2021, 1, 2))
    assert time_utils.earliest_date(timespan=timespan) == date(2021, 1, 1)
    assert time_utils.earliest_date(timespan=timespan[::-1]) == date(2021, 1, 1)


def test_truncated_latest_date():
    timespan = (date(2020, 1, 1), date(2021, 1, 1))
    assert (
        time_utils.truncated_latest_date(timespan=timespan, interval="yearly") == "2021"
    )


def test_truncated_earliest_date():
    timespan = (date(2020, 1, 1), date(2021, 1, 1))
    assert (
        time_utils.truncated_earliest_date(timespan=timespan, interval="yearly")
        == "2020"
    )
