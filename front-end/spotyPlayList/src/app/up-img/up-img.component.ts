import {
  Component,
  ElementRef,
  ChangeDetectorRef,
  ViewChild,
} from '@angular/core';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { LiveAnnouncer } from '@angular/cdk/a11y';
import { FormsModule } from '@angular/forms';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatInputModule } from '@angular/material/input';
import { MatButtonModule } from '@angular/material/button';
import { MatProgressSpinnerModule } from '@angular/material/progress-spinner';
import { LoadingModel } from '../models/loading';

import { ProcesListService } from '../services/proces-list.service';
import { ObservablesService } from '../services/observables.service';
import { ListBand } from '../models/list_band';
import { ApiRequestService } from '../services/api-request.service';
import { CardBandComponent } from '../organisms/card-band/card-band.component';
import { PlaylistDate } from '../models/playlist';
import { environment } from '../../environments/environment';
import { ErrorContainerComponent } from '../organisms/error-container/error-container.component';

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
    ErrorContainerComponent,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatProgressSpinnerModule,
  ],
})
export class UpImgComponent {
  @ViewChild('imgRef') imgRef!: ElementRef<HTMLImageElement>;

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
  selectedName: string = '';

  userBandName: string = '';
  $userBandName: string = '';
  showSuccessMessage: boolean = false;

  listb: any;
  playListName: string = '';
  //-----
  bandListCards: ListBand[] = [];
  // -- circulo
  circleX: number = 0; // Posición X del círculo
  circleY: number = 0; // Posición Y del círculo
  imgWidth!: number;
  imgHeight!: number;
  zoneY: number = 0;
  zoneX: number = 0;
  originalImgWidth: number = 0;
  originalImgHeight: number = 0;

  playlistInfo: PlaylistDate = {
    playlists: {
      band_id: '',
      name: 'LolaPalloza 2024',
      href: '',
      img: [''],
    },
    bandInfo: {
      failed_bands: [
        'ints',
        '2minutos',
        'andres calamaro',
        'ella es tan cargosa',
        'el zak',
      ],
      top_add: 0,
      top_failed: 0,
    },
  };

  constructor(
    private procesListService: ProcesListService,
    private apiRequestService: ApiRequestService,
    private observablesService: ObservablesService
  ) {}

  ngOnInit(): void {
    // valido que tengo un token para Spotify
    this.tokenSpotify = localStorage.getItem('access_token');
    console.log('tokenSpotify', this.tokenSpotify);

    // clean localStorage
    localStorage.removeItem('uploadedImage');

    // Observo si el optionList$ cambia, y mantengo optionList actualizado
    this.observablesService.optionError$.subscribe((options) => {
      this.optionList = options;
      this.adjustBandPositions();
    });

    // Obersvo y voy actualizando el puntero de la img segun la posicion del options
    if (this.imgRef) {
      this.observablesService.ImgPointer$.subscribe((imgPointer) => {
        this.zoneX = imgPointer[0];
        this.zoneY = imgPointer[1];
      });
    }

    // Suscripción al observable nextStep$
    this.observablesService.nextStep$.subscribe((step) => {
      // valido que this.step sea diferente a step
      if (this.step !== step) {
        this.step = step;
        this.handleStepChange(step);
      }
    });
  }

  // Ajustar las posiciones en base a una img ajutada con ratio 1/1
  adjustBandPositions(): void {
    console.log('ajustando posiciones');
    console.log('zoneX', this.zoneX);
    console.log('zoneY', this.zoneY);

    // vlaido que imgRef exista
    if (this.imgRef && this.imgRef.nativeElement) {
      // obtengo las dimenciones de la img original y las guardo en originalImgWidth y originalImgHeight
      this.originalImgWidth = this.imgRef.nativeElement.width;
      this.originalImgHeight = this.imgRef.nativeElement.height;
      // obtengo el ratio de la img original para poder ajustar las posiciones
      const ratioX = this.originalImgWidth / this.imgWidth;
      const ratioY = this.originalImgHeight / this.imgHeight;
      // ajusto las posiciones de las bandas
      this.circleX = this.zoneX * ratioX;
      this.circleY = this.zoneY * ratioY;
    } else {
      console.error('No se ha podido obtener la referencia de la imagen');
    }
  }

  // Método que actualizará la posición del puntero
  updatePointerPosition(positionArray: Array<number>): void {
    if (this.step === 1) {
      // Calcular las posiciones dentro de la imagen referenciada
      // obtengo las dimenciones de la img original y las guardo en originalImgWidth y originalImgHeight
      this.originalImgWidth = this.imgRef.nativeElement.width;
      this.originalImgHeight = this.imgRef.nativeElement.height;
      // obtengo el ratio de la img original para poder ajustar las posiciones
      const ratioX = this.originalImgWidth / this.imgWidth;
      const ratioY = this.originalImgHeight / this.imgHeight;

      // actualizo las posiciones del puntero
      this.circleX = positionArray[0] * ratioX;
      this.circleY = positionArray[1] * ratioY;
    }
  }

  // funcion login que llama la url http://localhost:5000/login
  login() {
    window.location.href = `${environment}/login`;
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    console.log('input-img', input);

    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
      console.log('selectedFile-img', this.selectedFile);

      this.loading = 'loading';

      // almaceno las dimeciones originales
      const img = new Image();
      img.src = URL.createObjectURL(this.selectedFile);
      img.onload = () => {
        this.imgWidth = img.width;
        this.imgHeight = img.height;
        console.log('imgWidth', this.imgWidth);
        console.log('imgHeight', this.imgHeight);
      };

      const reader = new FileReader();
      reader.onload = () => {
        this.imgSelected = reader.result; // Mostrar la imagen en la vista
        localStorage.setItem('uploadedImage', reader.result as string); // Guardar imagen en localStorage
      };
      reader.readAsDataURL(this.selectedFile);
      this.adjustBandPositions();
      // Subir archivo a la API y manejar la respuesta
      this.uploadImageToAPI(this.selectedFile);
    } else {
      console.log('No se ha seleccionado ningún archivo');
    }
  }
  trayAgain(): void {
    this.loading = 'loading';
    if (this.selectedFile) {
      this.uploadImageToAPI(this.selectedFile);
    } else {
      this.loading = 'up';
      this.imgSelected = '';
    }
  }

  // Método para manejar la carga de la imagen a la API y procesar la respuesta
  private uploadImageToAPI(file: File): void {
    const formData = new FormData();
    formData.append('img', file);
    console.log('formData-img', formData);

    this.apiRequestService.postImg(formData).subscribe({
      next: async (data: ListBand[]) => {
        localStorage.setItem('BandList', JSON.stringify(data)); // Guardar la lista de bandas en localStorage
        this.observablesService.updateOptionList(data); // Actualizar el observable con la lista de bandas
        this.procesListService.startGameCorrector(); // Iniciar el "game corrector"
        this.loading = 'done';
        console.log('data--data', data);
        // Ajustar las posiciones de las bandas después de recibir la respuesta de la API
        if (data[0].img_zone) {
          this.zoneX = data[0].img_zone[0] | 0;
          this.zoneY = data[0].img_zone[1] | 0;
        }
      },
      error: (error) => {
        this.loading = 'error';
        console.error('Error al enviar la imagen:', error);
      },
    });
  }
  //----------------------------------------------------------------
  onSubmitUserBandName(): void {
    console.log(' userBandName', this.userBandName);

    const band: ListBand = {
      band_id: '',
      name: this.userBandName,
      img_zone: [this.zoneX, this.zoneY, 0, 0],
    };
    if (this.userBandName != '') {
      // Cargo option en el observable updateBandListCorect
      this.observablesService.addBandListCorect(band);
      // cargar valor
      this.$userBandName = this.userBandName;
      // Mostrar el mensaje de éxito
      this.showSuccessMessage = true;
      // Ocultar el mensaje de éxito después de 3 segundos
      setTimeout(() => {
        this.showSuccessMessage = false;
        // Limpiar el span
        this.userBandName = '';
        this.$userBandName = '';
      }, 2000);
      // Limpiar el campo de entrada después de enviar
      this.userBandName = '';
    }
  }
  //----------------------------------------------------------------
  selectOption(option: string): void {
    this.selectedName = option;
    console.log('Opción seleccion', option);
    // actualizo el puntero
    this.observablesService.ImgPointer$.subscribe((imgPointer) => {
      this.zoneX = imgPointer[0];
      this.zoneY = imgPointer[1];
    });

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
      img_zone: [this.zoneX, this.zoneY, 0, 0],
    };

    // cargo option en el observable updateBandListCorect
    this.observablesService.addBandListCorect(band);
    // Mostrar el mensaje de éxito
    this.$userBandName = band.name;
    this.showSuccessMessage = true;
    // Ocultar el mensaje de éxito después de 3 segundos
    setTimeout(() => {
      this.showSuccessMessage = false;
      // Limpiar el campo de entrada después de enviar
      this.$userBandName = '';
    }, 2000);
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

  createPlayList(): void {
    // activo el spinner
    this.loading = 'loading';
    // valido que tenga algo cargado
    if (this.playListName == '') {
      console.error('No se ha ingresado un nombre para la playlist');
      this.loading = 'error';
      return;
    }
    // valido que bandListCards tenga elementos
    if (this.bandListCards.length === 0) {
      this.loading = 'error';
      console.error('No hay bandas en la lista');
      return;
    }
    // valido que selectedFile no sea null
    if (this.selectedFile === null) {
      this.loading = 'error';
      console.error('No se ha seleccionado un archivo img');
      return;
    }

    console.log('Creando playlist con nombre = ', this.playListName);
    // creo el obj formData
    const formData = new FormData();
    formData.append('img', this.selectedFile);
    console.log('formData-img create play', formData);

    // Le paso a generatePlayList el valor del input playListName
    this.apiRequestService
      .generatePlayList(
        this.playListName,
        this.bandListCards,
        this.selectedFile
      )
      .subscribe({
        next: (data: any) => {
          this.loading = 'done';
          console.log('data', data);
          this.playlistInfo.playlists = data[0];
          this.playlistInfo.bandInfo = data[1];
          this.observablesService.incrementNextStep();
          this.observablesService.incrementNextStep();
          // el valor de la img viene en base64, lo modifico para cargar en el html
          this.playlistInfo.playlists.img = [
            'data:image/jpeg;base64,' + this.playlistInfo.playlists.img[0],
          ];
        },
        error: (error: any) => {
          this.loading = 'error';
          console.error('Error al generar la playlist:', error);
        },
      });
  }

  // --- trayAgainStep1 ---
  trayAgainStep1(): void {
    this.loading = 'loading';
    // vuelvo a enviar la lista con correciones a this.apiRequestService.postList y espero la respeusta
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
        this.loading = 'error';
        console.error('Error al enviar la lista de correciones:', error);
      },
    });
  }
  // --- trayAgainStep2 ---
  trayAgainStep2(): void {
    this.loading = 'loading';
    // Genero la lista de opciones
    this.createPlayList();
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
            this.loading = 'error';
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
