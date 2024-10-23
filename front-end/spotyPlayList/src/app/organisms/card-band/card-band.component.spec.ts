import { ComponentFixture, TestBed } from '@angular/core/testing';

import { CardBandComponent } from './card-band.component';

describe('CardBandComponent', () => {
  let component: CardBandComponent;
  let fixture: ComponentFixture<CardBandComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [CardBandComponent]
    });
    fixture = TestBed.createComponent(CardBandComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
