from iot_central import connect_device
from accelerometer import connect_accelerometer, get_reference_values

try:
    device_client = connect_device()
    accelerometer = connect_accelerometer()
    reference_values = get_reference_values(accelerometer)
    print('siema')
except Exception as ex:
    print(ex)
