About:
I wanted create moving targets for target shooting. My goal is to use off the shelf parts and make it easy for anyone to be able to do this on their own.

Hardware:
   Raspberry Pi W with headers https://smile.amazon.com/gp/product/B07B8MMD3V
   Servo Hat for Pi https://smile.amazon.com/gp/product/B07Z1JS855
   16GB memory card https://smile.amazon.com/gp/product/B073K14CVB
   MG996R Servos https://smile.amazon.com/gp/product/B07MFK266B/
   Servo extension cables https://smile.amazon.com/gp/product/B07HJ4LDDP
   Power supply for Pi https://www.adafruit.com/product/1995
   Power supply for Hat https://www.adafruit.com/product/276 (I cut off end and wired to power)
   4 button (optional) https://smile.amazon.com/gp/product/B07F391653
   wires for buttons (optional) https://smile.amazon.com/gp/product/B07GD2BWPY
   3D Printer

Here is a picture of the initial hardware setup: https://github.com/mkinney/targets/blob/master/pi_with_hat_and_servo.png or with optional buttons https://github.com/mkinney/targets/blob/master/pi_with_hat_servo_and_buttons.png

I really like this work https://www.thingiverse.com/thing:3319383
I plan to use this as inspiration for the direction of this project even though I had created some prototypes using some boards, rulers, and screws.

Note: The guide at https://learn.adafruit.com/raspberry-pi-zero-creation/text-file-editing was most helpful getting started. If there are any questions about getting up and running, please visit that page.

Steps:
   Added "ssh" file to config directory
   Created wpa_supplicant.conf
   Added these lines to end of config.txt:
      #Enable UART
      enable_uart=1
   Booted Pi.
   Got networking working.
   I ssh'd to pi (user "pi" and default password is "raspberry") then did these steps:
      sudo apt-get update
      sudo apt-get upgrade
      # change password by running: "passwd"
      sudo apt-get install -y python3 git python3-pip
      sudo update-alternatives --install /usr/bin/python python $(which python2) 1
      sudo update-alternatives --install /usr/bin/python python $(which python3) 2
      sudo update-alternatives --config python
      sudo pip3 install adafruit-circuitpython-servokit
      pip3 install RPI.GPIO
      pip3 install adafruit-blinka
      pip3 install smbus
      pip3 install bottle
      # edited /etc/modules to ensure these lines were present:
          i2c-dev
          i2c-bcm2708
      sudo raspi-config
         # 2 Networking, changed hostname to "targets.local"
         # 5 Interfacing Options, P4 SPI -> yes
         # 5 Interfacing Options, I2C -> yes
   Reboot.
   Clone this repo and change into the targets directory.
       git clone https://github.com/mkinney/targets.git 
   Connect a servo to the first connection on pi hat.

Start a simple python webserver using the bottle framework.
   cd targets
   python targets.py

Note: Press control-c to quit after you are done running targets.py.

This will create a simple webserver and will turn the servo on the first port when you click "submit" on the web page.

This is what the output looks like:

    pi@targets:~/targets $ python targets.py
    reset_targets
    reset_targets
    Bottle v0.12.18 server starting up (using WSGIRefServer())...
    Listening on http://targets.local:8080/
    Hit Ctrl-C to quit.

    192.168.0.165 - - [18/Oct/2020 05:54:59] "GET / HTTP/1.1" 200 170
    all_targets
    0 110 1.0 0
    Sleeping for  1
    reset_targets

If you just want to start/stop from 4 buttons, add pins using https://github.com/mkinney/targets/blob/master/pi_w_pins.png (see buttons.py for small test script).
Assuming stop is wired to GPIO 21 and start is wired to GPIO 16. (Don't forget to connect ground, too.)
