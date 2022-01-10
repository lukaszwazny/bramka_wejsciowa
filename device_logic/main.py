from serial.serialutil import SerialException
from iot_central import connect_device, handle_command, send_close_event
from accelerometer import connect_accelerometer, get_reference_values
from helpers import wait_for_door_opened_and_closed
import api
import rdm6300_modified
import config
import relay
import threading

try:
    config.device_client = connect_device()
    config.device_client.on_method_request_received = handle_command
    accelerometer = connect_accelerometer()
    reference_values = get_reference_values(accelerometer)
    relay.setup()
    
    while True:
        try:
            if config.remote_open:
                relay.open()
                wait_for_door_opened_and_closed(accelerometer, reference_values)
                relay.close()
                config.remote_open = False
            value = ''
            in_card = out_card = None
            out_reader = rdm6300_modified.Reader(config.out_reader_port)
            out_card = out_reader.read(0.5)
            in_reader = rdm6300_modified.Reader(config.in_reader_port)
            in_card = in_reader.read(0.5)
        except SerialException as s_ex:
            print(s_ex)
        if in_card:
            value = str(in_card.value) 
            print('in ' + str(value))
            threading.Thread(target=api.Function8, args=[value]).start()
            config.got_not_open_request = config.got_open_request = False
            while not config.got_open_request and not config.got_not_open_request:
                if config.got_open_request:
                    relay.open()
                    wait_for_door_opened_and_closed(accelerometer, reference_values)
                    relay.close()
                    send_close_event()
            config.got_open_request = config.got_not_open_request = False
        elif out_card:
            value = str(out_card.value)
            print('out ' + str(value))
            relay.open()
            wait_for_door_opened_and_closed(accelerometer, reference_values)
            relay.close()
            resp = api.Function9(value)
            print(resp.text)
except Exception as ex:
    print(ex)
    relay.clean()
