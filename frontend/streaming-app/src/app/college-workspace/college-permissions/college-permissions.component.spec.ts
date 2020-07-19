import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CollegePermissionsComponent } from './college-permissions.component';

describe('CollegePermissionsComponent', () => {
  let component: CollegePermissionsComponent;
  let fixture: ComponentFixture<CollegePermissionsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CollegePermissionsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CollegePermissionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
