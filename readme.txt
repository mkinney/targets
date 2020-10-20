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
   Download Raspios lite and unzip
   Prepare the micro sd card:

      # insert new card into mac

      # see what drive it is (something like 1, 2, or 3)
      diskutil list

# This is what part of the output looks like: (Note: I'm using a larger drive for reasons. It does not need to be this big. So, on my computer the drive is /dev/disk2.)

      /dev/disk2 (external, physical):
   #:                       TYPE NAME                    SIZE       IDENTIFIER
   0:     FDisk_partition_scheme                        *128.0 GB   disk2
   1:             Windows_FAT_32 VOLUME1                 128.0 GB   disk2s1

       # unmount disk
       diskutil unmountDisk /dev/disk2

       # copy image to disk (Note: This will wipe the contents. Be extra careful as to which disk you are using. If unsure, do not proceed.)
       sudo dd bs=1m if=2020-08-20-raspios-buster-armhf-lite.img of=/dev/disk2

       # This will probably prompt for your password since we're using "sudo".
       # Here was the output for my prep:

Password:
1760+0 records in
1760+0 records out
1845493760 bytes transferred in 427.476069 secs (4317186 bytes/sec)

       # When this step is done, it should auto-mount the drive and you can
       # write the files on next steps to it. (The mounted drive was called
       # "boot".

   Add "ssh" file to config directory to have ssh service started upon pi boot.
      touch ssh
   Create wpa_supplicant.conf file. My file looks like this: (Note: The XXX and YYY are not my ssid/psk values.)

ctrl_interface=DIR=/var/run/wpa_supplicant
update_config=1
country=US
network={
  ssid="xxx"
  psk="yyy"
  scan_ssid=1
  key_mgmt=WPA-PSK
}

   Added these lines to end of config.txt:
#Enable UART
enable_uart=1

   Change out of that directory so we can unmount the drive.
   Unmount the drive.
      diskutil unmountDisk /dev/disk2

   Insert the card into the pi.
   Connect power to pi (which will boot the pi).
   Wait a couple of minutes.
   Ensure networking is working. (We want networking to update/install software on the pi.)

   Connect to pi via ssh (user "pi" and default password is "raspberry") then did these steps: (ex: "ssh pi@raspberrypi.local")


      sudo apt-get update
      # If you get this error "Error writing to output file - write (28: No space left on device)", then you need to go run "sudo raspi-config" and go into Advanced Options, A1 Expand filesystem. After done, it will reboot the pi. Then re-try the "update".
      sudo apt-get upgrade
      # change password by running: "passwd"
      passwd
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
