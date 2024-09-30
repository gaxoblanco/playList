import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';
import { Observable, BehaviorSubject, Subject } from 'rxjs';
import { ListBand } from '../models/list_band';
import { ObservablesService } from './observables.service';

@Injectable({
  providedIn: 'root',
})
export class ProcesListService {
  private apiUrl = 'http://localhost:5000';
  constructor(
    private http: HttpClient,
    private cookieService: CookieService,
    private observablesService: ObservablesService
  ) {}

  // ----------------------------------------------------------------
  public connectors = [
    'la',
    'el',
    'los',
    'las',
    'le',
    'lo',
    'es',
    'tan',
    'a',
    'un',
    'y',
    'de',
    'del',
    'al',
    'the',
    'and',
    'of',
    'in',
    'on',
    'at',
    'for',
    'with',
    '1',
    '2',
    '3',
    '4',
    '5',
    '6',
    '7',
    '8',
    '9',
    '0',
  ];
  generateWordCombinations(input: string): any {
    // Pasar a minúsculas y dividir el input en palabras
    input = input.toLowerCase();
    const words = input.trim().split(' ');

    // Array para almacenar las combinaciones
    const combinations: string[] = [];

    // Generar combinaciones de palabras
    for (let i = 0; i < words.length; i++) {
      let phrase = words[i];

      // Agregar solo combinaciones que no sean un conector aislado
      if (!this.connectors.includes(phrase)) {
        combinations.push(phrase);
      }

      // Iterar sobre las palabras siguientes y generar combinaciones
      for (let j = i + 1; j < words.length; j++) {
        phrase += ' ' + words[j];

        // Verificar que la combinación no termine ni comience con un conector
        const phraseWords = phrase.trim().split(' ');
        const startsWithConnector = this.connectors.includes(phraseWords[0]);
        const endsWithConnector = this.connectors.includes(
          phraseWords[phraseWords.length - 1]
        );

        // Verificar que la combinación no sea solo conectores
        const onlyConnectors = phraseWords.every((word) =>
          this.connectors.includes(word)
        );

        // Agregar solo si no es solo conectores y no empieza o termina con uno
        if (!onlyConnectors && !startsWithConnector && !endsWithConnector) {
          combinations.push(phrase);
        }
      }
    }

    return combinations;
  }

  // Start --- Limpiesa y creacion del array de bandas
  // optionList$ === bandList.json
  startGameCorrector(): void {
    // nextStep$ == 0 start process
    this.observablesService.resetNextStep();
    this.observablesService.optionList$.subscribe(async (options) => {
      for (const option of options) {
        // paso todo a lowercase
        option.name = option.name.toLowerCase();
        const words = option.name.trim().split(' ');
        const bandErrors = this.generateWordCombinations(option.name);

        // valido que la palabra del medio sea un conector
        if (words[1] == 'de' || words[1] == 'del' || words[1] == 'the') {
          // cargo option en el observable updateBandListCorect
          this.observablesService.addBandListCorect(option);
          // emito un movimiento emitShowContinueButton
          this.observablesService.emitShowContinueButton();
          console.log('pase por aqui', words[1]);
        } else if (bandErrors.length > 3) {
          // // valido que la palabra del medio sea un conector
          // if (words[1] == 'de' || words[1] == 'del' || words[1] == 'the') {
          //   // cargo option en el observable updateBandListCorect
          //   this.observablesService.addBandListCorect(option);
          //   // emito un movimiento emitShowContinueButton
          //   this.observablesService.emitShowContinueButton();
          //   console.log('pase por aqui', words[1]);
          // }
          // cargo las nuevas opciones en el observable updateOptionError
          this.observablesService.updateOptionError(bandErrors);
          console.log('Errores:', bandErrors);

          // espero a que showContinueButtonSubject cambie
          // para continuar con el siguiente grupo
          await this.observablesService.waitForShowContinueButton().then(() => {
            console.log('Siguiente grupo');
          });
        } else if (bandErrors.length < 3) {
          // cargo option en el observable updateBandListCorect
          this.observablesService.addBandListCorect(option);
        }
      }
      this.observablesService.incrementNextStep();
      console.log('nextStep$:', this.observablesService);
    });
  }
  //----------------------------------------------------------------
  //
}
