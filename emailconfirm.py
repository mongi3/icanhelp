#!/usr/bin/python

"""
This script contains a function that will email a confirmation after someone
has signed up for a help request item.  If they did not provide an email address,
the contact will be sent an email notifying them of this event.
"""

import web
import model
from datetime import datetime, timedelta
import config

web.config.smtp_server = config.SMTP_SERVER
web.config.smtp_port = config.SMTP_PORT
web.config.smtp_username = config.SMTP_USER
web.config.smtp_password = config.SMTP_PASS
web.config.smtp_starttls = True

def sendConfirmationEmail(item_id):
    # don't even attempt if email config info has not been provided
    if not web.config.smtp_username:
        print "WARNING: email user/password not configured.  Ignoring attempt to send confirmation email."
        return

    item = model.get_item(int(item_id))
    # Get contact info for the help item
    post_data = model.get_post(int(item.helpRequestId))
    contact_data = model.get_contact_data(post_data.contactId)
    item.contactName = contact_data.name
    item.contactEmail = contact_data.email
    item.contactPhone = contact_data.phone
    item.url = "%s/view/%s" % (config.SITE_BASE, item.helpRequestId)

    if item.helpEmail:
        f = web.config.smtp_username
        to = item.helpEmail
        cc = item.contactEmail
        subject = 'Confirmation: you signed up to help on %(date)s' % item
        msg = """Thanks for you willingness to help.
        
This email is to confirm that you signed up to help on %(date)s for the item "%(description)s".  More details can be found here:
        
%(url)s
        
If you have any questions don't reply to this email.  Instead contact %(contactName)s
    email: %(contactEmail)s
    phone: %(contactPhone)s

Thanks!""" % item
        #print f, to, subject, msg
        web.sendmail(f,to,subject,msg,cc=cc)
    else:
        # The person did not provide an email.  Instead an email will be sent
        # to the contact person informing them of the situation.
        f = web.config.smtp_username
        to = item.contactEmail
        subject = 'Confirmation: Helper with no email'
        msg = """%(helpName)s signed up to help on %(date)s for item 
"%(description)s" but did not provide an email address.
        
Since no email is present, the website will be unable to provide them an automatic reminder.

Details can be found here:
        
%(url)s
""" % item
        #print f, to, subject, msg
        web.sendmail(f,to,subject,msg)
    


