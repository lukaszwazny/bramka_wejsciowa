import { Component, OnInit, ViewChild } from '@angular/core';
import { MatStepper } from '@angular/material/stepper/stepper';
import { Client } from 'azure-iot-device';
import { AnimationOptions } from 'ngx-lottie';
import { IotConnectService } from '../services/iot-connect.service';
import { sleep } from '../services/utils';

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

  lessons = [
    {id: 1, name: 'MUAY THAI'},
    {id: 2, name: 'BOKS'},
    {id: 3, name: 'JUDO'},
    {id: 4, name: 'PILATES'},
  ]

  identificator_nr?:string
  roles?:Array<string>

  cause ?: String

  deviceClient:any
  gotComand:boolean

  constructor(private iotConnectService: IotConnectService) {this.gotComand = false}

  async commandHandler(request:any, response:any) {
    if (!this.gotComand){
      this.gotComand = true
      switch (request.methodName) {
      case 'gotUser': {
        console.log(request)
        //await this.sendCommandResponse(request, response, 200, 'ok');
        if (request.payload?.identificator_nr){
          this.identificator_nr = request.payload?.identificator_nr
          this.roles = request.payload?.roles
        } else {
          this.stepper.selectedIndex = 1;
          //this.stepper.selected = this.stepper.steps.get(1)
          console.log(this.stepper.selectedIndex)
          console.log(this)
          // setTimeout( () => {
          //   this.stepper.selectedIndex = 0;
          //   console.log('screen 0')
          // }, 3000)
        }
        
        break;
      }
      case 'gotEntrance': {
        console.log(request)
        break;
      }
      default:
        //await this.sendCommandResponse(request, response, 404, 'unknown method');
        break;
      }
      this.gotComand = false
    } else {
      //await this.sendCommandResponse(request, response, 404, 'application now busy');
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
          this.deviceClient.onDeviceMethod('gotEntrance', (request:any, response:any) => {this.commandHandler(request, response)})
        }
      });
      sleep(700)
    })
  }

  ngAfterViewInit() {
    console.log(this.stepper); // correctly outputs the element in console, not undefined
    this.stepper.steps.forEach(Step => {
      Step.completed = false;
    });
  }

  setScreen(i:number){
    this.stepper.linear = false;
    this.stepper.selectedIndex = i;
    setTimeout(() => {
       this.stepper.linear = true;
    });
  }

}
