#!/bin/bash
# A sample Bash script, by Ryan
export PYTHONPATH=$PYTHONPATH:/usr/lib/python3/dist-packages
sudo python3 ./gillMaximetDataSampler_V1.py
sudo python3 ./sshcon.py
