# This is just a wrapper script to attempt to pull in your
# custom configuration.  If custom config is not available
# (like at initial project creation), this will provide
# suitable defaults for operation.
#
# As part of setup you should copy the vars below to a 
# file named myconfig.py and set them appropriately for
# your installation.

from __future__ import absolute_import, division, print_function

import os

DEFAULT_SITE_BASE = r'http://no_base_site_set_yet.com/icanhelp/'

try:
    from myconfig import *
except ImportError:
    # Customized config not available, use defaults
    #NOTE: you should copy these vars to "myconfig.py" and update
    #      for your own installation
    SITE_BASE = os.getenv('SITE_BASE', DEFAULT_SITE_BASE)
    if SITE_BASE == DEFAULT_SITE_BASE:
        print('WARNING: SITE_BASE not set... emails will not have appropriate links')

    # Set false to use day/month/year convention
    DATE_MONTH_FIRST = int(os.getenv('DATE_MONTH_FIRST', 1)) == True
    
    # Set offset from host machine to local time in seconds
    #   used to send reminder emails appropriately
    # Generally a server would be running with UTC time:
    # eg) value for arizona = -7 hours = -7*3600 = -25200
    DATE_UTC_TO_LOCAL_OFFSET_SEC = int(os.getenv('DATE_UTC_TO_LOCAL_OFFSET_SEC', '0'))
    if DATE_UTC_TO_LOCAL_OFFSET_SEC == 0:
        print('WARNING: DATE_UTC_TO_LOCAL_OFFSET_SEC not set!  reminder emails may be sent at wrong times')

    # SMTP Config (needed for sending emails)
    SMTP_SERVER = os.getenv('SMTP_SERVER', 'smtp.gmail.com')
    SMTP_PORT = os.getenv('SMTP_PORT', 587)
    SMTP_USER = os.getenv('SMTP_USER', '')
    SMTP_PASS = os.getenv('SMTP_PASS', '')

    if not SMTP_USER or not SMTP_PASS:
        print('WARNING: SMTP settings not set!  Emails will likely not function properly')
