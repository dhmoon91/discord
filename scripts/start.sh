#!/bin/bash
cd /home/ubuntu/discord
nohup python3 bot.py > my.log 2>&1 &
echo $! > save_pid.txt