import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CollegeWorkspaceComponent } from './college-workspace.component';

describe('CollegeWorkspaceComponent', () => {
  let component: CollegeWorkspaceComponent;
  let fixture: ComponentFixture<CollegeWorkspaceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CollegeWorkspaceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CollegeWorkspaceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
