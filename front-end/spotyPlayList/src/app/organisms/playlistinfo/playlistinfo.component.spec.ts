import { ComponentFixture, TestBed } from '@angular/core/testing';

import { PlaylistinfoComponent } from './playlistinfo.component';

describe('PlaylistinfoComponent', () => {
  let component: PlaylistinfoComponent;
  let fixture: ComponentFixture<PlaylistinfoComponent>;

  beforeEach(() => {
    TestBed.configureTestingModule({
      declarations: [PlaylistinfoComponent]
    });
    fixture = TestBed.createComponent(PlaylistinfoComponent);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
