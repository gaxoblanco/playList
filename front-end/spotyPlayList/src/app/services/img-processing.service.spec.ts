import { TestBed } from '@angular/core/testing';

import { ImgProcessingService } from './img-processing.service';

describe('ImgProcessingService', () => {
  let service: ImgProcessingService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ImgProcessingService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
