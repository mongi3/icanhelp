#!/usr/bin/python

"""
This is a script to email a reminder the day before the help item someone
has signed up for is required.

In order to work properly, this script should be set to run as a daily cronjob
at the desired reminder time.  This script will examine the database and find
all help items that are due *the next day*.  If there a person has signed
up to help, they will be emailed a reminder.
"""

import web
import model
from datetime import datetime, timedelta


web.config.smtp_server = 'smtp.gmail.com'
web.config.smtp_port = 587
web.config.smtp_username = 'icanhelp.valencia@gmail.com'
web.config.smtp_password = 'helpvalencia'
web.config.smtp_starttls = True

now = datetime.now()

# Use database to find which items are due tomorrow
tomorrow_items = []
db = model.db
for item in db.select('HelpItem'):
    item_time = datetime.strptime(item.date,'%m/%d/%Y')
    t_delta = item_time - now
    if timedelta(days=0) < t_delta < timedelta(days=1):
        tomorrow_items.append(item)
    

# For each item, if a helper has signed up, send an email reminder (using
# data from the database about the item)

for item in tomorrow_items:
    if item.helpEmail:
        # Get contact info for the help item
        post_data = model.get_post(int(item.helpRequestId))
        contact_data = model.get_contact_data(post_data.contactId)
        item.contactName = contact_data.name
        item.contactEmail = contact_data.email
        item.contactPhone = contact_data.phone
        
        # Construct message
        f = 'icanhelp.valencia@gmail.com'
        to = item.helpEmail
        subject = 'Reminder: you signed up to help on %(date)s' % item
        msg = """Thanks for you willingness to help.
        
This is a reminder that you signed up to help on %(date)s for the item "%(description)s".  More details can be found here:
        
http://jcopeland.homeip.net/icanhelp/view/%(helpRequestId)s
        
If you have any questions don't reply to this email.  Instead contact %(contactName)s
    email: %(contactEmail)s
    phone: %(contactPhone)s

Thanks!""" % item
#        print f, to, subject, msg
        web.sendmail(f,to,subject,msg)#,bcc='mongi3@gmail.com')
    else:
        # If the person who signed up didn't provide an email address, the
        # contact person will instead get an email so they can contact the
        # person that signed up by phone or some other means.
        # Get contact info for the help item
        post_data = model.get_post(int(item.helpRequestId))
        contact_data = model.get_contact_data(post_data.contactId)
        item.contactName = contact_data.name
        item.contactEmail = contact_data.email
        item.contactPhone = contact_data.phone
        
        # Construct message
        f = 'icanhelp.valencia@gmail.com'
        to = item.contactEmail
        subject = 'Need Manual Reminder for help on %(date)s' % item
        msg = """The following person signed up to help on %(date)s for the item "%(description)s" but did not provide an email to send an auto reminder:
        
        Name: %(helpName)s
        phone: %(helpPhone)s
        
Details can be found here:
        
        http://jcopeland.homeip.net/icanhelp/view/%(helpRequestId)s""" % item
#        print f, to, subject, msg
        web.sendmail(f,to,subject,msg)#,bcc='mongi3@gmail.com')



