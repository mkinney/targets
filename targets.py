#!/usr/bin/env python3

import time
import random
from bottle import route, run, post, request, template

# using pi w with header and a servo driver hat
# show shooting targets
# Note: requires power to both hat and pi

from adafruit_servokit import ServoKit

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
