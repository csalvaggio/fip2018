import argparse
import os
import RPi.GPIO
import subprocess
import sys

# Parse command line arguments
description = 'Live preview to allow focusing of Raspberry Pi cameras '
description += 'connected via multiplexer board'
parser = argparse.ArgumentParser(description=description)
helpMessage = 'camera multiplexer position A|B|C|D [default is A]'
parser.add_argument('-p', '--position',
                    type=str,
                    default='A',
                    help=helpMessage)
args = parser.parse_args()
position = args.position.upper()

# Check validity of multiplexer position specified
if position != 'A' and position != 'B' and position != 'C' and position != 'D':
   msg = 'Invalid multiplexer position specified: {0}'.format(position)
   print(msg)
   sys.exit(0)

# Initialize the GPIO state
RPi.GPIO.setwarnings(False)

RPi.GPIO.setmode(RPi.GPIO.BOARD)

RPi.GPIO.setup(7, RPi.GPIO.OUT)
RPi.GPIO.setup(11, RPi.GPIO.OUT)
RPi.GPIO.setup(12, RPi.GPIO.OUT)

RPi.GPIO.setup(15, RPi.GPIO.OUT)
RPi.GPIO.setup(16, RPi.GPIO.OUT)
RPi.GPIO.setup(21, RPi.GPIO.OUT)
RPi.GPIO.setup(22, RPi.GPIO.OUT)

RPi.GPIO.output(11, RPi.GPIO.HIGH)
RPi.GPIO.output(12, RPi.GPIO.HIGH)
RPi.GPIO.output(15, RPi.GPIO.HIGH)
RPi.GPIO.output(16, RPi.GPIO.HIGH)
RPi.GPIO.output(21, RPi.GPIO.HIGH)
RPi.GPIO.output(22, RPi.GPIO.HIGH)

# Select multiplexer position
if position == 'A':
   RPi.GPIO.output(7, RPi.GPIO.LOW)
   RPi.GPIO.output(11, RPi.GPIO.LOW)
   RPi.GPIO.output(12, RPi.GPIO.HIGH)
elif position == 'B':
   RPi.GPIO.output(7, RPi.GPIO.HIGH)
   RPi.GPIO.output(11, RPi.GPIO.LOW)
   RPi.GPIO.output(12, RPi.GPIO.HIGH)
elif position == 'C':
   RPi.GPIO.output(7, RPi.GPIO.LOW)
   RPi.GPIO.output(11, RPi.GPIO.HIGH)
   RPi.GPIO.output(12, RPi.GPIO.LOW)
elif position == 'D':
   RPi.GPIO.output(7, RPi.GPIO.HIGH)
   RPi.GPIO.output(11, RPi.GPIO.HIGH)
   RPi.GPIO.output(12, RPi.GPIO.LOW)

# Determine if camera is connected
cmd_stdout = subprocess.check_output(['vcgencmd', 'get_camera'])
detected = int(cmd_stdout.strip().decode('utf-8')[-1])
camera_present = True if detected == 1 else False

if camera_present:
   # Display user instructions
   msg = '*** Live preview for multiplexer position {0} ***'.format(position)
   print(msg)
   msg = '\n*** IMPORTANT NOTE ***'
   print(msg)
   msg = 'HDMI cable should be connected directly to the Pi that this script'
   print(msg)
   msg = 'is running on as the Pi camera\'s preview window is displayed as an'
   print(msg)
   msg = 'overlay on the GPU and will not display properly over an ssh tunnel'
   print(msg)

   # Display live preview
   cmd = 'raspistill '
   cmd += '--preview '
   cmd += '--verbose '
   cmd += '--keypress '
   cmd += '--fullscreen '
   cmd += '--exposure auto '
   cmd += '--timeout 0 '
   os.system(cmd)
else:
   msg = 'No camera present at multiplexer position {0}'.format(position)
   print(msg)

msg = 'Exiting ...'
print(msg)
sys.exit(0)

