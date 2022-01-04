import { Injectable } from '@angular/core';
import {environment} from '../../environments/environment'
import {ProvisioningDeviceClient} from 'azure-iot-provisioning-device'
import { SymmetricKeySecurityClient } from 'azure-iot-security-symmetric-key';
import { Mqtt as ProvisioningTransport }  from 'azure-iot-provisioning-device-mqtt';
import { Mqtt as DeviceTransport} from 'azure-iot-device-mqtt';
import { Client, DeviceClientOptions } from 'azure-iot-device';

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
    let hubClient = Client.fromConnectionString(connectionString, DeviceTransport);
    await hubClient.setOptions({modelId: model_id, productInfo: model_id});

    let deviceClient = await hubClient.open()
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
