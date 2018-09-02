"""
This file contains utility functions for use by icanhelp and templates.
"""

import time
from datetime import datetime, timedelta
from config import DATE_MONTH_FIRST


def convert_date(date_str):
    """Convert date from db storage format 'mm/dd/yyyy' to 'Sat, 02 Jan' """
    return time.strftime('%a, %d %b', time.strptime(date_str,'%m/%d/%Y'))

def date_valid(date_str):
    """Make sure user input date is valid format"""
    std_date_str = standardize_date(date_str)
    return std_date_str is not None

def standardize_date(date_str):
    """standardize input datestring to MM/DD/YYYY for db storage"""
    if DATE_MONTH_FIRST:
        valid_formats = [
            "%m/%d/%y",
            "%m/%d/%Y",
            "%m-%d-%y",
            "%m-%d-%Y",
        ]
    else:
        valid_formats = [
            "%d/%m/%y",
            "%d/%m/%Y",
            "%d-%m-%y",
            "%d-%m-%Y",
        ]

    for fmt in valid_formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%m/%d/%Y")
        except:
            continue
    return None

def get_date_validator_string():
    """Returns proper string for failed form validation"""
    if DATE_MONTH_FIRST:
        return 'MM/DD/YY'
    else:
        return 'DD/MM/YY'

def current_year_string():
    return str(datetime.now().year)

def nl2br(s):
    """Converts newlines \n to HTML breaks.  This is used to web-ify
    textarea input data."""
    return '<br />\n'.join(s.split('\n'))

def date_in_past(date_str):
    """Returns True if the date_str (mm/dd/yyyy) is for a day prior 
    to today"""
    now = datetime.now()
    item_time = datetime.strptime(date_str,'%m/%d/%Y')
    if item_time-now < timedelta(days=-1):
        inPast = True
    else:
        inPast = False
    return inPast
