import board
import adafruit_adxl34x
import math
import config


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
    x = y = z = 0.0

    for i in range(500):
        x += accelerometer.acceleration[0]
        y += accelerometer.acceleration[1]
        z += accelerometer.acceleration[2]

    x = x/500.0
    y = y/500.0
    z = z/500.0

    return (x, y, z)

def get_angle(accelerometer, reference_values):
    the_angle_y = the_angle_x = the_angle_z =  0

    x = y = z = 0
    for i in range(50):
        x = accelerometer.acceleration[0]
        y = accelerometer.acceleration[1]
        z = accelerometer.acceleration[2]

        delta_x = x - reference_values[0]
        delta_y = y - reference_values[1]
        delta_z = z - reference_values[2]

        delta_x2 = delta_x*delta_x
        delta_y2 = delta_y*delta_y
        delta_z2 = delta_z*delta_z

        angle_x = math.sqrt(delta_y2+delta_z2)
        if math.fabs(angle_x) < 0.18:
            the_angle_x += 0
        else:
            angle_x = delta_x/angle_x
            the_angle_x += math.degrees(math.atan(angle_x))

        angle_y = math.sqrt(delta_x2+delta_z2)
        if math.fabs(angle_y) < 0.18:
            the_angle_y += 0
        else:
            angle_y = delta_y/angle_y
            the_angle_y += math.degrees(math.atan(angle_y))

        angle_z = math.sqrt(delta_x2+delta_y2)
        if math.fabs(angle_z) < 0.18:
            the_angle_z += 0
        else:
            angle_z = delta_z/angle_z
            the_angle_z += math.degrees(math.atan(angle_z))

    the_angle_x = the_angle_x/50.0
    the_angle_y = the_angle_y/50.0
    the_angle_z = the_angle_z/50.0

    

    return (the_angle_x, the_angle_y, the_angle_z)

def testing():
    accelerometer = connect_accelerometer()
    ref_val = get_reference_values(accelerometer)

    is_closed=True
    was_closed=True
    while True:
        was_closed = is_closed
        angle = math.pow(get_angle(accelerometer, ref_val)[0], 3)
        if  angle > math.pow(config.opening_angle, 3):
            is_closed=True
        if angle < math.pow(config.closing_angle, 3):
            is_closed=False
        if was_closed and not is_closed:
            print('opened')
        if not was_closed and is_closed:
            print('closed')