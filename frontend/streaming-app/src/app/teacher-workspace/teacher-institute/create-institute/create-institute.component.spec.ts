import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CreateInstituteComponent } from './create-institute.component';

describe('CreateCollegeComponent', () => {
  let component: CreateInstituteComponent;
  let fixture: ComponentFixture<CreateInstituteComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CreateInstituteComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CreateInstituteComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
