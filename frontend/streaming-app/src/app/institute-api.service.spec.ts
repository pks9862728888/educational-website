import { TestBed } from '@angular/core/testing';

import { InstituteApiService } from './institute-api.service';

describe('InstituteApiService', () => {
  let service: InstituteApiService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(InstituteApiService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
