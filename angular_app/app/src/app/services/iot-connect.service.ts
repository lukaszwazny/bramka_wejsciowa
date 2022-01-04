import { Injectable } from '@angular/core';
import {environment} from '../../environments/environment'
import {ProvisioningDeviceClient} from 'azure-iot-provisioning-device'
import { SymmetricKeySecurityClient } from 'azure-iot-security-symmetric-key';
import { MqttWs as ProvisioningTransport }  from 'azure-iot-provisioning-device-mqtt';
import { MqttWs as DeviceTransport} from 'azure-iot-device-mqtt';
import { Client, DeviceClientOptions, Message } from 'azure-iot-device';

@Injectable({
  providedIn: 'root'
})
export class IotConnectService {

  constructor() { }

  async connectDevice() {
    const provisioning_host = "global.azure-devices-provisioning.net"
    const id_scope = environment.ID_SCOPE
    const registration_id = environment.REGISTRATION_ID
    const symmetric_key = environment.SYMMETRIC_KEY
    const model_id = environment.MODEL_ID
    
    const provisioningSecurityClient = new SymmetricKeySecurityClient(registration_id, symmetric_key)

    const provisioningClient = ProvisioningDeviceClient.create(
      provisioning_host, id_scope, new ProvisioningTransport(), provisioningSecurityClient)
    provisioningClient.setProvisioningPayload({'modelId': model_id})

    const registeredDevice = await provisioningClient.register()

    if (registeredDevice?.status != 'assigned'){
      console.log('Device not assigned!');
      return new Promise(resolve => {
              resolve(registeredDevice);
          })
    } 

    console.log('Device assigned!');
    let connectionString = 'HostName=' + registeredDevice?.assignedHub 
          + ';DeviceId=' + registeredDevice?.deviceId 
          + ';SharedAccessKey=' + symmetric_key;
    //let deviceClient = Client.fromConnectionString(connectionString, DeviceTransport);
    let deviceClient = Client.fromConnectionString('HostName=iotc-0ef9c35c-5689-4fc8-8b9a-c859316e0ce2.azure-devices.net;DeviceId=ident;SharedAccessKey=324tSOCfFNiSbu5V2FPDt9uhLfhNNb4UbcoV4OTlwSM=', DeviceTransport);
    //await deviceClient.setOptions({modelId: model_id, productInfo: model_id});
    await deviceClient.setOptions({modelId: 'dtmi:modelDefinition:tzldmlsv:d1fwmhq00dg'});

    let connectionStatus;
    // try {
      connectionStatus = await deviceClient.open()
    // }
    // catch (error)
    // {
    //   connectionStatus = error
    // }
    const msg = new Message(
      JSON.stringify(
        {siemanko: "siemanko"}
      )
    );
    msg.contentType = 'application/json';
    msg.contentEncoding = 'utf-8';
    await deviceClient.sendEvent(msg);
    
        //   if (err) {
        //     console.log('Device not connected!');
        //     return err;
        //   } else {
        //     console.log('Device connected!');
        //     return hubClient;
        //   }
        // });
    console.log('siema')
    // if registration_result.status == "assigned":
    //     print("Device was assigned")
    // else:
    //     raise Exception("Couldn't assign the device!")

    // device_client = IoTHubDeviceClient.create_from_symmetric_key(
    //         symmetric_key=symmetric_key,
    //         hostname=registration_result.registration_state.assigned_hub,
    //         device_id=registration_result.registration_state.device_id,
    //         product_info=model_id,
    //     )
    // asyncio.run(device_client.connect())
    // if device_client.connected:
    //     print("Device was connected")
    //     return device_client
    // else:
    //     raise Exception("Couldn't connect device!")
    // }

  }
}
