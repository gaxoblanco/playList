import { Component, OnInit } from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { LoadingModel } from '../models/loading';
import { MatIconModule } from '@angular/material/icon';
import { LiveAnnouncer } from '@angular/cdk/a11y';

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
  tokenSpotify: any | undefined;
  requestTokenSpotify: boolean = true;
  bandListCorect: ListBand[] = [];
  selectedName: string = '';

  constructor(
    private procesListService: ProcesListService,
    private apiRequestService: ApiRequestService,
    private observablesService: ObservablesService
  ) {}

  ngOnInit(): void {
    // observo si el optionList$ cambia, y mantengo optionList actualizado
    this.observablesService.optionError$.subscribe((options) => {
      this.optionList = options;
    });
    // valido que tengo un token para Spotify
    this.tokenSpotify = localStorage.getItem('sportify_access_token');
    console.log('tokenSpotify', this.tokenSpotify);

    // clean localStorage
    localStorage.removeItem('uploadedImage');

    // Suscripción al observable nextStep$
    this.observablesService.nextStep$.subscribe((step) => {
      // Dependiendo del valor de step, ejecuta diferentes procesos
      switch (step) {
        case 0:
          // valido que el token de Spotify exista
          if (!this.tokenSpotify) {
            console.error('No hay token de Spotify');
            this.requestTokenSpotify = false;
            return;
          }
          break;
        case 1:
          // envio la lista actualizada con las correciones para obtener el band_id

          // this.bandListCorect = this.observablesService.bandListCorect$;
          console.log(
            'bandListCorect$:',
            this.observablesService['bandListCorect$']
          );
          // Me suscribo al Observable para obtener la respuesta
          console.log(this.apiRequestService.postList(this.bandListCorect));

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
