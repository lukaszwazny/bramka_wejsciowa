import { Injectable } from '@angular/core';
import {environment} from '../../environments/environment'
import {ProvisioningDeviceClient} from 'azure-iot-provisioning-device'
import { SymmetricKeySecurityClient } from 'azure-iot-security-symmetric-key';
import { MqttWs as ProvisioningTransport }  from 'azure-iot-provisioning-device-mqtt';
import { MqttWs as DeviceTransport} from 'azure-iot-device-mqtt';
import { NoRetry } from 'azure-iot-common'
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
    let deviceClient = Client.fromConnectionString(connectionString, DeviceTransport);
    await deviceClient.setOptions({modelId: model_id, productInfo: model_id});

    return new Promise<Client>(resolve => {
      resolve(deviceClient);
    })

  }
}
