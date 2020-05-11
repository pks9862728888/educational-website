import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TeacherWorkspaceComponent } from './teacher-workspace.component';

describe('TeacherWorkspaceComponent', () => {
  let component: TeacherWorkspaceComponent;
  let fixture: ComponentFixture<TeacherWorkspaceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TeacherWorkspaceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TeacherWorkspaceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
