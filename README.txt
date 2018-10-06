============
Simple Setup
============

With docker installed you can get up and running with a single command:

  docker run -p 8080:8080 mongi3/icanhelp

Now if you visit localhost:8080 in your web browser you should see the site.

==========
Background
==========
icanhelp was a quick reaction program (read a few evenings) created to 
aid my wife after she got called as a compassionate service leader at 
church.  There is certainly a lot that could be improved for 
more general use.

One of the primary goals was to make this easy for general users to use.
We didn't want the burden of creating accounts which would make things less
accessible and may give people problems if they forgot credentials.  It's hard
enough to get people to help out without additional burden!

Here's how it works.  An administrator can create a help listing providing
some general details about what is needed, and also creating more specific
items for signup.  The creator then sends an email from their personal account
to all those who may be interested containing a link to the help signup as well
as more details that may have been inappropriate for a general audience on
the website itself.  Those who receive the email can then click the link
and signup for specific items by providing their name and optionally their
phone and email addresses.  If they provide email's they'll receive a 
confirmation email and an automatic reminder.  The administrator will be 
emailed anytime someone signs up.  When the event rolls around, if the
user did not provide an email, the reminder will be sent to the creating admin
so they can manually make a reminder if they so choose.

The admin can of course log in at any time to check out who has signed up and
make modifications as required.

The reason it was setup this way was for simplicity and to prevent extraneous
personal information from being stored on the web.  It takes extra work
to setup SSL security and such.  Also we generally want
the least amount of personal details posted to the general web as possible.
(this can also make it easier to get approval from any authorities who
may object to such a site.)

Originally there was just a single admin, but I later added the ability for
multiple admin accounts to be created so that different people/functions
could have their own postings for their own purposes.

Below is some basic setup info to help those who may attempt to take this
code and replicate something on their own.


=============
Items of Note
=============
In order for the confirmation (at signup) and reminder email scripts to work 
you'll need to follow the instructions in config.py to provide your own stmp info.  
For this site I created a gmail account and provided those credentials.

The site uses sqlite database to store information.  Before using you'll need
to create the database file.  I've got a function to do this which you can
run as follows:

cd icanhelp #wherever you put things
python # start python shell
import model # imports code in model.py
model.initDb()

You should now have a db.sqlite file in the icanhelp directory.

----

You'll also want to update the email weblinks to point to your instance's url...


==============
Using as Admin
==============

The admin login page is just a hidden link at the bottom of the page.
Click on the period in the copyright notice to go to the admin login page.

When you initialized the database above, a single user was created with the
following credentials:

username: admin
password: admin

You'll of course want to login as admin and change this to something different.

Any admin can create additional admin accounts.  Each admin however can only
see postings that they have created.  The "admin" user has special rights
however and is able to see all postings from other accounts.

-------------

I'm sure there is more to tell but that's all I can think of at the moment...

-Jeff
