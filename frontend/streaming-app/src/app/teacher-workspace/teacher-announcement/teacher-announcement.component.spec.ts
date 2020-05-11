import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TeacherAnnouncementComponent } from './teacher-announcement.component';

describe('TeacherAnnouncementComponent', () => {
  let component: TeacherAnnouncementComponent;
  let fixture: ComponentFixture<TeacherAnnouncementComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TeacherAnnouncementComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TeacherAnnouncementComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
