"""
    Date related utility
"""

import calendar
from datetime import datetime, timedelta

from catalog.models import TLE

def format_inline_time(inline_time):
    return datetime.strptime(inline_time, '%Y%m%d%H%M%S')

def date2fraction(date):
    """
        Return the fractionnal value of the current date/time in the year
    """

    start_year = datetime(date.year, 1, 1, 0, 0, 0, 0)
    diff = date - start_year

    return diff.total_seconds() / timedelta(days=1).total_seconds()

def fraction2date(fraction):
    """
        Return the month, day and time matching to the epoch
    """

    seconds = fraction * 86400

    time = datetime.fromtimestamp(seconds)
    return time
