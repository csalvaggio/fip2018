import gpio
import os
import sys
import time
import datetime


# Create a button object
buttonPin = 4
button = gpio.Button(buttonPin, edgeType='falling',
                                detectionOn=False, 
                                reverse=False)

# Create the full path to the trigger file
home = os.path.expanduser('~')
path = os.path.join(home, 'tmp')
triggerFile = os.path.join(path, 'trigger_cameras.lock')

if os.path.exists(triggerFile):
   os.remove(triggerFile)

# Set the delay time [s] to avoid multiple button events
delayTime = 0.5

print('Activated, press button to trigger cameras ...')
while True:
   button.wait()

   if os.path.exists(triggerFile):
      continue
   else:
      # Form a current date/time string (year, month, day, 
      #                                  hour, minute, second, millisecond)
      date = datetime.datetime.now().strftime('%Y_%m_%d_%H_%M_%S_%f')

      imagesPath = os.path.join(home, 'data')
      imagesPath = os.path.join(imagesPath, date)
      os.mkdir(imagesPath)

      f = open(triggerFile, 'w')
      f.write(imagesPath)
      f.close()

      print('... triggered')

   time.sleep(delayTime)
