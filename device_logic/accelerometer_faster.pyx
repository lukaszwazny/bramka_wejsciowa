import math

def get_angle(accelerometer, reference_values):
    cdef float the_angle_y, the_angle_x, the_angle_z =  0

    cdef float x, y, z = 0
    cdef float delta_x, delta_y, delta_z = 0
    cdef float delta_x2, delta_y2, delta_z2 = 0
    cdef float angle_x, angle_y, angle_z = 0

    for i in range(500):
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
        angle_x = delta_x/angle_x
        the_angle_x += math.degrees(math.atan(angle_x))

        angle_y = math.sqrt(delta_x2+delta_z2)
        angle_y = delta_y/angle_y
        the_angle_y += math.degrees(math.atan(angle_y))

        angle_z = math.sqrt(delta_x2+delta_y2)
        angle_z = delta_z/angle_z
        the_angle_z += math.degrees(math.atan(angle_z))

    the_angle_x = the_angle_x/500.0
    the_angle_y = the_angle_y/500.0
    the_angle_z = the_angle_z/500.0

    return (the_angle_x, the_angle_y, the_angle_z)