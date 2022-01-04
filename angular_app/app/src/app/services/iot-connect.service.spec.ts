import { TestBed } from '@angular/core/testing';

import { IotConnectService } from './iot-connect.service';

describe('IotConnectService', () => {
  let service: IotConnectService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(IotConnectService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
