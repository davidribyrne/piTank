#!/bin/sh
# Port 80 & access to GPIO require root
# Probably a more secure way to do this, but it's a toy, not a production server

mkdir log
sudo python bin/PiTank.py &> log/server.log