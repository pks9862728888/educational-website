import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TeacherInstituteComponent } from './teacher-institute.component';

describe('TeacherInstituteComponent', () => {
  let component: TeacherInstituteComponent;
  let fixture: ComponentFixture<TeacherInstituteComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TeacherInstituteComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TeacherInstituteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
