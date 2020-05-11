import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TeacherCollegeComponent } from './teacher-college.component';

describe('TeacherCollegeComponent', () => {
  let component: TeacherCollegeComponent;
  let fixture: ComponentFixture<TeacherCollegeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TeacherCollegeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TeacherCollegeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
