#!/usr/bin/env python3
# Simple test of 4 button connected to pi w
# Yootop 2 Pcs 4-Key Matrix Membrane Switch,
# 1 x 4 Universal Array Keypad with 5 Pin 
# 2.54mm Pitch Female Connector
# https://smile.amazon.com/gp/product/B07F391653

import time

import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(16, GPIO.RISING,bouncetime=1)
GPIO.add_event_detect(20, GPIO.RISING,bouncetime=1)
GPIO.add_event_detect(21, GPIO.RISING,bouncetime=1)
GPIO.add_event_detect(19, GPIO.RISING,bouncetime=1)

def my_callback(a):
	print(str(a) + ' PUSHED!')

GPIO.add_event_callback(16, my_callback)
GPIO.add_event_callback(20, my_callback)
GPIO.add_event_callback(21, my_callback)
GPIO.add_event_callback(19, my_callback)

while True:
	#print GPIO.input(16), GPIO.input(20), GPIO.input(21), GPIO.input(19)
	time.sleep(0.25)
