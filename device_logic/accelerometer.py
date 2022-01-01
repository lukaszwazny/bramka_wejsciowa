import time
import board
import adafruit_adxl34x

def connect_accelerometer():
    try:
        i2c = board.I2C()
        accelerometer = adafruit_adxl34x.ADXL345(i2c)
    except:
        try:
            i2c = board.I2C()
            accelerometer = adafruit_adxl34x.ADXL345(i2c)
        except:
            raise Exception("Couldn't connect to accelerometer!")
    print("Connected with accelerometer")
    return accelerometer

def get_reference_values(accelerometer):
    x = y = z = 0

    for i in range(30):
        x += accelerometer.acceleration[0]
        y += accelerometer.acceleration[1]
        z += accelerometer.acceleration[2]
        time.sleep(0.2)

    x = x/30
    y = y/30
    z = z/30

    return (x, y, z)
