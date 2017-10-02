"""
This file contains utility functions for use by icanhelp and templates.
"""

import time
from datetime import datetime, timedelta

def convert_date(date_str):
    """Convert date from 'mm/dd/yyyy' to 'Jan 02, Sat' """
    return time.strftime('%b %d, %a', time.strptime(date_str,'%m/%d/%Y'))

def date_valid(date_str):
    """Make sure date of valid mm/dd/yyyy or mm/dd/yy format"""
    std_date_str = standardize_date(date_str)
    return std_date_str is not None

def standardize_date(date_str):
    """standardize m/d/y format to MM/DD/YYYY"""
    valid_formats = [
        "%m/%d/%y",
        "%m/%d/%Y",
        "%m-%d-%y",
        "%m-%d-%Y",
        ]
    for fmt in valid_formats:
        try:
            dt = datetime.strptime(date_str, fmt)
            return dt.strftime("%m/%d/%Y")
        except:
            continue
    return None

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
