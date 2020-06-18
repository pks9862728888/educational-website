import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { BlockedMembersComponent } from './blocked-members.component';

describe('BlockedMembersComponent', () => {
  let component: BlockedMembersComponent;
  let fixture: ComponentFixture<BlockedMembersComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ BlockedMembersComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(BlockedMembersComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
