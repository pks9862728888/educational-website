import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TeacherMockTestComponent } from './teacher-mock-test.component';

describe('TeacherMockTestComponent', () => {
  let component: TeacherMockTestComponent;
  let fixture: ComponentFixture<TeacherMockTestComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TeacherMockTestComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TeacherMockTestComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
