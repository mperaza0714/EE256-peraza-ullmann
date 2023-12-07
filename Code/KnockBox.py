# Code for KnockBox

import time
import board
import busio
import audioio
import digitalio
import storage
import adafruit_sdcard  # TODO add this library
from analogio import AnalogIn
from adafruit_debouncer import Debouncer

## Set up the pins

# LED
led = digitalio.DigitalInOut(board.D17)
led.direction = digitalio.Direction.OUTPUT

# Button
button = digitalio.DigitalInOut(board.D18)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Pull.UP
pushed = Debouncer(button)

# Force Sensor
force = AnalogIn(board.A5)
knockDetected = False
#TODO there probably needs to be a function that coninuously checks the analog data

# Microphone
#TODO

# CD Card
# Use a digital pin to select the SD card
cs = digitalio.DigitalInOut(board.D9)
# Wire up the SPI pins
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# Connect to the card and mount the filesystem.
# Once this is done, the SD card looks just like another part of the files system!
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")

# Speaker
audio = audioio.AudioOut(board.D11)
# Preload example audio
wave_file = open("/sd/Audio/example.wav", "rb") # Note the "/sd/" prefix for the SD card
wave = audioio.WaveFile(wave_file)              # Everything else is the same ...

# State Machine Setup
idleState = 0
recordState = 1
playState = 2
knockState = 3
# initial state
state = idleState


while True:

    # Wait for Button Press or Knock
    if state == idleState:
        #Check For Incoming Message TODO
        #if there is an incoming message
        # change states to playState

        # Check Button
        pushed.update()
        #TODO Check to make use logic is correct
        # if button pushed
        if pushed.fell:
            state = recordState

        # Check Knock
        if knockDetected:
            state = knockState

    elif state == recordState:
        #TODO How to check if button is not being held anymore
        #start rcording audio, still don't know how to do that
    elif state == playState:
        #TODO
        wave_file = open("thing we want to open", "rb")
        wave = audio.WaveFile(wave_file)
        audio.play(wave)
    else:
        state = idleState
        continue





    ## Sending a Message ##
    # Check for button press

    # While button is pressed start recording
    # Record audio and store in SD Card
    # Once button is released send audio to server

    ## Recieveing a Message ##
    # Wait to recieve message
    # Light up LED when messaage recieved
    # Click button to play message

    ## Send a Knock ##
    # knock detected
    # Send indicator to server

    ## Recieve a Knock ##
    # Wait to recieve knock
    # Once recieved move servo based on knock pattern


