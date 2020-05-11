import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TeacherFeedbackComponent } from './teacher-feedback.component';

describe('TeacherFeedbackComponent', () => {
  let component: TeacherFeedbackComponent;
  let fixture: ComponentFixture<TeacherFeedbackComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TeacherFeedbackComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TeacherFeedbackComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
