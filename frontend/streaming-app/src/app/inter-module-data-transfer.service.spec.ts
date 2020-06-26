import { TestBed } from '@angular/core/testing';

import { InterModuleDataTransferService } from './inter-module-data-transfer.service';

describe('InterModuleDataTransferService', () => {
  let service: InterModuleDataTransferService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(InterModuleDataTransferService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
