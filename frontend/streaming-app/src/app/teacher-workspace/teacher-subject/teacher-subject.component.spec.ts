import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TeacherSubjectComponent } from './teacher-subject.component';

describe('TeacherSubjectComponent', () => {
  let component: TeacherSubjectComponent;
  let fixture: ComponentFixture<TeacherSubjectComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TeacherSubjectComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TeacherSubjectComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
