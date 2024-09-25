import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';
import { Observable, of } from 'rxjs';

@Injectable({
  providedIn: 'root',
})
export class ProcesListService {
  private apiUrl = 'http://localhost:5000';

  constructor(private http: HttpClient, private cookieService: CookieService) {}

  // Obtengo el token de acceso
  postCode(code: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      code: code,
    });

    return this.http.post<any>(
      `${this.apiUrl}/callback`,
      { code },
      { headers }
    );
  }

  // Envio la img y obtengo el json
  postImg(img: FormData): Observable<any> {
    console.log('img -->', img);

    // No es necesario establecer 'Content-Type' para FormData
    return this.http.post<any>(`${this.apiUrl}/up_img`, img);
  }

  // Subfunción para validar si una cadena tiene 3 o más espacios
  hasThreeOrMoreSpaces(text: string): boolean {
    let count = 0;
    for (const char of text) {
      if (char === ' ') {
        count += 1;
        if (count >= 3) {
          return true;
        }
      } else {
        count = 0;
      }
    }
    return false;
  }

  // Función para detectar errores en los nombres de la lista de bandas
  // detectPossibleErrors(bandList: any[]): any[] {
  //   const errorPatterns = [
  //     /La .*la/i,
  //     /la .*La/i,
  //     /la .*la /i,
  //     /LA .*LA /i,
  //     /El .*el/i,
  //     /el .*El/i,
  //     /el .*el /i,
  //     /EL .*EL /i,
  //     /Los .*los/i,
  //     /los .*Los/i,
  //     /los .*los /i,
  //     /LOS .*LOS /i,
  //     /La .*los/i,
  //     /la .*Los/i,
  //     /La .*el/i,
  //     /la .*El/i,
  //     /Los .*la/i,
  //     /los .*La/i,
  //     /El .*los/i,
  //     /el .*Los/i,
  //     /El .*la/i,
  //     /el .*La/i,
  //     /Los .*el/i,
  //     /los .*El/i,
  //     /&/,
  //     / y /i,
  //     / Y /i,
  //     / x /,
  //     / X /,
  //     /: /,
  //   ];

  //   const correctedNames: any[] = [];

  //   bandList.forEach((band) => {
  //     const name = band.name;
  //     let hasError = false;

  //     // Verificar si algún patrón coincide
  //     for (const pattern of errorPatterns) {
  //       if (pattern.test(name)) {
  //         hasError = true;
  //         break;
  //       }
  //     }

  //     // Verificar si la cadena tiene 3 o más espacios
  //     if (this.hasThreeOrMoreSpaces(name)) {
  //       hasError = true;
  //       console.log(`Nombre con 3 o más espacios detectado: ${name}`);
  //     }

  //     if (hasError) {
  //       console.log(`Nombre problemático encontrado: ${name}`);

  //       // Pedir el nombre correcto al usuario
  //       const correctName = prompt(
  //         `Ingrese el nombre correcto para "${name}" o deje vacío para mantener el actual: `
  //       );

  //       // Si el usuario ingresa un nombre nuevo, actualizar
  //       if (correctName && correctName.trim() !== '') {
  //         band.name = correctName.trim();
  //       }

  //       correctedNames.push(band);

  //       // Bucle para ingresar campos adicionales como nuevos elementos
  //       let extraField: string | null;
  //       do {
  //         extraField = prompt(
  //           'Ingrese un valor adicional o deje vacío para finalizar: '
  //         );
  //         if (extraField && extraField.trim() !== '') {
  //           correctedNames.push({ name: extraField.trim(), band_id: '' });
  //         }
  //       } while (extraField && extraField.trim() !== '');
  //     } else {
  //       correctedNames.push(band);
  //     }
  //   });

  //   // Guardar los nombres corregidos en una cookie
  //   this.cookieService.set('correctedBandList', JSON.stringify(correctedNames));

  //   return correctedNames;
  // }

  // Método para obtener los nombres corregidos desde la cookie
  getCorrectedNamesFromCookie(): any[] {
    const correctedBandList = this.cookieService.get('correctedBandList');
    if (correctedBandList) {
      return JSON.parse(correctedBandList);
    }
    return [];
  }

  // Generar combinaciones de subcadenas basadas en el nombre completo
  generateNameOptions(fullName: string): string[] {
    const words = fullName.split(' ');
    const options: string[] = [];

    // Crear combinaciones de subcadenas
    for (let i = 0; i < words.length; i++) {
      for (let j = i + 1; j <= words.length; j++) {
        options.push(words.slice(i, j).join(' '));
      }
    }

    return options;
  }

  // Simulación de detección de errores
  detectPossibleErrors(band: any): string[] {
    const errors: string[] = [];
    // Simulación de validación de errores
    if (band.name.includes('error')) {
      errors.push(`Error encontrado en la banda: ${band.name}`);
    }
    return errors;
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
}
