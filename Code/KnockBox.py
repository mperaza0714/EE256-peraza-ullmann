# Code for KnockBox

import time
import board
import busio
import audioio
import digitalio
import storage
from random import randint
import adafruit_sdcard  # TODO add libraries
from analogio import AnalogIn
from adafruit_debouncer import Debouncer
import adafruit_esp32spi.adafruit_esp32spi_socket as socket
from adafruit_esp32spi import adafruit_esp32spi
import adafruit_requests as requests
from adafruit_io.adafruit_io import IO_HTTP, AdafruitIO_RequestError

## Set up the pins

# LED
led = digitalio.DigitalInOut(board.PB09)
led.direction = digitalio.Direction.OUTPUT

# Button
button = digitalio.DigitalInOut(board.D18)
button.direction = digitalio.Direction.INPUT
button.pull = digitalio.Push.UP
pushed = Debouncer(button)

# Force Sensor
force = AnalogIn(board.A5)
knockDetected = False
#TODO there probably needs to be a function that coninuously checks the analog data

# Microphone
#TODO

# Speaker
audio = audioio.AudioOut(board.D11)
# Preload example audio
wave_file = open("/sd/Audio/example.wav", "rb") # Note the "/sd/" prefix for the SD card
wave = audioio.WaveFile(wave_file)              # Everything else is the same ...

## Setup SPI Devices

# CD Card
# Use a digital pin to select the SD card
cs = digitalio.DigitalInOut(board.PA19)
# Wire up the SPI pins
spi = busio.SPI(board.SCK, board.MOSI, board.MISO)
# Connect to the card and mount the filesystem.
# Once this is done, the SD card looks just like another part of the files system!
sdcard = adafruit_sdcard.SDCard(spi, cs)
vfs = storage.VfsFat(sdcard)
storage.mount(vfs, "/sd")
# Speaker
audio = audioio.AudioOut(board.PA12)
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

# WIFI Setup
try:
    from secrets import secrets
except ImportError:
    print("WiFi secrets are kept in secrets.py, please add them there!")
    raise

# If you have an externally connected ESP32:
esp32_cs = DigitalInOut(board.D10)
esp32_ready = DigitalInOut(board.D4)
esp32_reset = DigitalInOut(board.D6)
esp = adafruit_esp32spi.ESP_SPIcontrol(spi, esp32_cs, esp32_ready, esp32_reset)

print("Connecting to AP...")
while not esp.is_connected:
    try:
        #TODO
        esp.connect_AP(secrets["ssid"], secrets["password"])
    except RuntimeError as e:
        print("could not connect to AP, retrying: ", e)
        continue
print("Connected to", str(esp.ssid, "utf-8"), "\tRSSI:", esp.rssi)

socket.set_interface(esp)
requests.set_socket(socket, esp)

#TODO
aio_username = secrets["aio_username"]
aio_key = secrets["aio_key"]

# Initialize an Adafruit IO HTTP API object
io = IO_HTTP(aio_username, aio_key, requests)

try:
    # Get the 'temperature' feed from Adafruit IO
    temperature_feed = io.get_feed("temperature")
except AdafruitIO_RequestError:
    # If no 'temperature' feed exists, create one
    temperature_feed = io.create_new_feed("temperature")

# Send random integer values to the feed
random_value = randint(0, 50)
print("Sending {0} to temperature feed...".format(random_value))
io.send_data(temperature_feed["key"], random_value)
print("Data sent!")

# Retrieve data value from the feed
print("Retrieving data from temperature feed...")
received_data = io.receive_data(temperature_feed["key"])
print("Data from temperature feed: ", received_data["value"])

## State Machine Setup

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


