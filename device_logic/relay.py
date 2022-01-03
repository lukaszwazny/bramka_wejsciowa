import RPi.GPIO as GPIO
import config

def setup():
    GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(config.relay, GPIO.OUT, initial=GPIO.HIGH)

def open():
    GPIO.output(config.relay, GPIO.LOW)

def close():
    GPIO.output(config.relay, GPIO.HIGH)