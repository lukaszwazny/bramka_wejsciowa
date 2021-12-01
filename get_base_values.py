import time
import board
import adafruit_adxl34x

i2c = board.I2C()
accelerometer = adafruit_adxl34x.ADXL345(i2c)

x = y = z = 0

for i in range(20):
    print("%f %f %f"%accelerometer.acceleration)
    x += accelerometer.acceleration[0]
    y += accelerometer.acceleration[1]
    z += accelerometer.acceleration[2]
    time.sleep(1)

x = x/20
y = y/20
z = z/20

print('x: ', x, 'y: ', y, 'z:', z)