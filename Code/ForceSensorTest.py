import time
import board
from analogio import AnalogIn

# set up the A5 pin for analog input
analog_in = AnalogIn(board.PA06)

# read the pin every 200 ms, and print/plot the result
while True:
    print(( analog_in.value / 655.360,))    # convert to 0.0-100.0 floating point
    time.sleep(0.05)\