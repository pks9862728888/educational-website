import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateCollegeComponent } from './create-college.component';

describe('CreateCollegeComponent', () => {
  let component: CreateCollegeComponent;
  let fixture: ComponentFixture<CreateCollegeComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateCollegeComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateCollegeComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
