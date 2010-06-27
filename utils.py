"""
This file contains utility functions for use by icanhelp and templates.
"""

import time
from datetime import datetime, timedelta

def convert_date(date_str):
    """Convert date from 'mm/dd/yyyy' to 'Jan 02, Sat' """
    return time.strftime('%b %d, %a', time.strptime(date_str,'%m/%d/%Y'))
    
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
