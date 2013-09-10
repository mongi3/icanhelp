#!/usr/bin/env bash

apt-get update
apt-get install -y apache2 libapache2-mod-python
rm -rf /var/www
ln -fs /vagrant /var/www

# enable some modules in apache
sudo a2enmod python
sudo a2enmod rewrite

# change apache config to allow overrides by .htaccess
sed -i 's/AllowOverride None/AllowOverride All/' /etc/apache2/sites-available/default

# Restart apache
/etc/init.d/apache2 restart

# initialize DB for icanhelp site
pushd /vagrant/icanhelp > /dev/null
python -c "import model; model.initDb()"

# This is a bit hacky, but for some reason apache is unable to run stuff
# off the bat without this being done...
python code.py 1234 &
sleep 5
pkill python

popd > /dev/null

