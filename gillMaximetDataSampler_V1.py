# -*- coding: utf-8 -*-
"""


This program allows you to sample data from a Gill Maximet Weather station
Here, the output is in default factory mode, but the program will work in any mode, just change the header accordingly.
The program generates a new text file in the same folder as this program every 1 min and writes the data.


Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in
all copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
THE SOFTWARE.
"""

import time
from datetime import datetime
from serial import *
import os
import subprocess

# set your parameters here!
ser = Serial()        
ser.port        = '/dev/ttyUSB0'                                                # choose serial port where device is plugged in
ser.baudrate    = 19200                                                         # default baud rate is 19200
ser.bytesize    = EIGHTBITS
ser.parity      = PARITY_NONE
ser.stopbits    = STOPBITS_ONE

fname = 'maximet.csv'                                
starttime = time.time()
fileInterval = 55
  

ser.open()                                                                      # open serial                                          


rawdata = ser.readline()
subdata = rawdata[1:36]

starttime = time.time()
filename = time.strftime(fname)
print ('new file created')
         
fid = open(filename,'wb')
fid.write(subdata)
fid.close()
    
fid = open(filename,'+a')
fid.write(',')
timeStamp = datetime.now().strftime('%d-%m-%Y %H:%M')
fid.write(timeStamp)
fid.close()
print (subdata)
print (timeStamp)
subprocess.run(["psql", "-f", "/home/cfns/systemtest/copy.sql", "postgres://postgres:stagecfns@localhost:5432/postgres"])
