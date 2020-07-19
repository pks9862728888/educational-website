import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { CoachingWorkspaceComponent } from './coaching-workspace.component';

describe('CoachingWorkspaceComponent', () => {
  let component: CoachingWorkspaceComponent;
  let fixture: ComponentFixture<CoachingWorkspaceComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ CoachingWorkspaceComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(CoachingWorkspaceComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
