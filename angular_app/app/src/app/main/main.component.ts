import { Component, OnInit, ViewChild } from '@angular/core';
import { MatStepper } from '@angular/material/stepper/stepper';
import { Client, DeviceMethodResponse } from 'azure-iot-device';
import { AnimationOptions } from 'ngx-lottie';
import { IotConnectService } from '../services/iot-connect.service';
import { sleep } from '../services/utils';
import { Message } from 'azure-iot-common';
import { MqttWs } from 'azure-iot-device-mqtt';
import { SharedAccessKeyAuthenticationProvider } from 'azure-iot-device';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-main',
  templateUrl: './main.component.html',
  styleUrls: ['./main.component.scss']
})
export class MainComponent implements OnInit {

  @ViewChild('stepper') stepper!: MatStepper;

  card: AnimationOptions = {
    path: 'assets/card.json'
  }

  lack: AnimationOptions = {
    path: 'assets/lack.json'
  }

  sorry: AnimationOptions = {
    path: 'assets/sorry.json'
  }

  run: AnimationOptions = {
    path: 'assets/run.json'
  }

  lessons:Array<{id:number, name:string}>

  identificator_nr:string
  roles:Array<string>
  role:string
  package:{package_id?:number, package_name:string}

  cause ?: String

  deviceClient:any
  gotComand:boolean
  private response:DeviceMethodResponse

  constructor(private iotConnectService: IotConnectService,
    private api:ApiService) {
    this.gotComand = false; 
    this.roles = [];
    this.lessons = []
    this.identificator_nr = ""
    this.role = ""
    this.package = {package_id: undefined, package_name: ""}
    this.response = new DeviceMethodResponse("null", new MqttWs(new SharedAccessKeyAuthenticationProvider({host: "null", deviceId: "null"})))
  }

  async commandHandler(request:any, response:any) {
    if (!this.gotComand){
      this.response = response
      this.gotComand = true
      switch (request.methodName) {
      case 'gotUser': {
        await this.sendCommandResponse(request, response, 200, 'ok');
        if (request.payload?.identificator_nr){
          this.identificator_nr = request.payload?.identificator_nr
          this.roles = request.payload?.roles
          if (this.roles.length == 1){
            this.role = this.roles[0]
            this.handleIdAndRole()
          } else {
            this.stepper.selectedIndex = 2
            this.refresh()
          }
        } else {
          this.stepper.selectedIndex = 1;
          this.refresh()
          this.backToFirstScreen()
        }
        
        break;
      }
      case 'gotEntrance': {
        await this.sendCommandResponse(request, response, 200, 'ok')
        if (request.payload?.role_name == "MaRiAn"){
          this.backToFirstScreen()
          break;
        }
        this.identificator_nr = request.payload?.identificator_nr
        this.role = request.payload?.role_name
        this.handleEntrance(request.payload?.lesson_type_id, request.payload?.justification, {id: undefined, name: request.payload?.package})
        break;
      }
      default:
        await this.sendCommandResponse(request, response, 404, 'unknown method');
        this.gotComand = false
        break;
      }
    } else {
      await this.sendCommandResponse(request, response, 404, 'application now busy');
    }
    
  }

  async sendCommandResponse(request:any, response:any, status:any, payload:any){
    try {
      await response.send(status, payload);
      console.log('Response to method \'' + request.methodName +
                '\' sent successfully.' );
    } catch (err:any) {
      console.error('An error ocurred when sending a method response:\n' +
                err.toString());
    }
  }

  ngOnInit(): void {
    this.iotConnectService.connectDevice().then(_deviceClient => {
      console.log(_deviceClient)
      this.deviceClient = _deviceClient
      this.deviceClient.open((err: any) => {
        if (err) {
          console.log('Client not connected!');
        } else {
          console.log('Client connected');
          this.deviceClient.onDeviceMethod('gotUser', 
            this.commandHandler.bind(this))
          this.deviceClient.onDeviceMethod('gotEntrance', 
            this.commandHandler.bind(this))
        }
      });
      sleep(1000)
    })
  }

  backToFirstScreen(){
    setTimeout( () => {
      this.stepper.selectedIndex = 0;
      this.refresh()
      console.log('screen 0')
    }, 5000)
    this.gotComand = false
  }

  handleIdAndRole(role?:string){
    if(role)
      this.role = role
    this.api.function10(this.identificator_nr, this.role)
      .subscribe({
        next: (res:any) => {
          if (!res.reason_of_disallowance){
            if (this.role == "KLIENT" || this.role == "TRENER"){
              if (this.role == "KLIENT"){
                this.package.package_id = res?.package.package_ID
                this.package.package_name = res?.package.package_name
              }
              this.api.function11()
                .subscribe({
                  next: (_res:any) => {
                    this.lessons = _res.map( (r:any) => {
                      return {id: r.lesson_type_id, name: r.name}
                    })
                    this.stepper.selectedIndex = 4
                    this.refresh()
                  },
                  error: (err:any) => {
                    this.showError(err.error)
                  }
                })
            } else {
              this.handleEntrance(undefined, res?.justification?.description, undefined)
            }
            
          } else {
            this.showError(res.reason_of_disallowance)
          }
        },
        error: (err:any) => {
          this.showError(err.error)
        }
      })
  }

  refresh(){
    (this.response as any)._transport.sendEvent(new Message(new Buffer("À", "ascii")), (err:any, res:any)=>{})
  }

  showError(_error:string){
    this.cause = _error
    this.stepper.selectedIndex = 3
    this.refresh()
    this.backToFirstScreen()
  }

  handleEntrance(lesson_id?:number, justification?:string, _package?:{id?:number, name?:string}){
    this.api.function12(this.identificator_nr, this.role, lesson_id, justification, _package)
      .subscribe({
        next: () => {
          this.stepper.selectedIndex = 5
          this.refresh()
          this.gotComand = false
        },
        error: (err:any) => {
          this.showError(err.error)
        }
      })
  }

  handleLessonChoose(lesson:{id:number, name:string}){
    if(this.role == 'KLIENT'){
      this.api.function3(this.identificator_nr, new Date().toISOString().split('T')[0], null)
        .subscribe({
          next: (res:any) => {
            if (res?.entrance_allowed) {
              this.handleEntrance(lesson.id, undefined, {id: this.package.package_id, name: this.package.package_name})
            } else {
              this.showError(res?.reason_of_disallowance)
            }
          },
          error: (err:any) => {
            this.showError(err.error)
          }
        })
    } else {
      this.handleEntrance(lesson.id, undefined, undefined)
    }
  }

}
