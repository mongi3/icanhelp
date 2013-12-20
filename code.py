#!/usr/bin/env python

""" Using webpy 0.3 """
import web
import model
import time
import hashlib

import utils
from config import URL_BASE

import emailconfirm

### Url mappings

urls = (
    '/', 'Index',
    '/new', 'New',
    '/view/(\d+)', 'View',
    '/delete/(\d+)', 'Delete',
    '/edit/(\d+)', 'Edit',
    '/newitem/(\d+)', 'NewItem',
    '/deleteitem/(\d+)', 'DeleteItem',
    '/edititem/(\d+)', 'EditItem',
    '/helpsignup/(\d+)', 'HelpSignup',
    '/login', 'Login',
    '/logout', 'Logout',
    '/error/(.*)', 'Error',
    '/helpconfirm/(\d+)', 'HelpConfirm',
    '/newadmin', 'NewAdmin',
    '/editadmin', 'EditAdmin',
)

app = web.application(urls, globals())

# This statement is more complicated than just the session line so that
# debug prompts that cause reload of the module work properly.
if web.config.get('_session') is None:
    session = web.session.Session(app, web.session.DiskStore('sessions'), initializer={'admin': False, 'userId': None})
#    session = web.session.Session(app, web.session.DBStore(model.db,'SessionData'), initializer={'admin': False})
    web.config._session = session
else:
    session = web.config._session


### Templates
t_globals = {
    'session': session,
    'utils'  : utils,
    'model'  : model,
    'URL_BASE': URL_BASE,
}
render = web.template.render('templates', base='base', globals=t_globals)




# Constants



class Index:
    def GET(self):
        """ Show page """
        posts = model.get_posts()
        for post in posts:
            # Post is set active only if it has an item yet to occur
            post.active = False
            items = model.get_items(post.id)
            for item in items:
                if not utils.date_in_past(item.date):
                    post.active = True
        return render.index(posts)


class New:
    # Build contact list of dropdown
    contact_list = [(contact.id,contact.name) for contact in model.get_contacts()]
    form = web.form.Form(
        web.form.Textbox('title', web.form.notnull, size=30, description="Title:"),
        web.form.Textarea('details', web.form.notnull, rows=10, cols=65, description="Details:"),
        web.form.Button('Done', type='submit')
        )
    
    def GET(self):
        if not session.admin:
            authorization_error()
        form = self.form()
        return render.new(form)

    def POST(self):
        if not session.admin:
            authorization_error()
        form = self.form()
        if not form.validates():
            return render.new(form)
        post_id = model.new_post(form.d.title, form.d.details, session.userId)
        raise web.seeother('/view/%d' % post_id)


class View:
    def GET(self, id):
        """ View single post """
        id = int(id)
        post_data = model.get_post(id)
        if not post_data:
            argument_error()
        if session.admin and not model.authorized_user(session.userId, post_data.contactId):
            authorization_error()
        # Modify details of post_data for display.  Need to be able to handle
        # newlines in textarea data in a websafe way.
        post_data.details = web.net.websafe(post_data.details)
        post_data.details = utils.nl2br(post_data.details)
        item_data = model.get_items(id)
        contact_data = model.get_contact_data(post_data.contactId)
        return render.view(post_data, item_data, contact_data)


class Delete:
    def GET(self, id):
        if not session.admin:
            authorization_error()
        post = model.get_post(int(id))
        if not model.authorized_user(session.userId, post.contactId):
            authorization_error()
        return render.delete(post)

    def POST(self, id):
        if not session.admin:
            authorization_error()
        post = model.get_post(int(id))
        if not model.authorized_user(session.userId, post.contactId):
            authorization_error()
        model.del_post(int(id))
        raise web.seeother('/')


class Edit:
    def GET(self, id):
        if not session.admin:
            authorization_error()
        post = model.get_post(int(id))
        if not model.authorized_user(session.userId, post.contactId):
            authorization_error()
        form = New.form()
        form.fill(post)
        return render.edit(post, form)

    def POST(self, id):
        if not session.admin:
            authorization_error()
        #TODO: take care of display issue with details (textarea data)
        form = New.form()
        post = model.get_post(int(id))
        if not model.authorized_user(session.userId, post.contactId):
            authorization_error()
        if not form.validates():
            return render.edit(post, form)
        model.update_post(int(id), form.d.title, form.d.details, form.d.contactId)
        raise web.seeother('/view/%d' % int(id))


class NewItem:
    form = web.form.Form(
        web.form.Textbox('date', web.form.regexp(r'^(0[1-9]|1[012])/(0[1-9]|[12][0-9]|3[01])/(19|20)\d\d$', 'Must be in form mm/dd/yyyy'), size=8, description="Date:"),
        web.form.Textbox('description', web.form.notnull, size=30, description="Description:"),
        web.form.Textbox('count', web.form.regexp(r'^\d+$', 'Must be a number'), size=2, description="Number of Entries:", value='1'),
        web.form.Button('Done', type='submit')
        )
    
    def GET(self, post_id):
        if not session.admin:
            authorization_error()
        post_id = int(post_id)
        post = model.get_post(post_id)
        if not model.authorized_user(session.userId, post.contactId):
            authorization_error()
        form = self.form()
        return render.newitem(post, form)

    def POST(self, post_id):
        if not session.admin:
            authorization_error()
        post_id = int(post_id)
        post = model.get_post(post_id)
        if not model.authorized_user(session.userId, post.contactId):
            authorization_error()
        form = self.form()
        if not form.validates():
            post = model.get_post(post_id)
            return render.newitem(post, form)
        for idx in range(int(form.d.count)):
            model.new_help_item(post_id, form.d.date, form.d.description)
        raise web.seeother('/view/%d' % post_id)


class DeleteItem:
    def GET(self, item_id):
        if not session.admin:
            authorization_error()
        item = model.get_item(int(item_id))
        post = model.get_post(item.helpRequestId)
        if not model.authorized_user(session.userId, post.contactId):
            authorization_error()
        return render.deleteitem(post, item)

    def POST(self, item_id):
        if not session.admin:
            authorization_error()
        item_data = model.get_item(int(item_id))
        post = model.get_post(item_data.helpRequestId)
        if not model.authorized_user(session.userId, post.contactId):
            authorization_error()
        post_id = model.del_help_item(int(item_id))
        raise web.seeother('/view/%d' % item_data.helpRequestId)


class EditItem:
    form = web.form.Form(
        web.form.Textbox('date', web.form.regexp(r'^(0[1-9]|1[012])/(0[1-9]|[12][0-9]|3[01])/(19|20)\d\d$', 'Must be in form mm/dd/yyyy'), size=8, description="Date:"),
        web.form.Textbox('description', web.form.notnull, size=30, description="Description:"),
        web.form.Textbox('helpName', size=30, description="Helper Name:"),
        web.form.Textbox('helpEmail', size=30, description="Helper Email:"),
        web.form.Textbox('helpPhone', size=30, description="Helper Phone:"),
        web.form.Button('Done', type='submit')
        )
        
    def GET(self, id):
        if not session.admin:
            authorization_error()
        item = model.get_item(int(id))
        post = model.get_post(item.helpRequestId)
        if not model.authorized_user(session.userId, post.contactId):
            authorization_error()
        form = self.form()
        form.fill(item)
        return render.edititem(post, item, form)

    def POST(self, id):
        if not session.admin:
            authorization_error()
        #TODO: take care of display issue with details (textarea data)
        form = self.form()
        item = model.get_item(int(id))
        post = model.get_post(item.helpRequestId)
        if not model.authorized_user(session.userId, post.contactId):
            authorization_error()
        if not form.validates():
            return render.edititem(post, item, form)
        model.update_help_item(int(id), form.d.date, form.d.description, 
                     form.d.helpName, form.d.helpEmail, form.d.helpPhone)
        raise web.seeother('/view/%d' % item.helpRequestId)


class HelpSignup:
    #TODO: get email address validation working
    vemail = web.form.regexp(r".*@.*","must be a valid email address")
#    vemail = EmailRegexp(r".*@.*", "Email address not valid")

    form = web.form.Form(
        web.form.Textbox('helpName', web.form.notnull, size=30, description="Name:"),
        web.form.Textbox('helpEmail', size=30, description="Email:"),
        web.form.Textbox('helpEmail2', size=30, description="Repeat Email:"),
        web.form.Textbox('helpPhone', size=30, description="Phone:"),
        web.form.Button('Signup', type='submit'),
        validators = [ web.form.Validator("Email addresses do not match", 
                                        lambda i: i.helpEmail == i.helpEmail2),
                       web.form.Validator("Must provide either email or phone number", 
                                        lambda i: i.helpEmail != '' or i.helpPhone != ''),
                     ]
    )
        
    def GET(self, id):
        item = model.get_item(int(id))
        #TODO: should error checking like this be done elsewhere?
        if not item:   # Requested item doesn't exist
            raise web.seeother('/')
        if item.helpName:  # Someone has already signed up for this item
            raise web.seeother('/error/item_help_provided?req_id=%d' % int(item.helpRequestId))
        post = model.get_post(item.helpRequestId)
        form = self.form()
        return render.helpsignup(post, item, form)

    def POST(self, id):
        form = self.form()
        item = model.get_item(int(id))
        if not item:   # Requested item doesn't exist
            raise web.seeother('/')
        if item.helpName:  # Someone has already signed up for this item
            raise web.seeother('/error/item_help_provided?req_id=%d' % int(item.helpRequestId))
        if not form.validates():
            post = model.get_post(item.helpRequestId)
            return render.helpsignup(post, item, form)
        model.update_help_item(int(id), item.date, item.description, 
                     form.d.helpName, form.d.helpEmail, form.d.helpPhone)
        emailconfirm.sendConfirmationEmail(int(id))
        raise web.seeother('/helpconfirm/%d' % item.id)


class HelpConfirm:
    def GET(self, id):
        item = model.get_item(int(id))
        if not item:   # Requested item doesn't exist
            raise web.seeother('/')
        return render.helpconfirm(item)


class Login:
    form = web.form.Form(
        web.form.Textbox('username', web.form.notnull),
        web.form.Password('password', web.form.notnull),
        web.form.Button('Login', type='submit')
        )
        
    def GET(self):
        form = self.form()
        return render.login(form)

    def POST(self):
        form = self.form()
        if not form.validates():
            return render.login(form)
        pwdhash = hashlib.md5(form.d.password).hexdigest()
        session.user = None
        for contact in model.get_contacts():
            if form.d.username == contact.username and pwdhash == contact.passhash:
                #login successful
                session.userId = contact.id
                session.admin = True
                raise web.seeother('/')
        if not session.user:
            return render.login(form)


class Logout:
    def GET(self):
        session.userId = None
        session.admin = False
        raise web.seeother('/')


class Error:
    def GET(self, error):
        if error == 'bogus_arguments':
            title = 'Bogus Arguments for Page'
            msg = 'Click below to goto home page'
            link = ''
        elif error == 'item_help_provided':
            data = web.input(req_id=None)
            if data.req_id == None:
                return self.unknown_error()
            title = 'Help Already Provided'
            msg = 'Help has already been provded for this item.  Click link below to find other available items.'
            link = 'view/%s' % data.req_id
        elif error == 'not_authorized':
            title = 'Authorization Error'
            msg = 'You are not authorized to perform the requested operation.'
            link = ''
        else:
            return self.unknown_error()
        return render.error(title, msg, link)

    def unknown_error(self):
        title = 'Unknown Error'
        msg = 'Click link below to goto home page.'
        link = ''
        return render.error(title, msg, link)


def argument_error():
    """Call this function whenever invalid arguments are provided by user in 
    URL string"""
    raise web.seeother('/error/bogus_arguments')

def authorization_error():
    """Call this function whenever user attempts unauthorized action"""
    raise web.seeother('/error/not_authorized')

    
class NewAdmin:
    form = web.form.Form(
        web.form.Textbox('username', web.form.notnull, size=30, description="Username:"),
        web.form.Password('password', web.form.notnull, size=30, description="Password:"),
        web.form.Password('password2', web.form.notnull, size=30, description="Repeat Password:"),
        web.form.Textbox('name', web.form.notnull, size=30, description="Name:"),
        web.form.Textbox('email', web.form.notnull, web.form.regexp(r'.*@.*\..*', 'Invalid email'), size=30, description="Email:"),
        web.form.Textbox('email2', web.form.notnull, size=30, description="Repeat Email:"),
        web.form.Textbox('phone', web.form.notnull, size=30, description="Phone:"),
        web.form.Button('OK', type='submit'),
        validators = [ web.form.Validator("Passwords do not match", 
                                        lambda i: i.password == i.password2),
                       web.form.Validator("Email addresses do not match", 
                                        lambda i: i.email == i.email2),
                     ]
        )
        
    def GET(self):
        if not session.admin:
            authorization_error()
        form = self.form()
        return render.newadmin(form)

    def POST(self):
        if not session.admin:
            authorization_error()
        form = self.form()
        if not form.validates():
            return render.newadmin(form)
        passhash = hashlib.md5(form.d.password).hexdigest()
        model.add_contact(form.d.username, passhash, form.d.name, form.d.email, form.d.phone)
        raise web.seeother('/')


class EditAdmin:
        
    def GET(self):
        if not session.admin:
            authorization_error()
        admin = model.get_contacts(session.userId)
        #print admin
        form = NewAdmin.form()
        form.fill(admin)
        return render.editadmin(form)


    def POST(self):
        if not session.admin:
            authorization_error()
        form = NewAdmin.form()
        if not form.validates():
            return render.editadmin(form)
        passhash = hashlib.md5(form.d.password).hexdigest()
        model.update_contact(session.userId, form.d.username, passhash, form.d.name, form.d.email, form.d.phone)
        raise web.seeother('/')



if __name__ == '__main__':
    app.run()

