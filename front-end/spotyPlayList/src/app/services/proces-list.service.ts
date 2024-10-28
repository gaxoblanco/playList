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
    'a',
    'un',
    'y',
    'al',
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
    console.log('words -->', words);

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
        // Convertimos el nombre a minúsculas y lo separamos en palabras
        const words = option.name.trim().toLowerCase().split(' ');
        // genero las combinaciones de palabras
        const bandErrors = this.generateWordCombinations(option.name);

        // valido que el split tenga 3 palabras
        if (words.length > 2) {
          const isValidName = this.isValidBandName(words);
          // valido que sea un nombre valido
          if (isValidName) {
            this.observablesService.addBandListCorect(option);
            // emito un movimiento emitShowContinueButton
            this.observablesService.emitShowContinueButton();
          } else {
            // elimino las opciones en bandErrors que sean un conector o middleConectr
            const cleanBandErrors = bandErrors.filter(
              (item: string) => !this.connectors.includes(item)
            );
            // cargo las nuevas opciones en el observable updateOptionError
            console.log('es un conector de inicio de nombre', words[1]);
            this.observablesService.updateOptionError(cleanBandErrors);

            // espero a que showContinueButtonSubject cambie
            // para continuar con el siguiente grupo
            await this.observablesService
              .waitForShowContinueButton()
              .then(() => {
                console.log('Siguiente grupo');
              });
          }
        }
        const band: ListBand = {
          band_id: '',
          name: option.name.trim().toLowerCase(),
        };
        // cargo option en el observable updateBandListCorect
        this.observablesService.addBandListCorect(band);
      }
      this.observablesService.incrementNextStep();
      console.log(
        'proces-list.services bandListCorect$:',
        this.observablesService['bandListCorect$']
      );
    });
  }
  //----------------------------------------------------------------
  //
  private isValidBandName(words: string[]): boolean {
    const validInitialConnectors = ['la', 'el', 'los', 'las', 'the'];
    const validSecondWordConnectors = [
      'de',
      'del',
      'es',
      'tan',
      'and',
      'in',
      'you',
      'on',
      'at',
    ];

    if (validInitialConnectors.includes(words[0])) {
      return true;
    }

    if (words.length > 2 && validSecondWordConnectors.includes(words[1])) {
      console.log('isValidBandName', words[1]);

      return true;
    }

    return false;
  }
}
