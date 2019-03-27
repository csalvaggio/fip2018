import os
import sys
import subprocess
import time


print('Initializing slave node ...')

# Create the full path to the trigger file
home = os.path.expanduser('~')

# Create a path to the lock file
locksPath = os.path.join(home, 'tmp')
triggerFile = os.path.join(locksPath, 'trigger_cameras.lock')

# Create a path to the shared image directory
imagesPath = os.path.join(home, 'data')

# Create the capture command
capture = os.path.join(home, 'src')
capture = os.path.join(capture, 'python')
capture = os.path.join(capture, 'misc')
capture = os.path.join(capture, 'capture.py')

# Set the delay time [s] for each loop iteration to prevent high rate cycling
delayTime = 0.1

print('... slave node initialized')

try:
   while True:
      # This listing must occur for the trigger file to be seen with no delay
      os.listdir(locksPath)

      time.sleep(delayTime)
      if os.path.exists(triggerFile):
         # Read the shared image directory filename from the trigger file
         f = open(triggerFile, 'r')
         imagesPath = f.read()
         f.close()

         print('Acquiring images ...')
         # Trigger each camera on the multiplexer
         args = ['python3', capture]
         subprocess.run(args)
         print('... images acquired\n')

         # If shared image directory exists, move images from local /tmp 
         # directory there
         if os.path.exists(imagesPath):
            print('Moving locally stored images to shared directory ...')
            cmd = 'mv /tmp/*.jpg ' + imagesPath
            os.system(cmd)
            print('... locally stored images have been moved\n')

         # If the trigger file exists, remove it
         if os.path.exists(triggerFile):
            print('Removing current trigger lock file ...')
            args = ['rm', '-f', triggerFile]
            subprocess.run(args)
            print('... current trigger lock file removed\n')

except KeyboardInterrupt:
   print('\nExiting ...')
   sys.exit()
