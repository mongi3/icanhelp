#!/usr/bin/env bash

###############
# APACHE SETUP
###############

# setup domainname (removes some annoying apache warnings)
mkdir -p /etc/apache2/conf.d
echo "ServerName $(cat /etc/hostname)" > /etc/apache2/conf.d/fqdn

# get apache installed with mod_python
apt-get update
apt-get install -y apache2 libapache2-mod-python
rm -rf /var/www
ln -fs /vagrant /var/www

# enable some modules in apache
sudo a2enmod python
sudo a2enmod rewrite

# change apache to run as vagrant user/grp (allows writing to file share areas)
sed -i 's/www-data/vagrant/' /etc/apache2/envvars
rm -rf /var/lock/apache2 #cleanup old lock file...

# change apache config to allow overrides by .htaccess
sed -i 's/AllowOverride None/AllowOverride All/' /etc/apache2/sites-available/default

# Restart apache
/etc/init.d/apache2 restart


################
# ICANHELP INIT
################

# initialize DB for icanhelp site
pushd /vagrant/icanhelp > /dev/null
python -c "import model; model.initDb()"

# This is a bit hacky, but for some reason apache is unable to run stuff
# off the bat without this being done...
#python code.py 1234 &
#sleep 5
#pkill python
#popd > /dev/null

# Add cron job for sending email reminders
# Send reminder emails for icanhelp
echo "0 2 * * * vagrant /vagrant/icanhelp/emailreminder.py >> /vagrant/icanhelp/emailLog.txt 2>&1" > /etc/cron.d/icanhelpEmailReminder


