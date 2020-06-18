import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { StaffWorkspaceComponent } from './staff-workspace.component';

describe('StaffWorkspaceComponent', () => {
  let component: StaffWorkspaceComponent;
  let fixture: ComponentFixture<StaffWorkspaceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ StaffWorkspaceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(StaffWorkspaceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
