import { TestBed } from '@angular/core/testing';

import { ProcesListService } from './proces-list.service';

describe('ProcesListService', () => {
  let service: ProcesListService;

  beforeEach(() => {
    TestBed.configureTestingModule({});
    service = TestBed.inject(ProcesListService);
  });

  it('should be created', () => {
    expect(service).toBeTruthy();
  });
});
