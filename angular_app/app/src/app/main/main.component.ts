import { Component, OnInit, ViewChild } from '@angular/core';
import { MatStepper } from '@angular/material/stepper/stepper';
import { AnimationOptions } from 'ngx-lottie';
import { IotConnectService } from '../services/iot-connect.service';

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

  roles = [
    {id: 1, name: 'KLIENT'},
    {id: 2, name: 'TRENER'},
    {id: 3, name: 'WIDZ'},
    {id: 4, name: 'RECEPCJA'},
    {id: 5, name: 'ADMIN'},
  ]

  cause : String = ""

  constructor(private iotConnectService: IotConnectService) {}


  ngOnInit(): void {
    this.iotConnectService.connectDevice()
  }

  ngAfterViewInit() {
    console.log(this.stepper); // correctly outputs the element in console, not undefined
}

}
