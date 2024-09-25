import { NgModule } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import {
  MatChipEditedEvent,
  MatChipInputEvent,
  MatChipsModule,
} from '@angular/material/chips';
import { LoadingModel } from '../models/loading';
import { MatIconModule } from '@angular/material/icon';
import { LiveAnnouncer } from '@angular/cdk/a11y';

import { CookieService } from 'ngx-cookie-service';

import { ProcesListService } from '../services/proces-list.service';
import { ListBand } from '../models/list_band';

@Component({
  selector: 'app-up-img',
  templateUrl: './up-img.component.html',
  styleUrls: ['./up-img.component.scss'],
  standalone: true,
  imports: [MatCardModule, MatChipsModule, MatIconModule, CommonModule],
})
export class UpImgComponent {
  selectedFile: File | null = null;
  showContinueButton = false;
  loading: LoadingModel = 'up';
  optionList: any[] = [];
  currentErrors: string[] = [];
  selectedList: number = 0;
  announcer: LiveAnnouncer | undefined;

  headers = new HttpHeaders({
    'Access-Control-Allow-Origin': '*', // Permite todas las orígenes
    'Content-Type': 'multipart/form-data', // Ajusta el tipo de contenido si es necesario
  });

  constructor(
    private http: HttpClient,
    private procesListService: ProcesListService,
    private cookieService: CookieService
  ) {}

  ngOnInit(): void {}

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
    }
    this.loading = 'loading';

    try {
      // Si hay un archivo seleccionado, se lo enviamos a la API
      if (this.selectedFile) {
        const formData = new FormData();
        formData.append('img', this.selectedFile);

        // Hacer post a la URL http://localhost:5000/up_img con la imagen y obtener el JSON
        this.procesListService.postImg(formData).subscribe({
          next: async (data: ListBand[]) => {
            // Guardar la data en localStorage
            localStorage.setItem('BandList', JSON.stringify(data));
            // Leer la data de localStorage y loguear su valor
            const storedData = localStorage.getItem('BandList');
            // console.log('Valor de BandList en localStorage:', storedData);

            for (const band of data) {
              // genero el array de las posibles combinacion de errores
              const bandErrors =
                this.procesListService.generateWordCombinations(band.name);

              // Valido que bandErrors tenga elementos
              if (bandErrors.length > 3) {
                // cargo las nuevas opciones
                this.optionList = [...bandErrors];

                // Esperar a que el usuario haga clic en "continuar"
                await this.waitForUserConfirmation();

                // Agregar los errores detectados a la lista de opciones
                // this.optionList = [...this.optionList, ...bandErrors];
              }
            }
          },
          error: (error) => {
            console.error(error);
          },
        });
      }
    } catch (error) {
      console.log('Error:', error);
    }
  }

  uploadImage(): void {
    if (this.selectedFile) {
      console.log('Archivo seleccionado:', this.selectedFile);
      // Aquí puedes implementar la lógica para subir la imagen a tu API
    } else {
      console.log('No se ha seleccionado ninguna imagen');
    }
  }
  //----------------------------------------------------------------
  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();

    // Add our option
    if (value) {
      // this.optionList = [...this.optionList, { name: value }];
    }

    // Clear the input value
    event.chipInput!.clear();
  }

  remove(option: any): void {
    const index = this.optionList.indexOf(option);
    if (index >= 0) {
      this.optionList.splice(index, 1);
      if (this.announcer) {
        this.announcer.announce(`Removed ${option.name}`);
      }
    }
  }

  edit(option: any, event: MatChipEditedEvent) {
    const value = event.value.trim();

    // Remove option if it no longer has a name
    if (!value) {
      this.remove(option);
      return;
    }

    // Remove option if it no longer has a name
    if (!value) {
      this.remove(option);
      return;
    }

    // Edit existing option
    this.optionList = this.optionList.map((item: any) => {
      if (item === option) {
        return { ...item, name: value };
      }
      return item;
    });
  }

  //----------------------------------------------------------------
  // Función para esperar a que el usuario haga clic en "continuar"
  async waitForUserConfirmation(): Promise<void> {
    return new Promise<void>((resolve) => {
      const button = document.getElementById('continue-button');
      if (button) {
        button.addEventListener('click', () => {
          this.showContinueButton = false; // Ocultar el botón después del clic
          resolve(); // Resuelve la promesa cuando el usuario hace clic
        });
      }
    });
  }
}
