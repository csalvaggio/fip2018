import RPi.GPIO as gpio
import os
import network


def capture(cam):
   print('Acquiring image from Camera {0} on {1}'.format(cam, ip))

   captureFilename = '/tmp/{0}_camera{1}'.format(ip, cam)
   cmd = 'raspistill '
   cmd += '-t 1 '
   cmd += '-o ' + captureFilename + '.jpg'
   os.system(cmd)


# Form an IP address string
ip = network.get_interface_ip_address('eth0')

# Initialize the GPIO state
gpio.setwarnings(False)

gpio.setmode(gpio.BOARD)

gpio.setup(7, gpio.OUT)
gpio.setup(11, gpio.OUT)
gpio.setup(12, gpio.OUT)

gpio.setup(15, gpio.OUT)
gpio.setup(16, gpio.OUT)
gpio.setup(21, gpio.OUT)
gpio.setup(22, gpio.OUT)

gpio.output(11, True)
gpio.output(12, True)
gpio.output(15, True)
gpio.output(16, True)
gpio.output(21, True)
gpio.output(22, True)

# Capture camera at multiplexer position 1
gpio.output(7, False)
gpio.output(11, False)
gpio.output(12, True)
capture(1)
    
# Capture camera at multiplexer position 2
gpio.output(7, True)
gpio.output(11, False)
gpio.output(12, True)
capture(2)

'''
# Capture camera at multiplexer position 3
gpio.output(7, False)
gpio.output(11, True)
gpio.output(12, False)
capture(3)

# Capture camera at multiplexer position 4
gpio.output(7, True)
gpio.output(11, True)
gpio.output(12, False)
capture(4)
'''
