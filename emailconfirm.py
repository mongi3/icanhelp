#!/usr/bin/python

"""
This script contains a function that will email a confirmation after someone
has signed up for a help request item.  If they did not provide an email address,
the contact will be sent an email notifying them of this event.
"""

import web
import model
from datetime import datetime, timedelta


web.config.smtp_server = 'smtp.gmail.com'
web.config.smtp_port = 587
web.config.smtp_username = 'icanhelp.valencia@gmail.com'
web.config.smtp_password = 'helpvalencia'
web.config.smtp_starttls = True

def sendConfirmationEmail(item_id):
    item = model.get_item(int(item_id))
    # Get contact info for the help item
    post_data = model.get_post(int(item.helpRequestId))
    contact_data = model.get_contact_data(post_data.contactId)
    item.contactName = contact_data.name
    item.contactEmail = contact_data.email
    item.contactPhone = contact_data.phone

    if item.helpEmail:
        f = 'icanhelp.valencia@gmail.com'
        to = item.helpEmail
        cc = item.contactEmail
        subject = 'Confirmation: you signed up to help on %(date)s' % item
        msg = """Thanks for you willingness to help.
        
This email is to confirm that you signed up to help on %(date)s for the item "%(description)s".  More details can be found here:
        
http://jcopeland.homeip.net/icanhelp/view/%(helpRequestId)s
        
If you have any questions don't reply to this email.  Instead contact %(contactName)s
    email: %(contactEmail)s
    phone: %(contactPhone)s

Thanks!""" % item
        #print f, to, subject, msg
        web.sendmail(f,to,subject,msg,cc=cc)#,bcc='mongi3@gmail.com')
    else:
        # The person did not provide an email.  Instead an email will be sent
        # to the contact person informing them of the situation.
        f = 'icanhelp.valencia@gmail.com'
        to = item.contactEmail
        subject = 'Confirmation: Helper with no email'
        msg = """%(helpName)s signed up to help on %(date)s for item 
"%(description)s" but did not provide an email address.
        
Since no email is present, the website will be unable to provide them an automatic reminder.

Details can be found here:
        
http://jcopeland.homeip.net/icanhelp/view/%(helpRequestId)s
""" % item
        #print f, to, subject, msg
        web.sendmail(f,to,subject,msg)#,bcc='mongi3@gmail.com')
    


