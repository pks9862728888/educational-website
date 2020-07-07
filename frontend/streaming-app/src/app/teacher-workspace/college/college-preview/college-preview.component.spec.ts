import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CollegePreviewComponent } from './college-preview.component';

describe('CollegePreviewComponent', () => {
  let component: CollegePreviewComponent;
  let fixture: ComponentFixture<CollegePreviewComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CollegePreviewComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CollegePreviewComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
