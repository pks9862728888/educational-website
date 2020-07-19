import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { SchoolWorkspaceComponent } from './school-workspace.component';

describe('SchoolWorkspaceComponent', () => {
  let component: SchoolWorkspaceComponent;
  let fixture: ComponentFixture<SchoolWorkspaceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ SchoolWorkspaceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(SchoolWorkspaceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
