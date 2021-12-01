import time
import board
import adafruit_adxl34x
import math

i2c = board.I2C()
accelerometer = adafruit_adxl34x.ADXL345(i2c)

x_base = -0.16475172
y_base = 0.31577413
z_base = 10.016512309999998

while True:

    angle_y = angle_x = 0
    for i in range(20):
        x = accelerometer.acceleration[0] - x_base
        y = accelerometer.acceleration[1] - y_base
        z = accelerometer.acceleration[2] - z_base

        x2 = x*x
        y2 = y*y
        z2 = z*z

        result = math.sqrt(y2+z2)
        result = x/result
        angle_x += math.degrees(math.atan(result))

        result = math.sqrt(x2+z2)
        result = y/result
        angle_y += math.degrees(math.atan(result))
    angle_x = angle_x/20
    angle_y = angle_y/20

    print('x: ', angle_x, 'y: ', angle_y)

    time.sleep(1)