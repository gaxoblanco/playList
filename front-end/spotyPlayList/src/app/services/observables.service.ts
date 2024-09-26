import { Injectable } from '@angular/core';
import { CookieService } from 'ngx-cookie-service';
import { Observable, BehaviorSubject, Subject } from 'rxjs';
import { ListBand } from '../models/list_band';

@Injectable({
  providedIn: 'root',
})
export class ObservablesService {
  constructor() {}

  // --- fist list band ---
  // BehaviorSubject to hold the array
  private optionListSubject: BehaviorSubject<any[]> = new BehaviorSubject<
    any[]
  >([]);
  // Observable to expose the array
  optionList$: Observable<any[]> = this.optionListSubject.asObservable();
  // Public method to update optionListSubject
  public updateOptionList(data: any[]): void {
    this.optionListSubject.next(data);
  }
  // --- list refactor the band name ---
  // BehaviorSubject para la lista de errores
  private optionErrorSubject: BehaviorSubject<string[]> = new BehaviorSubject<
    string[]
  >([]);
  // Oberservable para la lista de errores
  optionError$: Observable<string[]> = this.optionErrorSubject.asObservable();
  // method to update optionListSubject
  public updateOptionError(data: string[]): void {
    this.optionErrorSubject.next(data);
  }

  // --- second list band ---
  // BehaviorSubject to hold the array
  private bandListCorect: BehaviorSubject<ListBand[]> = new BehaviorSubject<
    ListBand[]
  >([]);
  // Observable to expose the array
  bandListCorect$: Observable<ListBand[]> = this.bandListCorect.asObservable();
  // Public method to update optionListSubject
  public updateBandListCorect(data: ListBand[]): void {
    this.bandListCorect.next(data);
  }
  // Public method to add new band to bandListCorect
  public addBandListCorect(data: ListBand): void {
    const current = this.bandListCorect.getValue();
    current.push(data);
    this.bandListCorect.next(current);
  }

  //----------------------------------------------------------------
  // Subject para emitir el valor cuando showContinueButton cambia
  private showContinueButtonSubject = new Subject<void>();
  // Method para emitir el valor cuando showContinueButton cambia
  emitShowContinueButton(): void {
    this.showContinueButtonSubject.next();
  }
  // Method to wait for showContinueButton to change
  waitForShowContinueButton(): Promise<void> {
    return new Promise((resolve) => {
      this.showContinueButtonSubject.subscribe(() => {
        resolve();
      });
    });
  }
}
