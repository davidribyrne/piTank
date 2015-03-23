#!/bin/sh
# Port 80 & access to GPIO require root
# Probably a more secure way to do this, but it's a toy, not a production server

mkdir log 2> /dev/null
touch log/access
touch log/error
sudo sh -c 'python bin/PiTank.py 2>&1 | tee --append log/server.log'
