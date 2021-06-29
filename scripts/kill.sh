#!/bin/bash
cd /home/ubuntu/discord
kill -9 `cat save_pid.txt`
rm save_pid.txt