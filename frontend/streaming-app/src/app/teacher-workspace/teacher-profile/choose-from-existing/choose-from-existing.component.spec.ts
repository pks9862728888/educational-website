import { async, ComponentFixture, TestBed } from '@angular/core/testing';

import { ChooseFromExistingComponent } from './choose-from-existing.component';

describe('ChooseFromExistingComponent', () => {
  let component: ChooseFromExistingComponent;
  let fixture: ComponentFixture<ChooseFromExistingComponent>;

  beforeEach(async(() => {
    TestBed.configureTestingModule({
      declarations: [ ChooseFromExistingComponent ]
    })
    .compileComponents();
  }));

  beforeEach(() => {
    fixture = TestBed.createComponent(ChooseFromExistingComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
