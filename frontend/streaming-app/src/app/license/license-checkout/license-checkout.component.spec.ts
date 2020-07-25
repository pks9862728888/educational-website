import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LicenseCheckoutComponent } from './license-checkout.component';

describe('LicenseCheckoutComponent', () => {
  let component: LicenseCheckoutComponent;
  let fixture: ComponentFixture<LicenseCheckoutComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LicenseCheckoutComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LicenseCheckoutComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
