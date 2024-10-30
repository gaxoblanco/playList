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
    // Verificar si el nombre ya existe en bandListCorect
    if (!current.some((b) => b.name === data.name)) {
      current.push(data);
      this.bandListCorect.next(current);
    }
  }

  // --- observable to continue corretion ---
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

  // --- observable to next step que tiene un contador ---
  // BehaviorSubject para el contador
  private nextStepSubject: BehaviorSubject<number> =
    new BehaviorSubject<number>(0);
  // Observable para el contador
  nextStep$: Observable<number> = this.nextStepSubject.asObservable();
  // Method para actualizar el contador
  public updateNextStep(data: number): void {
    this.nextStepSubject.next(data);
  }
  // Method para incrementar el contador
  public incrementNextStep(): void {
    const current = this.nextStepSubject.getValue();
    this.nextStepSubject.next(current + 1);
    console.log('<--incrementNextStep-->', this.nextStepSubject.value);
  }
  // Method para resetear el contador
  public resetNextStep(): void {
    this.nextStepSubject.next(0);
  }
  // Method para obtener el vlaor del contador
  public getStep(): number {
    return this.nextStepSubject.getValue();
  }

  // --- Img Pointer observable ImgPointer$ = [number, number, number, number]
  //BehaviorSubject para ImgPointer
  private imgPointerSubject = new BehaviorSubject<
    [number, number, number, number]
  >([0, 0, 0, 0]);
  public ImgPointer$: Observable<[number, number, number, number]> =
    this.imgPointerSubject.asObservable();

  // Método para actualizar el puntero de la imagen
  public updateImgPointer(pointer: [number, number, number, number]): void {
    this.imgPointerSubject.next(pointer);
  }
}
