import web
import os
from datetime import datetime

DB_FILE = os.path.join(os.path.dirname(__file__),'db.sqlite')
db = web.database(dbn='sqlite', db=DB_FILE)
#db._db_cursor().text_factory = sqlite3.OptimizedUnicode

def get_posts():
    return [post for post in db.select('HelpRequest', order='id DESC')]

def get_post(id):
    try:
        post_data = db.select('HelpRequest', where='id=$id', vars=locals())[0]
    except IndexError:
        post_data = None
    return post_data

def get_item(id):
    try:
        item_data = db.select('HelpItem', where="id=$id", vars=locals())[0]
    except IndexError:
        item_data = None
    return item_data

def get_items(post_id):
    """Returns all item data associated with a post in time sorted order."""
    item_data = db.select('HelpItem', where="helpRequestId=$post_id", vars=locals())
    tmp_items = []
    for item in item_data:
        item_time = datetime.strptime(item.date,'%m/%d/%Y')
        tmp_items.append((item_time,item))
    tmp_items.sort()
    sorted_items = [i[1] for i in tmp_items]
    return sorted_items

def get_contact_data(contact_id):
    try:
        data = db.select('Contact', where="id=$contact_id", vars=locals())[0]
    except IndexError:
        data = None
    return data
    
def new_post(title, details, contactId):
    """Adds new post to database and returns the index if the new post."""
    id = db.insert('HelpRequest', title=title, details=details, contactId=contactId)
    return id
#    for item in helpItems:
#        db.insert('HelpItem', date=item.date, description=item.desc, helpRequestId=id)


def del_post(id):
    db.delete('HelpItem', where="helpRequestId=$id", vars=locals())
    db.delete('HelpRequest', where="id=$id", vars=locals())

def update_post(id, title, details):
#    for item in helpItems:
#        db.update('HelpItem', where="id=$item.id", vars=locals(),
#            date=item.date, description=item.desc, 
#            helpName=item.helpName, helpEmail=item.helpEmail, 
#            helpPhone=item.helpPhone)
    db.update('HelpRequest', where="id=$id", vars=locals(),
        title=title, details=details)

def new_help_item(post_id, date, description):
    """Adds new help item to a post and returns the index of the new item."""
    id = db.insert('HelpItem', helpRequestId=post_id, date=date, description=description)
    return id
#    for item in helpItems:
#        db.insert('HelpItem', date=item.date, description=item.desc, helpRequestId=id)


def del_help_item(item_id):
    db.delete('HelpItem', where="id=$item_id", vars=locals())

def update_help_item(item_id, date, description, helpName, helpEmail, helpPhone):
    db.update('HelpItem', where="id=$item_id", vars=locals(), date=date, 
                description=description, helpName=helpName, helpEmail=helpEmail,
                helpPhone=helpPhone)


def get_contacts(id=None):
    if id == None:
        contacts = db.select('Contact')
    else:
        contacts = db.select('Contact', where="id=$id", vars=locals())[0]
    return contacts

def add_contact(username, passhash, name, email, phone):
    return db.insert('Contact', username=username, passhash=passhash, name=name, email=email, phone=phone)

def rm_contact(contactId):
    contactId = int(contactId)
    for post in get_posts():
        if post.contactId == contactId:
            del_post(post.id)
    return db.delete('Contact', where="id=$contactId", vars=locals())

def update_contact(contactId, username, passhash, name, email, phone):
    return db.update('Contact', where="id=$contactId", vars=locals(), username=username, passhash=passhash, name=name, email=email, phone=phone)


def authorized_user(userId, postId):
    """Returns True if the provided user is authorized modify the post, False
    otherwise."""
    # The initial user is allowed to modify any listing, otherwise only the
    # user that created the listing can modify it.
    return userId == 1 or userId == postId


def initDb():
   """Setup the database structure, clearing any existing database if it exists.
   This function should ONLY be called when initializing database when first
   setup."""
   import sqlite3
   try:
       os.remove(DB_FILE)
   except OSError:
       pass
   db = sqlite3.connect(DB_FILE)
   db.execute("""create table Contact
                     (id        INTEGER PRIMARY KEY AUTOINCREMENT,
                      username  TEXT,
                      passhash  TEXT,
                      name      TEXT,
                      email     TEXT,
                      phone     TEXT
                      )""")
   db.execute("""create table HelpRequest
                     (id         INTEGER PRIMARY KEY AUTOINCREMENT,
                      contactId  INTEGER,
                      title      TEXT,
                      details    TEXT,
                      FOREIGN KEY(contactId) REFERENCES Contact(id)
                      )""")
   db.execute("""create table HelpItem
                     (id             INTEGER PRIMARY KEY AUTOINCREMENT,
                      helpRequestId  INTEGER,
                      date           TEXT,
                      description    TEXT,
                      helpName       TEXT,
                      helpEmail      TEXT,
                      helpPhone      TEXT,
                      FOREIGN KEY(helpRequestId) REFERENCES HelpRequest(id)
                      )""")
   # init with single admin user
   #default password: "admin" <-- BE SURE TO CHANGE!
   db.execute("""insert into Contact (username,passhash,name,email,phone)
                 values ('admin','21232f297a57a5a743894a0e4a801fc3','administrator','asdf@asdf.com','555-5555')""")
   db.commit()
   db.close()
   



