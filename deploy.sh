#!/bin/bash

cd /home/ubuntu/UltimateDecisionMaker/
echo "==========================="
echo "Pulling from master..."
echo "==========================="
git reset --hard
git pull origin/master
echo "==========================="
echo "Pull from master successful!"
echo "==========================="
echo " "
echo "==========================="
echo "Upgrading/Migrating database..."
echo "==========================="
cd /home/ubuntu/UltimateDecisionMaker/
flask db upgrade
flask db migrate
echo " "
echo "==========================="
echo "Restarting gunicorn..."
echo "==========================="
sudo systemctl gunicorn restart
echo " "
echo " "
echo "==========================="
echo      "Deploy to EC2 complete!"
echo "==========================="
