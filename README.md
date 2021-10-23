# ICanHelp

## Simple Setup

With docker installed you can get up and running with a single command:

    docker run -p 8080:8080 ghcr.io/mongi3/icanhelp:master

Now if you visit localhost:8080 in your web browser you should see the site.

## Environment Variables

There are other environment variables if you want to customize various things inside the docker container.

If you want email confirmations and reminders to be sent, you must configure
some environment variables appropriately:

| Docker Environment Var. | Description |
| ----------------------- | ----------- |
| `-e SITE_BASE=<FQDN-for-host>`<br/> **Required** | Address to base of site used in emailed links. eg) `http://my_site.com/icanhelp/`
| `-e SMTP_SERVER=<address>`<br/> **Recommended** *Default: smtp.gmail.com* | Must be set properly to send confirmation and reminder emails.
| `-e SMTP_PORT=<portnum>`<br/> **Recommended** *Default: 587* | port for SMTP server
| `-e SMTP_USER=<username>`<br/> **Recommended** | username for SMTP authentication
| `-e SMTP_PASS=<password>`<br/> **Recommended** | password for SMTP authentication
| `-e DATE_UTC_TO_LOCAL_OFFSET_SEC=<Offset>`<br/> **Recommended** *Default: UTC* | Set offset for your timezone so reminder emails are sent at proper time.  eg) arizona=UTC-7 = -7*3600=-25200

In order to customize to local formats throughout the world:

| Docker Environment Var. | Description |
| ----------------------- | ----------- |
| `-e DATE_MONTH_FIRST=<0,1>`<br/> *Optional* *Default: 1* | Set 0 for day to be first in date strings

All together a command might look like the following:

```
docker run -d \
       --name icanhelp \
       -p 8080:8080 \
       -e SITE_BASE=http://www.site.com/ \
       -e SMTP_SERVER=smtp.gmail.com \
       -e SMTP_USER=user@gmail.com \
       -e SMTP_PASS=**** \
       -e DATE_UTC_TO_LOCAL_OFFSET_SEC=-25200 \
       -v /dir/for/icanhelp:/app/icanhelp/data \
       --restart=unless-stopped \
       ghcr.io/mongi3/icanhelp:master
```

Here is a rundown of the other arguments passed into the example `docker run`:

| Docker Arguments | Description |
| ---------------- | ----------- |
| `-p 8080:8080`<br/> **Recommended** | Maps to host port 8080 from docker internal port 8080
| `--restart=unless-stopped`<br/> **Recommended** | Automatically (re)starts on boot or in the event of a crash
| `-v /dir/for/icanhelp:/app/icanhelp/data`<br/> **Recommended** | Volumes for your database and logs to persist changes across docker image updates
| `--net=host`<br/> *Optional* | Alternative to `-p <port>:<port>` arguments (Cannot be used at same time as -p) if you don't run any other web application


## Background

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


## Items of Note

In order for the confirmation (at signup) and reminder email scripts to work 
you'll need to follow the instructions in config.py to provide your own stmp info.  
For this site I created a gmail account and provided those credentials.

The site uses sqlite database to store information.  Before using you'll need
to create the database file.  I've got a function to do this which you can
run as follows:

```
cd icanhelp #wherever you put things
python # start python shell
import model # imports code in model.py
model.initDb()
```

You should now have a db.sqlite file in the icanhelp directory.

----

You'll also want to update the email weblinks to point to your instance's url...


## Using as Admin

The admin login page is just a hidden link at the bottom of the page.
Click on the period in the copyright notice to go to the admin login page.

When you initialized the database above, a single user was created with the
following credentials:

```
username: admin
password: admin
```

You'll of course want to login as admin and change this to something different.

Any admin can create additional admin accounts.  Each admin however can only
see postings that they have created.  The "admin" user has special rights
however and is able to see all postings from other accounts.

