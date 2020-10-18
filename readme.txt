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
   3D Printer

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
   Connect a servo to the first connection on pi hat.

Start a simple python webserver using the bottle framework.
   python targets.py
