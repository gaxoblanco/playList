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

  // Envio la img y obtengo el json
  postImg(img: FormData): Observable<any> {
    console.log('img -->', img);

    // No es necesario establecer 'Content-Type' para FormData
    return this.http.post<any>(`${this.apiUrl}/up_img`, img);
  }

  // ----------------------------------------------------------------
  generateWordCombinations(input: string): any {
    // Lista de conectores
    const connectors = [
      'la',
      'el',
      'los',
      'las',
      'le',
      'lo',
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
    // pasar la cadena completa a minúsculas
    input = input.toLowerCase();

    // Dividir la cadena en un array de palabras
    const words = input.trim().split(' ');

    // Array para almacenar las combinaciones
    const combinations: string[] = [];

    // Iterar sobre cada palabra en el array
    for (let i = 0; i < words.length; i++) {
      let phrase = words[i];
      // valido que sea un conector
      if (connectors.includes(words[i])) {
        combinations.push(phrase); // Añadir la palabra sola al array
      }
      combinations.push(phrase);
      // Iterar sobre las palabras siguientes y generar combinaciones
      for (let j = i + 1; j < words.length; j++) {
        phrase += ' ' + words[j]; // Agregar la siguiente palabra a la frase
        combinations.push(phrase); // Añadir la nueva combinación al array
      }

      // Verificar si contiene solo conectores al inicio, si es así, no agregamos
      //  const firstWord = combinations.split(' ')[0].toLowerCase();
      if (connectors.includes(words[i])) {
        combinations.pop(); // pop = elimina el último elemento del array
      }
    }
    return combinations;
  }

  // Start --- Limpiesa y creacion del array de bandas
  // optionList$ === bandList.json
  startGameCorrector(): void {
    this.observablesService.optionList$.subscribe(async (options) => {
      for (const option of options) {
        // paso todo a lowercase
        option.name = option.name.toLowerCase();
        const words = option.name.trim().split(' ');
        const bandErrors = this.generateWordCombinations(option.name);

        // Valido que bandErrors tenga mas de 3 elementos === 2 " "
        // valido que la palabra del medio sea un conector
        if (words[1] == 'de' || words[1] == 'del' || words[1] == 'the') {
          // cargo option en el observable updateBandListCorect
          this.observablesService.addBandListCorect(option);
          // emito un movimiento emitShowContinueButton
          this.observablesService.emitShowContinueButton();
          console.log('pase por aqui', words[1]);
        } else if (bandErrors.length > 3) {
          // valido que la palabra del medio sea un conector
          if (words[1] == 'de' || words[1] == 'del' || words[1] == 'the') {
            // cargo option en el observable updateBandListCorect
            this.observablesService.addBandListCorect(option);
            // emito un movimiento emitShowContinueButton
            this.observablesService.emitShowContinueButton();
            console.log('pase por aqui', words[1]);
          }
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
    });
  }
}
