"""
    Date related utility
"""

from datetime import datetime, timedelta

def get_days(date):
    """
        Return the fractionnal value of the current date/time in the year
    """
    start_year = datetime(date.year, 1, 1, 0, 0, 0, 0)
    diff = date - start_year

    return diff.total_seconds() / timedelta(days=1).total_seconds() + 1
