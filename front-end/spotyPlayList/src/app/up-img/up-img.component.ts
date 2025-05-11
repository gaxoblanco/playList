import { Component, ElementRef, Renderer2, ViewChild } from '@angular/core';
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
import Cropper from 'cropperjs';

import { LoadingModel } from '../models/loading';
import { ProcesListService } from '../services/proces-list.service';
import { ObservablesService } from '../services/observables.service';
import { ListBand } from '../models/list_band';
import { ApiRequestService } from '../services/api-request.service';
import { CardBandComponent } from '../organisms/card-band/card-band.component';
import { PlaylistDate } from '../models/playlist';
import { environment } from '../../environments/environment';
import { ErrorContainerComponent } from '../organisms/error-container/error-container.component';
import { HeaderService } from '../services/header.service';
import { PlaylistinfoComponent } from '../organisms/playlistinfo/playlistinfo.component';
import { CardBandMobileComponent } from '../organisms/card-band-mobile/card-band-mobile.component';
import { Subject, Subscription, take } from 'rxjs';
import { LanguageService } from '../services/language.service';
import { ImgProcessingService } from '../services/img-processing.service';

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
    CardBandComponent,
    ErrorContainerComponent,
    FormsModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
    MatProgressSpinnerModule,
    PlaylistinfoComponent,
    CardBandMobileComponent,
  ],
})
export class UpImgComponent {
  @ViewChild('imgRef', { static: false }) imgRef!: ElementRef<HTMLImageElement>;
  // ViewChild para el contenedor de imagen
  @ViewChild('upImgContainer', { static: false }) upImgContainer?: ElementRef;

  // Posiciones y dimensiones de la imagen
  boxX: number = 0;
  boxY: number = 0;
  boxX2: number = 0;
  boxY2: number = 0;
  zoneX: number = 0;
  zoneY: number = 0;
  zoneX2: number = 0;
  zoneY2: number = 0;
  originalImgWidth: number = 0;
  originalImgHeight: number = 0;
  colorPointer: string = 'red';

  // Screen size properties
  isMobile: boolean = false;
  breakpointMobile: number = 960; // Breakpoint for mobile (match with your media queries)

  // Información de la playlist
  playlistInfo: PlaylistDate = {
    playlists: {
      band_id: '',
      name: 'Loading...',
      href: '',
      img: [''],
    },
    bandInfo: {
      failed_bands: ['loading...', 'loading...', 'loading...'],
      top_add: 0,
      top_failed: 0,
    },
  };
  playListName: string = '';

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
  //-----
  bandListCards: ListBand[] = [];
  imgWidth!: number;
  imgHeight!: number;

  private cropperInstance: Cropper | null = null;
  cropperEnabled: boolean = false;
  private subscriptions: Subscription[] = []; // guardo las subscripciones para poder desuscribirme
  uploadImageText: string = 'Upload Image';

  constructor(
    private languageService: LanguageService,
    private procesListService: ProcesListService,
    private apiRequestService: ApiRequestService,
    private observablesService: ObservablesService,
    private headerService: HeaderService,
    private renderer: Renderer2,
    private imgProcessingService: ImgProcessingService,
  ) {
    // Check initial screen size
    this.checkScreenSize();
    this.initializeLanguage();
  }
  private initializeLanguage(): void {
    this.languageService.language$.subscribe((language) => {
      this.uploadImageText =
        language === 'en' ? 'Upload Image' : 'Subir Imagen';
    });
  }

  ngOnInit(): void {
    this.initializeHeader();
    this.initializeObservables();
    this.validateSpotifyToken();
    this.clearLocalStorage();

    // escuchamos el evento resize para ajustar el tamaño de la imagen
    window.addEventListener('resize', () => {
      this.checkScreenSize();
    });

    // Subscribe al observable optionError$ para actualizar las opciones
    this.subscriptions.push(
      this.observablesService.optionError$.subscribe((options) => {
        this.optionList = options;
        this.adjustBandPositions();
      })
    );
  }
  ngOnDestroy(): void {
    this.subscriptions.forEach((sub) => sub.unsubscribe());
  }
  checkScreenSize(): void {
    this.isMobile = window.innerWidth < this.breakpointMobile;
  }
  private initializeHeader(): void {
    // valido en que idioma estamos
    this.languageService.language$.subscribe((language) => {
      if (language === 'en') {
        this.headerService.updateHeader(
          'Upload the image of the lineup you want to analyze.'
        );
      } else {
        this.headerService.updateHeader(
          'Sube la imagen del lineup que quieres analizar.'
        );
      }
    });
  }

  private initializeObservables(): void {
    this.observablesService.ImgPointer$.subscribe((imgPointer) => {
      [this.zoneX, this.zoneY, this.zoneX2, this.zoneY2] = imgPointer;
    });

    this.observablesService.nextStep$.subscribe((step) => {
      if (this.step !== step) {
        this.step = step;
        this.handleStepChange(step);
      }
    });
  }

  private validateSpotifyToken(): void {
    this.tokenSpotify = localStorage.getItem('access_token');
    if (this.tokenSpotify) {
      // this.requestTokenSpotify = false;
      console.log('Mensaje de que falta token', this.tokenSpotify);
    }
  }

  private clearLocalStorage(): void {
    localStorage.removeItem('uploadedImage');
  }

  // llevar al servicio para img_processing
  private calculateRatios(): { ratioX: number; ratioY: number } {
    this.originalImgWidth = this.imgRef.nativeElement.width;
    this.originalImgHeight = this.imgRef.nativeElement.height;

    return {
      ratioX: this.originalImgWidth / this.imgWidth,
      ratioY: this.originalImgHeight / this.imgHeight,
    };
  }
  // llevar al servicio para img_processing
  adjustBandPositions(): void {
    if (!this.imgRef?.nativeElement) {
      console.error('No se ha podido obtener la referencia de la imagen');
      return;
    }

    const { ratioX, ratioY } = this.calculateRatios();

    this.boxX = this.zoneX * ratioX - 5;
    this.boxY = this.zoneY * ratioY - 3;
    this.boxX2 = this.zoneX2 * 3 * ratioX;
    this.boxY2 = this.zoneY2 * 3 * ratioY;
  }
  //----------**************-----------------********---------

  // llevar al servicio para img_processing
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
      this.boxX = positionArray[0] * ratioX;
      this.boxY = positionArray[1] * ratioY;
    }
  }

  // funcion login que llama la url http://localhost:5000/login
  login() {
    window.location.href = `${environment}/login`;
  }

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    // console.log('input-img', input);
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];

      // Para mostrar vista previa en la UI
      const reader = new FileReader();
      reader.onload = () => {
        // Solo usar base64 para preview
        this.imgSelected = reader.result as string;

        // Inicializar el Cropper
        this.initializeCropper();
      };
      reader.readAsDataURL(this.selectedFile);
      // considera comprimir antes de guardar
      this.imgProcessingService.compressImage(this.selectedFile).then(compressedBase64 => {
        localStorage.setItem('uploadedImage', compressedBase64);
      });
    } else {
      console.log('No se ha seleccionado ningún archivo');
    }
  }
  // llevar al servicio para img_processing
  initializeCropper(): void {
    console.log('Inicializando cropper...');
    setTimeout(() => {
      if (this.imgRef && this.imgRef.nativeElement) {
        this.cropperInstance = new Cropper(this.imgRef.nativeElement, {
          aspectRatio: NaN, // Proporción de aspecto 1:1
          viewMode: 1, // Vista previa
          autoCropArea: 0.8, // Área de recorte automático al 100%
          crop: (event) => {
            // Actualizar las posiciones del puntero
            this.updatePointerPosition([
              event.detail.x,
              event.detail.y,
              event.detail.width,
              event.detail.height,
            ]);
          },
        });
      } else {
        console.error('El elemento <img> no se encontró en el DOM.');
      }
    }, 0); // Ajusta el tiempo si es necesario
  }
  // llevar al servicio para img_processing
  waitForCrop(): void {
    if (this.cropperInstance) {
      const croppedCanvas = this.cropperInstance.getCroppedCanvas();
      // console.log('Imagen recortada:', croppedCanvas.toDataURL());
      this.imgSelected = croppedCanvas.toDataURL();
      this.uploadImageToAPI(croppedCanvas.toDataURL());
      this.cropperInstance.destroy(); // Finaliza el Cropper
      this.cropperInstance = null; // Limpia la instancia del Cropper

      // alamceno las dimenciones de la nueva img para el puntero
      const img = new Image();
      img.src = this.imgSelected;
      img.onload = () => {
        this.imgWidth = img.width;
        this.imgHeight = img.height;
        // console.log('imgWidth', this.imgWidth);
        // console.log('imgHeight', this.imgHeight);
      };
    } else {
      console.error('El cropper no está inicializado.');
    }
  }

  trayAgain(): void {
    if (this.imgSelected) {
      this.imgSelected = null;
    } else {
      this.loading = 'up';
      this.imgSelected = '';
    }
  }

  // llevar al servicio para img_processing
  // Método para manejar la carga de la imagen a la API y procesar la respuesta
  private uploadImageToAPI(file: string): void {
    this.loading = 'loading';
    const formData = new FormData();
    formData.append('img', file);

    this.apiRequestService.postImg(formData).subscribe({
      next: async (data: any) => {
        try {
          // Verificar si la respuesta contiene un error 202
          if (data && data.error === 202) {
            console.error('Error 202:', data.message);
            this.loading = 'error';
            // Mostrar mensaje de error al usuario
            this.currentErrors = [data.message];
            return;
          }

          // Verificar que data tenga la estructura esperada
          if (!data || !data.associated_data) {
            console.error('Respuesta de API inválida:', data);
            this.loading = 'error';
            return;
          }

          // Guardar la lista de bandas en localStorage y en el servicio
          const bandList: ListBand[] = data.associated_data;
          this.colorPointer = data.contrast_color || 'red';

          localStorage.setItem('BandList', JSON.stringify(bandList));
          this.observablesService.updateOptionList(bandList);
          this.procesListService.startGameCorrector();
          this.loading = 'done';

          // valido el idioma y actualizo el this.headerService.updateHeader
          this.languageService.language$.subscribe((language) => {
            if (language === 'en') {
              this.headerService.updateHeader(
                'The text recognition may be wrong, we believe these names are misspelled.'
              );
            } else {
              this.headerService.updateHeader(
                'El reconocimiento de texto se puede equivocar, creemos que estos nombres están mal escritos.'
              );
            }
          });

          // Usar take(1) para evitar múltiples suscripciones
          this.observablesService.optionError$
            .pipe(
              // no requiere guardar referencia a la subscripción
              take(1)
            )
            .subscribe((options) => {
              this.optionList = options;
              this.adjustBandPositions();
              // Auto-cancela
            });

          // Posicionar el puntero en la primera banda
          if (bandList && bandList.length > 0 && bandList[0].img_zone) {
            this.zoneX = bandList[0].img_zone[0] | 0;
            this.zoneY = bandList[0].img_zone[1] | 0;
            this.zoneX2 = bandList[0].img_zone[2] | 0;
            this.zoneY2 = bandList[0].img_zone[3] | 0;
          }
        } catch (error) {
          console.error('Error procesando datos:', error);
          this.loading = 'error';
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
    // console.log(' userBandName', this.userBandName);

    const band: ListBand = {
      band_id: '',
      name: this.userBandName,
      img_zone: [this.zoneX, this.zoneY, this.zoneX2, this.zoneY2],
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
  //-------------------------- Crear su componente --------------------------------------
  selectOption(option: string): void {
    this.selectedName = option;
    // console.log('Opción seleccion', option);
    // actualizo el puntero
    this.observablesService.ImgPointer$.subscribe((imgPointer) => {
      this.zoneX = imgPointer[0];
      this.zoneY = imgPointer[1];
      this.zoneX2 = imgPointer[2];
      this.zoneY2 = imgPointer[3];
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
      img_zone: [this.zoneX, this.zoneY, this.zoneX2, this.zoneY2],
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
  //                   ------- Va con el nuevo componente ---------
  // Función para esperar a que el usuario haga clic en "continuar"
  async waitForUserConfirmation(): Promise<void> {
    console.log('Esperando a que el usuario haga clic en "continuar"');
    this.observablesService.emitShowContinueButton();
    return new Promise<void>((resolve) => {
      const button = document.getElementById('continue-button');
      if (button) {
        button.addEventListener(
          'click',
          () => {
            resolve();
          },
          { once: true }
        ); // 'once: true' para que el listener se elimine después de usarse
      } else {
        console.error('Button "continue-button" not found - agregar contador');
        // Timeout para evitar que se quede colgada para siempre
        setTimeout(resolve, 10000); // Ejemplo: resolver después de 10 segundos
      }
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
    // Actualizo headerService con la informacion del paso a realizar
    this.headerService.updateHeader(
      `Creating playlist ${this.playListName}, this can take a time.`
    );

    console.log('Creando playlist con nombre = ', this.playListName);
    // creo el obj formData
    const formData = new FormData();
    formData.append('img', this.selectedFile);
    // console.log('formData-img create play', formData);

    // Obtener la imagen comprimida del localStorage
    const uploadedImageBase64 = localStorage.getItem('uploadedImage');

    if (uploadedImageBase64) {
      // Convertir base64 a File
      this.selectedFile = this.imgProcessingService.base64ToFile(uploadedImageBase64, 'playlist_image.jpg');
    }
    console.log('this.bandListCards', this.bandListCards);
    console.log("quiza this.observablesService", this.observablesService['bandListCorect$']);


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
          this.playlistInfo.playlists = data[0];
          this.playlistInfo.bandInfo = data[1];
          this.observablesService.incrementNextStep();
          this.observablesService.incrementNextStep();
          // el valor de la img viene en base64, lo modifico para cargar en el html
          this.playlistInfo.playlists.img = [
            'data:image/jpeg;base64,' + this.playlistInfo.playlists.img[0],
          ];
          // Actualizo headerService con la informacion del paso a realizar
          this.headerService.updateHeader(
            `Check the final summary and consider supporting the project with a donation.`
          );
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
        this.bandListCards = data;
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
        // Actualizo el estado de carga
        this.loading = 'loading';

        // Utilizo takeUntil
        this.languageService.language$.pipe(take(1)).subscribe((language) => {
          const headerText =
            language === 'en'
              ? 'Loading the next step'
              : 'Cargando el siguiente paso';
          this.headerService.updateHeader(headerText);
        });

        // guardo el valor de postList en listb ------
        this.listb = this.apiRequestService.postList(
          this.observablesService['bandListCorect$']
        );
        // console.log('quitando img-container--selected');

        // le agrego styles min-height-0px a up_img_container
        if (this.upImgContainer) {
          this.renderer.setStyle(
            this.upImgContainer.nativeElement,
            'min-height',
            '0px'
          );
        }
        this.listb.subscribe({
          next: (data: any) => {
            this.bandListCards = data;
            console.log('bandListCards', this.bandListCards);

            this.loading = 'done';
            // Actualizo headerService con la informacion del paso a realizar
            this.headerService.updateHeader(
              'Adjust the final list by removing or editing bands according to your preferences. \n Enter the name of your playlist and click "Create."'
            );
            this.languageService.language$.subscribe((language) => {
              if (language === 'en') {
                this.headerService.updateHeader(
                  'Adjust the final list by removing or editing bands according to your preferences. \n Enter the name of your playlist and click "Create.'
                );
              } else {
                this.headerService.updateHeader(
                  'Ajusta la lista final eliminando o editando bandas según tus preferencias. \n Ingresa el nombre de tu playlist y haz clic en "Crear.'
                );
              }
            });
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
        // Actualizo el header para invitar al usuario a disfrutar de la música y generar una donación
        this.languageService.language$.subscribe((language) => {
          if (language === 'en') {
            this.headerService.updateHeader(
              'Enjoy the music and consider supporting the project with a donation.'
            );
          } else {
            this.headerService.updateHeader(
              'Disfruta de la música y considera apoyar el proyecto con una donación.'
            );
          }
        });
        break;
      default:
        console.error('Paso no reconocido:', step);
    }
  }

  resetImageAndOpenFileDialog(): void {
    // Resetear el estado
    this.imgSelected = null;
    this.selectedFile = null;
    this.currentErrors = [];

    // Si tienes una instancia de cropper activa, destrúyela
    if (this.cropperInstance) {
      this.cropperInstance.destroy();
      this.cropperInstance = null;
    }

    // Usa setTimeout para permitir que ngIf se actualice primero
    setTimeout(() => {
      // Abre el diálogo de selección de archivo programáticamente
      const fileInput = document.getElementById(
        'file-upload'
      ) as HTMLInputElement;
      if (fileInput) {
        fileInput.click();
      }
    }, 0);
  }
}
