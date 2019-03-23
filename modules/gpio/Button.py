import RPi.GPIO as GPIO
import sys

class Button(object):

   def __init__(self, pin, edgeType='rising',
                           detectionOn=False,
                           reverse=False):
      self._pin = pin
      self._edgeType = GPIO.RISING if edgeType == 'rising' else GPIO.FALLING
      self._detectionOn = detectionOn
      self._reverse = reverse

      try:
         GPIO.setmode(GPIO.BCM)
         if self._edgeType == GPIO.RISING:
            GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)
         else:
            GPIO.setup(self._pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)
      except RuntimeError:
         msg  = 'In order to use GPIO you must run with "root" privileges,\n'
         msg += '              try running your script using "sudo"'
         raise RuntimeError(msg)

      if self._detectionOn:
         GPIO.remove_event_detect(self._pin)
         GPIO.add_event_detect(self._pin, self._edgeType)

   @property
   def pin(self):
      return self._pin

   @property
   def edgeType(self):
      return 'rising' if self._edgeType == GPIO.RISING else 'falling'

   @edgeType.setter
   def edgeType(self, edgeType):
      if edgeType == 'rising' or edgeType == 'falling':
         self._edgeType = GPIO.RISING if edgeType == 'rising' else GPIO.FALLING
         if self._detectionOn:
            GPIO.remove_event_detect(self._pin)
            GPIO.add_event_detect(self._pin, self._edgeType)
      else:
         msg  = 'Edge type must be "rising" or "falling"'
         raise ValueError(msg)

   @property
   def detectionOn(self):
      return self._detectionOn

   @detectionOn.setter
   def detectionOn(self, detectionOn):
      self._detectionOn = detectionOn
      if self._detectionOn:
         GPIO.remove_event_detect(self._pin)
         GPIO.add_event_detect(self._pin, self._edgeType)
      else:
         GPIO.remove_event_detect(self._pin)

   @property
   def reverse(self):
      return self._reverse

   @reverse.setter
   def reverse(self, reverse):
      self._reverse = reverse

   def pressed(self):
      if self._detectionOn:
         return GPIO.event_detected(self._pin)
      else:
         if self._reverse:
            return not GPIO.input(self._pin)
         else:
            return GPIO.input(self._pin)

   def wait(self):
      try:
         if self._edgeType == GPIO.RISING:
            GPIO.wait_for_edge(self._pin, GPIO.RISING)
         elif self._edgeType == GPIO.FALLING:
            GPIO.wait_for_edge(self._pin, GPIO.FALLING)
         else:
            GPIO.wait_for_edge(self._pin, GPIO.BOTH)
      except KeyboardInterrupt:
         print('\nExiting ...')
         sys.exit()


if __name__ == '__main__':

   buttonPin = 4
   button = Button(buttonPin, edgeType='rising',
                                   detectionOn=False,
                                   reverse=False)

   print('Pin: {0}'.format(button.pin))
   print('Edge type: {0}'.format(button.edgeType))
   print('Detection on: {0}'.format(button.detectionOn))
   print('Reverse: {0}'.format(button.reverse))
   print('')
   print('Press button to continue ...')
   button.wait()
   print('PRESSED')

