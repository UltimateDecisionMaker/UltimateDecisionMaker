#!/bin/bash

cd /home/ubuntu/UltimateDecisionMaker/
# making sure deploy script is executable..
chmod u+x deploy.sh
echo "==========================="
echo "Pulling from master..."
echo "==========================="
git reset --hard origin/master
echo "==========================="
echo "Pull from master successful!"
echo "==========================="
echo " "
echo "==========================="
echo "Upgrading/Migrating database..."
echo "==========================="
flask db upgrade
flask db migrate
echo " "
echo "==========================="
echo "Restarting gunicorn..."
echo "==========================="
sudo systemctl restart gunicorn
echo " "
echo " "
echo "==========================="
echo      "Deploy completed"
echo "==========================="
