# This is just a wrapper script to attempt to pull in your
# custom configuration.  If custom config is not available
# (like at initial project creation), this will provide
# suitable defaults for operation.
#
# As part of setup you should copy the vars below to a 
# file named myconfig.py and set them appropriately for
# your installation.

try:
    from myconfig import *
except ImportError:
    # Customized config not available, use defaults
    #NOTE: you should copy these vars to "myconfig.py" and update
    #      for your own installation
    SITE_BASE = r'http://no_base_site_set_yet.com/icanhelp/'

    # Set false to use day/month/year convention
    DATE_MONTH_FIRST = True
    # Set offset from host machine to local time in seconds
    #   used to send reminder emails appropriately
    # Generally a server would be running with UTC time:
    # eg) value for arizona = -7 hours = -7*3600 = -25200
    DATE_UTC_TO_LOCAL_OFFSET_SEC = 0

    # SMTP Config (needed for sending emails)
    SMTP_SERVER = 'smtp.gmail.com'
    SMTP_PORT = 587
    SMTP_USER = 'bogus.email@gmail.com'
    SMTP_PASS = 'bogus password'
