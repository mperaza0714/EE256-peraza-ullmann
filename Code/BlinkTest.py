#Code to Test if LED Blinks
import time
import board
import digitalio

# LED
led = digitalio.DigitalInOut(board.PB09)
led.direction = digitalio.Direction.OUTPUT

while True:
    led.value = True
    time.sleep(0.5)
    led.value = False
    time.sleep(0.5)
