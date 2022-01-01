import os
from azure.iot.device.iothub.aio.async_clients import IoTHubDeviceClient
from azure.iot.device.provisioning.aio.async_provisioning_device_client import ProvisioningDeviceClient
import asyncio

def connect_device():
    provisioning_host = (
        "global.azure-devices-provisioning.net"
    )
    id_scope = os.environ.get('ID_SCOPE')
    registration_id = os.environ.get('REGISTRATION_ID')
    symmetric_key = os.environ.get('SYMMETRIC_KEY')
    model_id = os.environ.get('MODEL_ID')
    
    provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
            provisioning_host=provisioning_host, 
            id_scope=id_scope, 
            registration_id=registration_id, 
            symmetric_key=symmetric_key
        )
    provisioning_device_client.provisioning_payload = {'modelId': model_id}

    registration_result = asyncio.run(provisioning_device_client.register())
    if registration_result.status == "assigned":
        print("Device was assigned")
    else:
        raise Exception("Couldn't assign the device!")

    device_client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key=symmetric_key,
            hostname=registration_result.registration_state.assigned_hub,
            device_id=registration_result.registration_state.device_id,
            product_info=model_id,
        )
    asyncio.run(device_client.connect())
    if device_client.connected:
        print("Device was connected")
        return device_client
    else:
        raise Exception("Couldn't connect device!")