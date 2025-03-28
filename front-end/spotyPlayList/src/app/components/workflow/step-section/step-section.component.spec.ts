import { ComponentFixture, TestBed } from '@angular/core/testing';

import { StepSrctionComponent } from './step-section.component';

describe('StepSrctionComponent', () => {
  let component: StepSrctionComponent;
  let fixture: ComponentFixture<StepSrctionComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [StepSrctionComponent]
    });
    fixture = TestBed.createComponent(StepSrctionComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
