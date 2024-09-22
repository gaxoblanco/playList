import { ComponentFixture, TestBed } from '@angular/core/testing';

import { UpImgComponent } from './up-img.component';

describe('UpImgComponent', () => {
  let component: UpImgComponent;
  let fixture: ComponentFixture<UpImgComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [UpImgComponent]
    });
    fixture = TestBed.createComponent(UpImgComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
