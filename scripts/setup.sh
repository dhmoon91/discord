#!/bin/bash
sudo pip3 install virtualenv
cd /home/ubuntu/discord
sudo pip3 install -r requirements.txt
cd /home/ubuntu/
sudo cp .env discord/
alembic upgrade head