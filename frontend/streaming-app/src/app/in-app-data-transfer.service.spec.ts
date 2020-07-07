import { TestBed } from '@angular/core/testing';

import { InAppDataTransferService } from './in-app-data-transfer.service';

describe('InterModuleDataTransferService', () => {
  let service: InAppDataTransferService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(InAppDataTransferService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
