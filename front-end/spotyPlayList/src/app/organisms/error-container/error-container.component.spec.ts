import { ComponentFixture, TestBed } from '@angular/core/testing';

import { ErrorContainerComponent } from './error-container.component';

describe('ErrorContainerComponent', () => {
  let component: ErrorContainerComponent;
  let fixture: ComponentFixture<ErrorContainerComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [ErrorContainerComponent]
    });
    fixture = TestBed.createComponent(ErrorContainerComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
