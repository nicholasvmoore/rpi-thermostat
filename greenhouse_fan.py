#!/usr/bin/python3
import subprocess
import RPi.GPIO as GPIO
from time import sleep
#from subprocess import Popen, PIPE

# This script is meant for Python 3.2 on a RPi,
# it will grap the ambient temperature and control
# a fan based on the data collected.

# Global variables
timeframe = 5
interval = 60
past_temp = [0] * timeframe
threshold = 80
fan = "off"
relay = 16
#sensor = "/home/nicholas/temp"
#sensor = "/sys/bus/w1/devices/28-000005b37335/"
sensor = "/sys/bus/w1/devices/28-000005b34e5b/"
GPIO.setwarnings(False) 
GPIO.setmode(GPIO.BOARD)
GPIO.setup(relay, GPIO.OUT)

def get_ambient_temp_raw():
    # Grab the temp from the GPIO
    try:
        tempFile = open(sensor + "w1_slave" )
        ambient_temp_raw = tempFile.readlines()
        tempFile.close()
        return ambient_temp_raw
    except:
        print("The sensor is not readable")
        return

def get_ambient_temp():
    # Read the output of the ambient_temp_raw() and strip all but the temp
    ambient_temp_raw = get_ambient_temp_raw()
    ambient_temp_raw = ambient_temp_raw[1].split(" ")[9] # This splits the row into colums and chooses the temp
    ambient_temp_raw = ambient_temp_raw.split("=")[1] # This splits out the 't=' from the output
    return float(ambient_temp_raw) / 1000 * 1.8 + 32

def monitor_temp():
    global fan
    count = timeframe
    for i in range(0, 5):
        if i != timeframe - 1:
            past_temp[count - 1] = past_temp[count - 2]
            count -= 1
        else:
            past_temp[0] = get_ambient_temp()

    print(sum(past_temp)/len(past_temp), past_temp)

    # Initialization temp check
    #if fan == "off" and past_temp[timeframe -1] <= 0:
    #    if past_temp[0] >= threshold:
    #        fan = "on"
    #        fan_control(fan)
    #        return

    #if fan == "on" and past_temp[timeframe -1] <= 0:
    #    print("leaving fan on from initialization")
    #    return

    # If the fan is on and the temp has dropped below the threshold, turn the fan off
    #if fan == "on" and sum(past_temp)/len(past_temp) <= threshold:
    if sum(past_temp)/len(past_temp) <= threshold:
        #if past_temp[timeframe -1] <= 0:
        #    return
        #elif sum(past_temp)/len(past_temp) <= threshold:
        #    fan = "off"
        #    fan_control(fan)
        #    return
        if sum(past_temp)/len(past_temp) <= threshold:
            fan = "off"
            fan_control(fan)
            return

    # If fan is already on and the temp is above the threshold, leave the fan on
    #if fan == "on" and sum(past_temp)/len(past_temp) >= threshold:
	#return

    # If the average temp is above the threshold, turn the fan on
    if sum(past_temp)/len(past_temp) >= threshold:
        fan = "on"
        fan_control(fan)
        return

def fan_control(function):
    if function == "on":
        print("Turning fan", function)
        GPIO.output(relay, GPIO.LOW)
    if function == "off":
        print("Turning fan", function)
        GPIO.output(relay, GPIO.HIGH)

while True:
    try:
        monitor_temp()
        sleep(interval)
    except:
        pass
