#!/usr/bin/python

"""
This is a script to email a reminder the day before the help item someone
has signed up for is required.

In order to work properly, this script should be set to run as a daily cronjob
at the desired reminder time.  This script will examine the database and find
all help items that are due *the next day*.  If there a person has signed
up to help, they will be emailed a reminder.
"""

import os
import web
import model
from datetime import datetime, timedelta
import config
import utils

### Setup app DB
if not os.path.isfile(model.DB_FILE):
    model.initDb()

web.config.smtp_server = config.SMTP_SERVER
web.config.smtp_port = config.SMTP_PORT
web.config.smtp_username = config.SMTP_USER
web.config.smtp_password = config.SMTP_PASS
web.config.smtp_starttls = True

now = datetime.now()

try:
    offset_to_local = timedelta(seconds=config.DATE_UTC_TO_LOCAL_OFFSET_SEC)
except AttributeError:
    offset_to_local = timedelta(seconds=0)

# Use database to find which items are due tomorrow
tomorrow_items = []
db = model.db
for item in db.select('HelpItem'):
    item_time = datetime.strptime(item.date,'%m/%d/%Y')
    t_delta = item_time - now + offset_to_local
#    print item.date,t_delta
    if timedelta(days=0) < t_delta < timedelta(days=1):
#        print 'SEND EMAIL:',item.date,t_delta
        tomorrow_items.append(item)
    

# For each item, if a helper has signed up, send an email reminder (using
# data from the database about the item)

for item in tomorrow_items:
    post_data = model.get_post(int(item.helpRequestId))
    contact_data = model.get_contact_data(post_data.contactId)
    item.contactName = contact_data.name
    item.contactEmail = contact_data.email
    item.contactPhone = contact_data.phone
    item.url = "%s/view/%s" % (config.SITE_BASE, item.helpRequestId)
    item.date = utils.convert_date(item.date)

    if not item.helpName:
        # If the item doesn't have a name, no one is signed up.  Notify the
        # the contact person that the spot is still free.
        f = web.config.smtp_username
        to = item.contactEmail
        subject = 'No one signed up for help on %(date)s' % item
        msg = """No one signed up for help on %(date)s, item "%(description)s"
        
Details can be found here:
        
        %(url)s""" % item
    elif item.helpEmail:
        f = web.config.smtp_username
        to = item.helpEmail
        subject = 'Reminder: you signed up to help on %(date)s' % item
        msg = """Thanks for you willingness to help.
        
This is a reminder that you signed up to help on %(date)s for the item "%(description)s".  More details can be found here:
        
%(url)s
        
If you have any questions don't reply to this email.  Instead contact %(contactName)s
    email: %(contactEmail)s
    phone: %(contactPhone)s

Thanks!""" % item
    else:
        # If the person who signed up didn't provide an email address, the
        # contact person will instead get an email so they can contact the
        # person that signed up by phone or some other means.
        f = web.config.smtp_username
        to = item.contactEmail
        subject = 'Need Manual Reminder for help on %(date)s' % item
        msg = """The following person signed up to help on %(date)s for the item "%(description)s" but did not provide an email to send an auto reminder:
        
        Name: %(helpName)s
        phone: %(helpPhone)s
        
Details can be found here:
        
        %(url)s""" % item

    # Actually send the email
    print f, to, subject, msg
#    web.sendmail(f,to,subject,msg)

print '%d reminders sent %s' % (len(tomorrow_items), datetime.now())

