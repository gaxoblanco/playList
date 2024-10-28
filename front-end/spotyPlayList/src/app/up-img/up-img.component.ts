import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import {
  trigger,
  state,
  style,
  transition,
  animate,
} from '@angular/animations';
import { BehaviorSubject } from 'rxjs';

import { LoadingModel } from '../models/loading';

import { ProcesListService } from '../services/proces-list.service';
import { ObservablesService } from '../services/observables.service';
import { ListBand, optionBand } from '../models/list_band';
import { ApiRequestService } from '../services/api-request.service';
import { OptionsListComponent } from '../molecule/options-list/options-list.component';
import { CardBandComponent } from '../organisms/card-band/card-band.component';
@Component({
  selector: 'app-up-img',
  templateUrl: './up-img.component.html',
  styleUrls: ['./up-img.component.scss'],
  standalone: true,
  imports: [
    CommonModule,
    MatCardModule,
    MatChipsModule,
    MatIconModule,
    CommonModule,
    CardBandComponent,
  ],
})
export class UpImgComponent {
  step: number = 0;
  selectedFile: File | null = null;
  showContinueButton = false;
  loading: LoadingModel = 'up';
  optionList: any[] = [];
  currentErrors: string[] = [];
  selectedList: number = 0;
  announcer: LiveAnnouncer | undefined;
  imgSelected: any;
  tokenSpotify: any | undefined;
  requestTokenSpotify: boolean = true;
  bandListCorected: ListBand[] = [];
  selectedName: string = '';
  listb: any;
  //-----
  bandListCards: ListBand[] = [
    {
      band_id: '1',
      name: 'banda1',
      img: 'https://via.placeholder.com/150',
      genres: ['rock', 'salsa', 'sasea'],
    },
  ];
  optionsBand: optionBand[] = [
    { name: 'loading', img: 'https://via.placeholder.com/150' },
    { name: 'loading', img: 'https://via.placeholder.com/150' },
    { name: 'loading', img: 'https://via.placeholder.com/150' },
  ];

  constructor(
    private procesListService: ProcesListService,
    private apiRequestService: ApiRequestService,
    private observablesService: ObservablesService
  ) {}

  ngOnInit(): void {
    // this.observablesService.bandListCorect$.subscribe((bandList) => {
    //   this.bandList = bandList; // Actualiza la lista cuando el observable cambie
    // });
    // observo si el optionList$ cambia, y mantengo optionList actualizado
    this.observablesService.optionError$.subscribe((options) => {
      this.optionList = options;
    });
    // valido que tengo un token para Spotify
    this.tokenSpotify = localStorage.getItem('access_token');
    console.log('tokenSpotify', this.tokenSpotify);

    // clean localStorage
    localStorage.removeItem('uploadedImage');

    // Suscripción al observable nextStep$
    this.observablesService.nextStep$.subscribe((step) => {
      // valido que this.step sea diferente a step
      if (this.step !== step) {
        this.step = step;
        this.handleStepChange(step);
      }
    });
  }

  // funcion login que llama la url http://localhost:5000/login
  login() {
    window.location.href = 'http://localhost:5000/login';
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;

    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      this.loading = 'loading';

      const reader = new FileReader();
      reader.onload = () => {
        this.imgSelected = reader.result; // Mostrar la imagen en la vista
        localStorage.setItem('uploadedImage', reader.result as string); // Guardar imagen en localStorage
      };
      reader.readAsDataURL(this.selectedFile);

      this.uploadImageToAPI(this.selectedFile); // Subir archivo a la API y manejar la respuesta
    } else {
      console.log('No se ha seleccionado ningún archivo');
    }
  }

  // Método para manejar la carga de la imagen a la API y procesar la respuesta
  private uploadImageToAPI(file: File): void {
    const formData = new FormData();
    formData.append('img', file);

    this.apiRequestService.postImg(formData).subscribe({
      next: async (data: ListBand[]) => {
        localStorage.setItem('BandList', JSON.stringify(data)); // Guardar la lista de bandas en localStorage
        this.observablesService.updateOptionList(data); // Actualizar el observable con la lista de bandas
        this.procesListService.startGameCorrector(); // Iniciar el "game corrector"
        this.loading = 'done';
        console.log('data--data', data);
      },
      error: (error) => {
        console.error('Error al enviar la imagen:', error);
      },
    });
  }

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

    // Itero por las opciones en optionList y alimino las que tengan option como parte de su string
    this.optionList = this.optionList.filter((item) => !item.includes(option));

    // Filtro adicional para evitar que opciones similares queden en optionList
    this.optionList = this.optionList.filter((item) => item !== option);
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

  /// --- steps ---

  private handleStepChange(step: number): void {
    switch (step) {
      case 0:
        // valido que el token de Spotify exista
        if (!this.tokenSpotify) {
          console.error('No hay token de Spotify');
          this.step = 0;
          this.requestTokenSpotify = false;
          return;
        }
        break;
      case 1:
        this.loading = 'loading';
        // guardo el valor de postList en listb
        this.listb = this.apiRequestService.postList(
          this.observablesService['bandListCorect$']
        );

        this.listb.subscribe({
          next: (data: any) => {
            console.log('listb-->', this.listb);
            this.bandListCards = data;
            console.log('this.bandList--> ', this.bandListCards);
            this.loading = 'done';
            // actualizo el bandListCorect$
            this.observablesService.updateBandListCorect(this.bandListCards);
          },
          error: (error: any) => {
            console.error('Error al enviar la lista:', error);
          },
        });

        break;
      case 2:
        // Genero la lista de opciones

        break;
      case 3:
        // Genero la playList
        break;
      default:
        console.error('Paso no reconocido:', step);
    }
  }
}
