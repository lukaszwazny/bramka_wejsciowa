from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.provisioning.aio.async_provisioning_device_client import ProvisioningDeviceClient
import asyncio
import json
from azure.iot.device import Message
import board
import adafruit_adxl34x

i2c = board.I2C()
accelerometer = adafruit_adxl34x.ADXL345(i2c)

async def provision_device(provisioning_host, id_scope, registration_id, symmetric_key, model_id):
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
        provisioning_host=provisioning_host, 
        id_scope=id_scope, 
        registration_id=registration_id, 
        symmetric_key=symmetric_key
    )
    provisioning_device_client.provisioning_payload = {'modelId': model_id}
    return await provisioning_device_client.register()


async def main():
    provisioning_host = (
        "global.azure-devices-provisioning.net"
    )
    id_scope = '0ne00430809'
    registration_id = 'jern71nwjxqwymqxfpaxnz'
    symmetric_key = '6sg0ruimdnueE7rHsFhcZzuXmvGE4mNRmnB/uPFpiJg='
    model_id = 'dtmi:bramkawejsciowa:bramkaWejsciowa4s9;1'





    registration_result = await provision_device(
        provisioning_host=provisioning_host, 
        id_scope=id_scope, 
        registration_id=registration_id, 
        symmetric_key=symmetric_key,
        model_id=model_id)

    # if registration_result.status == "assigned":
    print("Device was assigned")
    # print(registration_result.registration_state.assigned_hub)
    # print(registration_result.registration_state.device_id)
    device_client = IoTHubDeviceClient.create_from_symmetric_key(
        symmetric_key='6sg0ruimdnueE7rHsFhcZzuXmvGE4mNRmnB/uPFpiJg=',
        hostname=registration_result.registration_state.assigned_hub,
        device_id=registration_result.registration_state.device_id,
        product_info=model_id,
    )
    # else:
    #     raise RuntimeError(
    #         "Could not provision device. Aborting Plug and Play device connection."
    #     )

    # Connect the client.
    await device_client.connect()
    print(device_client)

    x_acc_msg = {'x_acc': accelerometer.acceleration[0]}
    print(x_acc_msg)
    msg = Message(json.dumps(x_acc_msg))
    msg.content_encoding = 'utf-8'
    msg.content_type = 'application/json'
    await device_client.send_message(msg)

asyncio.run(main())