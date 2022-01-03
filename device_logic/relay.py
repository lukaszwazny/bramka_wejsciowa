import enum
import RPi.GPIO as GPIO
import config

bcm_to_tegra = {
    k: list(GPIO.gpio_pin_data.get_data()[-1]['TEGRA_SOC'].keys())[i] for i, k in enumerate(GPIO.gpio_pin_data.get_data()[-1]['BCM'])
}

def setup():
    if GPIO.getmode() == None:
        GPIO.setmode(GPIO.BCM)
    GPIO.setwarnings(False)
    GPIO.setup(get_pin(config.relay), GPIO.OUT, initial=GPIO.HIGH)
    print('GPIO setup done!')

def open():
    GPIO.output(get_pin(config.relay), GPIO.LOW)

def close():
    GPIO.output(get_pin(config.relay), GPIO.HIGH)

def clean():
    GPIO.cleanup()

def get_pin(pin):
    return config.relay if GPIO.getmode() == GPIO.BCM else bcm_to_tegra.get(config.relay)