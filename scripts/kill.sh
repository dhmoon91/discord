#!/bin/bash
test -f /home/ubuntu/discord/save_pid.txt && kill -9 `cat /home/ubuntu/discord/save_pid.txt` || echo "File doesn't exists"
