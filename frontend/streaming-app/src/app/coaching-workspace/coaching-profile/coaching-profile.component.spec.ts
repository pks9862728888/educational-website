import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CoachingProfileComponent } from './coaching-profile.component';

describe('CoachingProfileComponent', () => {
  let component: CoachingProfileComponent;
  let fixture: ComponentFixture<CoachingProfileComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CoachingProfileComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CoachingProfileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
