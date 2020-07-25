import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { LicenseReviewComponent } from './license-review.component';

describe('LicenseReviewComponent', () => {
  let component: LicenseReviewComponent;
  let fixture: ComponentFixture<LicenseReviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ LicenseReviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(LicenseReviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
