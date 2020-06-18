import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { TeacherResourcesComponent } from './teacher-resources.component';

describe('TeacherResourcesComponent', () => {
  let component: TeacherResourcesComponent;
  let fixture: ComponentFixture<TeacherResourcesComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ TeacherResourcesComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(TeacherResourcesComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
