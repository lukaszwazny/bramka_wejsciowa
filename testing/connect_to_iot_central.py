import time
from azure.iot.device.aio import IoTHubDeviceClient
from azure.iot.device.provisioning.aio.async_provisioning_device_client import ProvisioningDeviceClient
import asyncio
import json
from azure.iot.device import Message
from azure.iot.device import MethodResponse
import board
import adafruit_adxl34x

class Device:

    def __init__(self):
        self.i2c = board.I2C()
        self.accelerometer = adafruit_adxl34x.ADXL345(self.i2c)
        print('Accelerometer ready!')
        self.device_client = 0

    async def provision_device(self, provisioning_host, id_scope, registration_id, symmetric_key, model_id):
        provisioning_device_client = ProvisioningDeviceClient.create_from_symmetric_key(
            provisioning_host=provisioning_host, 
            id_scope=id_scope, 
            registration_id=registration_id, 
            symmetric_key=symmetric_key
        )
        provisioning_device_client.provisioning_payload = {'modelId': model_id}
        return await provisioning_device_client.register()

    def create_response_payload_with_status(self, command_request, method_name, create_user_response=None):
        """
        Helper method to create the payload for responding to a command request.
        This method is used for all method responses unless the user provides another
        method to construct responses to specific command requests.
        :param command_request: The command request for which the response is being sent.
        :param method_name: The method name for which we are responding to.
        :param create_user_response: Function to create user specific response.
        :return: The response payload.
        """
        if method_name:
            response_status = 200
        else:
            response_status = 404

        if not create_user_response:
            result = True if method_name else False
            data = "executed " + method_name if method_name else "unknown method"
            response_payload = {"result": result, "data": data}
        else:
            response_payload = create_user_response(command_request.payload)

        return (response_status, response_payload)

    async def handleCommand(self, command):
        print(command.name, command.payload, command.request_id)

        (response_status, response_payload) = self.create_response_payload_with_status(
            command_request=command, method_name=command.name
        )
        command_response = MethodResponse.create_from_method_request(
            method_request=command, status=response_status, payload=response_payload
        )
        try:
            await self.device_client.send_method_response(command_response)
        except Exception as e:
            print("responding to the {command} command failed".format(command=command.name))

    async def main(self):
        provisioning_host = (
            "global.azure-devices-provisioning.net"
        )
        id_scope = '0ne00430809'
        registration_id = 'ident'
        symmetric_key = '324tSOCfFNiSbu5V2FPDt9uhLfhNNb4UbcoV4OTlwSM='
        model_id = 'dtmi:modelDefinition:tzldmlsv:d1fwmhq00dg'

        # registration_id = 'jern71nwjxqwymqxfpaxnz'
        # symmetric_key = '6sg0ruimdnueE7rHsFhcZzuXmvGE4mNRmnB/uPFpiJg='
        # model_id = 'dtmi:bramkawejsciowa:bramkaWejsciowa4s9;1'


        registration_result = await self.provision_device(
            provisioning_host=provisioning_host,
            id_scope=id_scope,
            registration_id=registration_id,
            symmetric_key=symmetric_key,
            model_id=model_id
        )

        # if registration_result.status == "assigned":
        print("Device was assigned")

        self.device_client = IoTHubDeviceClient.create_from_symmetric_key(
            symmetric_key=symmetric_key,
            hostname=registration_result.registration_state.assigned_hub,
            device_id=registration_result.registration_state.device_id,
            product_info=model_id,
        )
        # else:
        #     raise RuntimeError(
        #         "Could not provision device. Aborting Plug and Play device connection."
        #     )

        # Connect the client.
        await self.device_client.connect()
        print(self.device_client)

        #command listener
        self.device_client.on_method_request_received = self.handleCommand

        #send telemetry
        while True:
            acc_msg = {'x_acc': self.accelerometer.acceleration[0], 'y_acc': self.accelerometer.acceleration[1], 'z_acc': self.accelerometer.acceleration[2]}
            print(acc_msg)
            msg = Message(json.dumps(acc_msg))
            msg.content_encoding = 'utf-8'
            msg.content_type = 'application/json'
            await self.device_client.send_message(msg)
            time.sleep(0.5)

    

asyncio.run(Device().main())