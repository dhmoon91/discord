#!/bin/bash
cd /home/ubuntu/discord
sudo chown -R ubuntu:ubuntu /home/ubuntu/discord
nohup python3 bot.py > my.log 2>&1 &
echo $! > save_pid.txt
echo "finished"