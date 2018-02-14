#!/usr/bin/python

import RPi.GPIO as gpio
import time as time
import os 
import glob 


#############################################

##setup
gpio.setmode(gpio.BCM)
gpio.setwarnings(False)
gpio.setup(21,gpio.IN, pull_up_down=gpio.PUD_UP)
gpio.setup(26,gpio.OUT, initial=1)
os.system('modprobe w1-gpio') 
os.system('modprobe w1-therm') 

##set dir
base_dir = '/sys/bus/w1/devices/'
##set device
device_folder = glob.glob(base_dir + '28*')[0] 
device_file = device_folder + '/w1_slave' 
 
 
def raw(): 
    op = open(device_file, 'r') 
    tempLine = op.readlines() 
    op.close() 
    return tempLine 
  
def tempOut(): 
    tempLine = raw() 
    while tempLine[0].strip()[-3:] != 'YES': 
        time.sleep(0.2) 
        tempLine = read_temp_raw() 
    equals_pos = tempLine[1].find('t=') 
    if equals_pos != -1: 
        temp_string = tempLine[1][equals_pos+2:] 
        temp_c = float(temp_string) / 1000.0 
        print(temp_c, 'celsius')
    
    

#########################################################

while True:
    i = gpio.input(21)
    
    if i==True:        
        ##print("off")        
        gpio.output(26,False)
        time.sleep(0.0001)
    
    elif i==False:
        ##print("on")
        tempOut()
        gpio.output(26,True)
        time.sleep(1)