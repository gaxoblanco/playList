import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CardBandMobileComponent } from './card-band-mobile.component';

describe('CardBandMobileComponent', () => {
  let component: CardBandMobileComponent;
  let fixture: ComponentFixture<CardBandMobileComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CardBandMobileComponent]
    });
    fixture = TestBed.createComponent(CardBandMobileComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
