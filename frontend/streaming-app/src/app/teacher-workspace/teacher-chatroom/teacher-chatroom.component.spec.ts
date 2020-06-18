import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TeacherChatroomComponent } from './teacher-chatroom.component';

describe('TeacherChatroomComponent', () => {
  let component: TeacherChatroomComponent;
  let fixture: ComponentFixture<TeacherChatroomComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TeacherChatroomComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TeacherChatroomComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
