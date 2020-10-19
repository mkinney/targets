#!/usr/bin/env python3

# using pi w with header and a servo driver hat
# show shooting targets
# Note: requires power to both hat and pi

import time
import random
from bottle import route, run, post, request, template

from adafruit_servokit import ServoKit

import RPi.GPIO as GPIO

# setup buttons (optional)
GPIO.setmode(GPIO.BCM)
GPIO.setup(16, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(20, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(21, GPIO.IN, pull_up_down=GPIO.PUD_UP)
GPIO.setup(19, GPIO.IN, pull_up_down=GPIO.PUD_UP)

GPIO.add_event_detect(16, GPIO.RISING,bouncetime=1)
GPIO.add_event_detect(20, GPIO.RISING,bouncetime=1)
GPIO.add_event_detect(21, GPIO.RISING,bouncetime=1)
GPIO.add_event_detect(19, GPIO.RISING,bouncetime=1)

# Set channels to the number of servo channels on your kit.
# 8 for FeatherWing, 16 for Shield/HAT/Bonnet.
kit = ServoKit(channels=16)

def target(num, angle=110, show_time=1.0, reset_angle=0):
    print(num, angle, show_time, reset_angle)
    # angle must be between 0-180 inclusive
    kit.servo[num].angle = angle
    # give time to move servo
    time.sleep(0.1)

    if show_time > 0:
        time.sleep(show_time)
        kit.servo[num].angle = reset_angle

def all_targets(randomize=False):
    print('all_targets')
    # ensure you list the servos that are connected
    servos = [0]
    random_seconds = 0.3
    if randomize:
        random.shuffle(servos)
        # wait between 1 and 2 seconds
        random_seconds = random.randint(1, 2)
    for servo in servos:
        target(servo)
        print("Sleeping for ", random_seconds)
        time.sleep(random_seconds)
    reset_targets()

def reset_targets():
    print('reset_targets')
    for i in range(16):
        kit.servo[i].angle = 0

reset_targets()

def my_callback(a):
    print(str(a) + ' PUSHED!')

def stop_button(a):
    reset_targets()

def play_button(a):
    all_targets()


GPIO.add_event_callback(16, all_targets)
GPIO.add_event_callback(20, my_callback)
GPIO.add_event_callback(21, stop_button)
GPIO.add_event_callback(19, my_callback)


index_html = '''
<html lang="en">

<head>
    <title>Targets</title>
</head>

<body>

    <form method="post">
        <button type="submit">Submit</button>
    </form>

</body>

</html>'''

@route('/')
def index():
    return template(index_html)

@post('/')
def process():
    all_targets(True)
    return template(index_html)

run(host='targets.local', reloader=True, port=8080, debug=True)
