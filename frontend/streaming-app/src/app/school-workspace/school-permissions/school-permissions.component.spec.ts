import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SchoolPermissionsComponent } from './school-permissions.component';

describe('SchoolPermissionsComponent', () => {
  let component: SchoolPermissionsComponent;
  let fixture: ComponentFixture<SchoolPermissionsComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SchoolPermissionsComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SchoolPermissionsComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
