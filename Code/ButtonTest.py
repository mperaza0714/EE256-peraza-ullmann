import time
import board

import digitalio
from adafruit_debouncer import Debouncer



# Set up the on-off toggle
Toggle = False # off

#set up the digital pin we are using
pin = digitalio.DigitalInOut(board.PA04)
pin.direction = digitalio.Direction.INPUT
pin.pull = digitalio.Pull.DOWN
switch = Debouncer(pin)

#check when button rises and falls at given time speed
while True:
    switch.update()
    if switch.rose:
        print("Pushed")
    elif switch.fell:
        print("Unpushed")
    else:
        print("NAN")

    time.sleep(0.1)