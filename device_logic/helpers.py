import math
from accelerometer import get_angle
import config


def wait_for_door_opened_and_closed(accel, ref_val):
    can_be_closed = False
    was_opened = False
    while not can_be_closed:
        angle = math.pow(get_angle(accel, ref_val)[0], 3)
        if angle < math.pow(config.opening_angle, 3):
            was_opened = True
        if angle > math.pow(config.closing_angle, 3) and was_opened:
            can_be_closed = True