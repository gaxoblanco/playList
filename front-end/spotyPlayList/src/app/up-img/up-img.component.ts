import { Component, OnInit } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CommonModule } from '@angular/common';
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
import { ObservablesService } from '../services/observables.service';
import { ListBand } from '../models/list_band';
import { ApiRequestService } from '../services/api-request.service';

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
  imgSelected: any;
  headers = new HttpHeaders({
    'Access-Control-Allow-Origin': '*', // Permite todas las orígenes
    'Content-Type': 'multipart/form-data', // Ajusta el tipo de contenido si es necesario
  });

  bandListCorect: ListBand[] = [];

  constructor(
    private http: HttpClient,
    private procesListService: ProcesListService,
    private apiRequestService: ApiRequestService,
    private cookieService: CookieService,
    private observablesService: ObservablesService
  ) {}

  ngOnInit(): void {
    // observo si el optionList$ cambia, y mantengo optionList actualizado
    this.observablesService.optionError$.subscribe((options) => {
      this.optionList = options;
    });

    // clean localStorage
    localStorage.removeItem('uploadedImage');

    // Suscripción al observable nextStep$
    this.observablesService.nextStep$.subscribe((step) => {
      // Dependiendo del valor de step, ejecuta diferentes procesos
      switch (step) {
        case 1:
          // envio la lista actualizada con las correciones para obtener el band_id

          // this.bandListCorect = this.observablesService.bandListCorect$;
          console.log(
            'Step 1 - bandListCorect$ -->',
            this.observablesService.bandListCorect$
          );
          break;
        case 2:
          // Muestro el listado de bandas con su img despues de obtener su band_id
          break;
        case 3:
          // Genero la playList
          break;
        default:
          console.error('Paso no reconocido:', step);
      }
    });
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
    }
    this.loading = 'loading';
    //----------------------------------------------------------------
    if (input.files && input.files.length > 0) {
      // Guardamos el archivo seleccionado en la variable selectedFile
      this.selectedFile = input.files[0];

      // Usamos FileReader para leer el archivo como una URL Base64
      const reader = new FileReader();
      // Cuando la imagen se haya cargado exitosamente
      reader.onload = () => {
        // Asignamos el resultado (Base64) a la variable imgSelected para mostrar la imagen en la vista
        this.imgSelected = reader.result;
      };

      // Leemos el archivo como una URL Base64
      reader.readAsDataURL(this.selectedFile);
    } else {
      console.log('No se ha seleccionado ningún archivo');
    }
    //----------------------------------------------------------------
    if (input) {
      // Usamos FileReader para leer el archivo como una URL Base64
      const reader = new FileReader();

      // Cuando la imagen se haya cargado exitosamente
      reader.onload = () => {
        // Guardamos la imagen en localStorage
        localStorage.setItem('uploadedImage', reader.result as string);

        // Asignamos el resultado (Base64) a la variable imgSelected para mostrar la imagen en la vista
        this.imgSelected = reader.result;
      };
    }
    try {
      // Si hay un archivo seleccionado, se lo enviamos a la API
      if (this.selectedFile) {
        const formData = new FormData();
        formData.append('img', this.selectedFile);

        // Hacer post a la URL http://localhost:5000/up_img con la imagen y obtener el JSON
        this.apiRequestService.postImg(formData).subscribe({
          next: async (data: ListBand[]) => {
            // Guardar la data en localStorage
            localStorage.setItem('BandList', JSON.stringify(data));
            this.loading = 'done';

            // Leer la data de localStorage y loguear su valor
            const storedData = localStorage.getItem('BandList');
            // console.log('Valor de BandList en localStorage:', storedData);

            // cargo el observable con la lista de bandas
            this.observablesService.updateOptionList(data);
            // Start "game" corrector
            this.procesListService.startGameCorrector();
            // Usamos FileReader para leer el archivo como una URL Base64
            const reader = new FileReader();
            // Cuando la imagen se haya cargado exitosamente
            reader.onload = () => {
              // Asignamos el resultado (Base64) a la variable imgSelected para mostrar la imagen en la vista
              this.imgSelected = reader.result;
            };
            if (this.selectedFile) {
              reader.readAsDataURL(this.selectedFile);
            } else {
              console.error('No file selected');
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
  onSubmit(): void {
    console.log('siguiente grupo');
    this.showContinueButton = true;
  }
  selectedName: string = '';
  selectOption(option: string): void {
    this.selectedName = option;
    console.log('Opción seleccion', option);

    // quitos las opciones que ya no son posibles
    if (this.selectedName.includes(' ')) {
      // si tiene espacio lo separo en palabras
      const words = this.selectedName.split(' ');

      // comparo cada opcion en optionList y quito las que tengan palabras en comun
      words.forEach((word) => {
        if (!this.procesListService.connectors.includes(word)) {
          this.optionList = this.optionList.filter(
            (item) => !item.includes(word)
          );
        }
      });
    }
    const band: ListBand = {
      band_id: '',
      name: this.selectedName,
    };

    // cargo option en el observable updateBandListCorect
    this.observablesService.addBandListCorect(band);
    console.log('bandListCorect$', this.observablesService.bandListCorect$);

    // Itero por las opciones en optionList y alimino las que tengan option como parte de su string
    this.optionList = this.optionList.filter((item) => !item.includes(option));

    // si no tengo opciones en optionsList, emito un movimiento waitForShowContinueButton
    if (this.optionList.length === 0) {
      this.observablesService.emitShowContinueButton();
    }
  }
  //----------------------------------------------------------------
  // Función para esperar a que el usuario haga clic en "continuar"
  async waitForUserConfirmation(): Promise<void> {
    console.log('Esperando a que el usuario haga clic en "continuar"');
    // emito un movimiento waitForShowContinueButton
    this.observablesService.emitShowContinueButton();
    return new Promise<void>((resolve) => {
      const button = document.getElementById('continue-button');
    });
  }
}
