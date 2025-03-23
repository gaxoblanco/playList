import { animate, state, style, transition, trigger } from '@angular/animations';
import { CommonModule } from '@angular/common';
import { HttpClient } from '@angular/common/http';
import { Component, ElementRef, EventEmitter, HostListener, Input, Output, QueryList, ViewChildren } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import { Subscription } from 'rxjs';
import { MobileClickDirective } from 'src/app/directive/mobile-click.directive';
import { ListBand, ListBandEdit } from 'src/app/models/list_band';
import { OptionsListComponent } from 'src/app/molecule/options-list/options-list.component';
import { ApiRequestService } from 'src/app/services/api-request.service';
import { ObservablesService } from 'src/app/services/observables.service';

@Component({
  selector: 'app-card-band-mobile',
  standalone: true, // Permite declarar el componente de manera independiente.
  templateUrl: './card-band-mobile.component.html',
  styleUrls: ['./card-band-mobile.component.scss'],
  animations: [
      trigger('toggleOptions', [
        state(
          'void',
          style({
            opacity: 0,
            transform: 'translateY(-10px)',
          })
        ),
        state(
          '*',
          style({
            opacity: 1,
            transform: 'translateY(0)',
          })
        ),
        transition('void <=> *', [animate('300ms ease-in-out')]),
      ]),
    ],
    imports: [
      CommonModule,
      MatCardModule,
      MatChipsModule,
      MatIconModule,
      CommonModule,
      OptionsListComponent,
      FormsModule,
      MobileClickDirective,
    ],
})
export class CardBandMobileComponent {
  @Input() bandList: ListBandEdit[] = []; // Se recibe desde el componente padre
  //  posicionamiento del puntero en img con bandList[0].img_zone
  @Output() hoverPosition = new EventEmitter<Array<number>>();
  @ViewChildren('bandCard') bandCards!: QueryList<ElementRef>;
  optionsBand: ListBand[] = [];
  loadinOptionsBand: ListBand[] = [
    // 1 cargando
    {
      band_id: '1',
      name: 'Cargando...',
      top_tracks: [
        {
          name: 'Cargando...',
          url: 'Cargando...',
        },
      ],
      genres: ['Cargando...'],
      img_zone: [0, 0, 0, 0],
      img_url: 'https://via.placeholder.com/150',
    },
    // 2 cargando
    {
      band_id: '2',
      name: 'Cargando...',
      top_tracks: [
        {
          name: 'Cargando...',
          url: 'Cargando...',
        },
      ],
      genres: ['Cargando...'],
      img_zone: [0, 0, 0, 0],
      img_url: 'https://via.placeholder.com/150',
    },
    // 3 cargando
    {
      band_id: '3',
      name: 'Cargando...',
      top_tracks: [
        {
          name: 'Cargando...',
          url: 'Cargando...',
        },
      ],
      img_zone: [0, 0, 0, 0],
      genres: ['Cargando...'],
      img_url: 'https://via.placeholder.com/150',
    },
  ];

  editedNames: string[] = [];
  // 5 new options
  activeCardIndex: number | null = null;
  isHovered: boolean = false;
  timeoutId: any;
  activeElement: boolean = false;
  // add new band
  addBand: ListBand = {
    band_id: '0',
    name: 'Add band',
    genres: ['Add extra band for your Play List'],
    img_zone: [0, 0, 0, 0],
    img_url: '../../../assets/addBand.jpg',
  };
  addBandHtml: string = '';

  // Propiedad para detectar si estamos en desktop
  isDesktop: boolean = false;
  // Para manejar suscripciones
  private subscription = new Subscription();
  constructor(
    private apiRequestService: ApiRequestService,
    private http: HttpClient,
    private observablesService: ObservablesService
  ) {}

  ngOnInit(): void {
    // cargo las opcionmes de loadin optionsBand
    this.optionsBand = this.loadinOptionsBand;
    // Detecta el tamaño de pantalla inicial
    this.checkScreenSize();
    // una vez cargado bandList en el ultimo elemento le agrego , elemento mas
    this.http
      .get('assets/addBand.jpg', { responseType: 'text' })
      .subscribe((data) => {
        this.addBandHtml = data;
      });
    if (this.bandList.length > 0) {
      const lastBand = this.bandList[this.bandList.length - 1];
      this.addBand.img_zone = lastBand.img_zone;
      this.bandList.push(this.addBand);
    }
    // this.subscription.add(
    //   this.observablesService.bandSelected$.subscribe(selectedIndex => {
    //     if (selectedIndex !== null) {
    //       // Cerrar el panel de opciones
    //       this.activeCardIndex = null;
    //       // Opcional: limpiar la selección para futuros eventos
    //       setTimeout(() => {
    //         // Usamos setTimeout para evitar el error ExpressionChangedAfterItHasBeenChecked
    //         this.observablesService.notifyBandSelected(null);
    //       });
    //     }
    //   })
    // );
  }
    // Importante: Limpiar la suscripción cuando el componente se destruya
    ngOnDestroy(): void {
      if (this.subscription) {
        this.subscription.unsubscribe();
      }
    }

  // Detector de tamaño de pantalla
  @HostListener('window:resize', ['$event'])
  checkScreenSize() {
    this.isDesktop = window.innerWidth >= 769; // El mismo breakpoint del CSS
  }

  // --- obtener lista de opciones
  getOptions(name: string, img_zone: [number, number, number, number]): void {
    // cargo el array de loading
    this.optionsBand = this.loadinOptionsBand;
    this.apiRequestService.getNameOptions(name).subscribe({
      // obtener el nombre correcto
      // next: (response) => {
      //   console.log('Respuesta de API:', response); // Para depuración

      //   try {
      //     // Intentar determinar el tipo de respuesta y procesarla adecuadamente
      //     let processedData: ListBand[] = [];

      //     if (response === null || response === undefined) {
      //       // La respuesta es null o undefined
      //       throw new Error('La respuesta de la API es null o undefined');
      //     }

      //     if (Array.isArray(response)) {
      //       // La respuesta ya es un array
      //       processedData = response;
      //     } else if (typeof response === 'object') {
      //       // La respuesta es un objeto, intentar extraer el array
      //       // Esto depende de la estructura exacta de tu respuesta
      //       const possibleArrays = Object.values(response).filter(val => Array.isArray(val));

      //       if (possibleArrays.length > 0) {
      //         // Usa el primer array encontrado
      //         processedData = possibleArrays[0] as ListBand[];
      //       } else {
      //         // Intenta convertir el objeto en un array si tiene una estructura compatible
      //         if (response && typeof response === 'object' && 'band_id' in response) {
      //           // Si parece ser un solo elemento de ListBand
      //           processedData = [response as ListBand];
      //         } else {
      //           throw new Error('No se pudo extraer un array de la respuesta');
      //         }
      //       }
      //     } else {
      //       throw new Error(`Respuesta inesperada de tipo: ${typeof response}`);
      //     }

      //     // Ahora es seguro procesar los datos
      //     if (processedData.length > 0) {
      //       processedData.forEach(element => {
      //         element.img_zone = img_zone;
      //       });
      //       this.optionsBand = processedData;
      //     } else {
      //       // Array vacío
      //       this.optionsBand = [{
      //         band_id: '0',
      //         name: 'No se encontraron opciones',
      //         genres: ['Intenta con otro nombre'],
      //         img_zone: img_zone,
      //         img_url: 'https://via.placeholder.com/150',
      //       }];
      //     }

      //   } catch (error) {
      //     console.error('Error procesando la respuesta:', error);
      //     this.optionsBand = [{
      //       band_id: '0',
      //       name: 'Error de formato en respuesta',
      //       genres: ['Intenta con otro nombre'],
      //       img_zone: img_zone,
      //       img_url: 'https://via.placeholder.com/150',
      //     }];
      //   }
      // },
      // error: (error) => {
      //   console.error('Error al obtener las opciones:', error);
      //   // En caso de error, mostrar mensaje amigable
      //   this.optionsBand = [{
      //     band_id: '0',
      //     name: 'Error al cargar opciones',
      //     genres: ['Intenta nuevamente'],
      //     img_zone: img_zone,
      //     img_url: 'https://via.placeholder.com/150',
      //   }];
      // },
    });
  }
  // --- activar solo en la tarjeta seleccionada
  toggleOptions(
    index: number,
    name: string,
    img_zone: [number, number, number, number]
  ): void {
    const safeImgZone: [number, number, number, number] = img_zone ?? [
      0, 0, 0, 0,
    ];

    if (this.activeCardIndex === index) {
      this.activeCardIndex = null; // Desactiva si se hace clic de nuevo
    } else {
      this.activeCardIndex = index; // Activa la tarjeta seleccionada
      const editedName = this.editedNames || name;
      this.getOptions(editedName[index], safeImgZone); // Llama a getOptions con el nombre editado
      console.log('editetName-->', editedName);
      // limpio el formulario
      this.editedNames[index] = '';
      this.startTimeout();
    }
  }

  // --- Borrar la opción seleccionada
  deleteOpcion(index: number): void {
    // Si estamos en modo edición para esta banda, salimos primero
    if (this.bandList[index].isEditing) {
      this.bandList[index].isEditing = false;
    }
    // valido que bandList tenga elementos y no sea el botón de añadir
    if (this.bandList.length > 0 && !(index === this.bandList.length - 1 && this.bandList[index].name === 'Add band')) {
      this.bandList.splice(index, 1);

      // Si se borra la banda activa, cerramos el panel de opciones
      if (this.activeCardIndex === index) {
        this.activeCardIndex = null;
      } else if (this.activeCardIndex !== null && this.activeCardIndex > index) {
        // Ajustamos el índice activo si se elimina una banda anterior
        this.activeCardIndex--;
      }
    }
  }
  // --- editar la posicion del puntero al hacer hover sobre la card
  onCardHover(index: number, event: MouseEvent): void {
    const hoverElement = this.bandList[index];
    const positionArray = hoverElement.img_zone; // Assuming this is the array
    // Emit the position array
    if (Array.isArray(positionArray) && positionArray.length >= 2) {
      this.hoverPosition.emit(positionArray);
    } else {
      console.error('Invalid position array:', positionArray);
    }
      // Para desktop, podemos mostrar los botones de acción al hacer hover
    if (this.isDesktop && this.activeCardIndex !== index) {
      // Activar el hover solo para mostrar las acciones, no para abrir opciones
      // Puedes usar una propiedad separada si no quieres afectar activeCardIndex
      // O simplemente cambiar el CSS para que muestre las acciones en hover
    }
  }

  saludo(
    i: number,
    name: string,
    img_zone: [number, number, number, number]
  ): void {
    // Emitir la posición para la imagen
    const positionArray = img_zone;
    if (Array.isArray(positionArray) && positionArray.length >= 2) {
      this.hoverPosition.emit(positionArray);
    } else {
      console.error('Invalid position array:', positionArray);
    }

    const cardElement = document.querySelector(`.band-card-${i}`);

    // Si ya está activa, la desactivamos
    if (this.activeCardIndex === i) {
      this.activeCardIndex = null;
      cardElement?.classList.remove('active');
      return;
    }

    // Desactivar la tarjeta anteriormente activa
    if (this.activeCardIndex !== null) {
      const previousCardElement = document.querySelector(
        `.band-card-${this.activeCardIndex}`
      );
      previousCardElement?.classList.remove('active');
    }

    // Activar la nueva tarjeta
    this.activeCardIndex = i;
    cardElement?.classList.add('active');

    // Cargar opciones
    this.getOptions(name, img_zone);

    // Comportamiento específico según dispositivo
    if (this.isDesktop) {
      // En escritorio: mostrar header y opciones
      // Mostrar el header con los controles de edición
      const headerElement = cardElement?.querySelector('.band-card--header');
      if (headerElement) {
        headerElement.classList.add('visible');
      }

      // Enfoca el input solo si estamos en escritorio
      setTimeout(() => {
        const input = cardElement?.querySelector('.band-name-input') as HTMLInputElement;
        if (input) {
          input.focus();
          this.editedNames[i] = name; // Inicializar con el nombre actual
        }
      });
    } else {
      // En móvil: solo mostrar las opciones de bandas, .band-card--header displey none
      const headerElement = cardElement?.querySelector('.band-card--header');
      if (headerElement) {
        headerElement.classList.remove('visible');
      }

    }
  }

  getSaludoFunction(i: number): () => void {
    return () => {
      // Si estamos en modo edición, no hacemos nada
      if (this.bandList[i].isEditing) {
        return;
      }
      // En móvil, mantener el comportamiento actual
      if (!this.isDesktop) {
        this.saludo(i, this.bandList[i].name, this.bandList[i].img_zone);
        this.scrollToActiveCard(i);
      } else {
        // En desktop, solo toggleEdit si es un clic explícito en el botón de edición
        // (no hacemos nada aquí, ya que en desktop los botones estarán visibles)
      }
    };
  }
  scrollToActiveCard(i: number): void {
    if (this.bandCards && this.bandCards.length > i) {
      const activeCard = this.bandCards.toArray()[i]?.nativeElement;
      if (activeCard) {
        activeCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
      }
    }
  }
  //----------------------------------------------------------------
  // Método para manejar el hover
  @HostListener('mouseenter', ['$event'])
  onMouseEnter() {
    this.isHovered = true;
    // console.log('hover');

    if (this.timeoutId) {
      clearTimeout(this.timeoutId);
    }
  }

  onMouseLeave() {
    this.isHovered = false;
    this.startTimeout();
  }

  startTimeout() {
    this.timeoutId = setTimeout(() => {
      if (!this.isHovered) {
        this.activeCardIndex = null; // Ocultar el componente
      }
    }, 2500); // 2000 ms
  }

  toggleEdit(index: number): void {
    // Ignorar el botón "Add band"
    if (index === this.bandList.length - 1 && this.bandList[index].name === 'Add band') {
      return;
    }

    // Activar el modo edición y preparar el nombre editable
    this.bandList[index].isEditing = true;
    this.bandList[index].editedName = this.bandList[index].name;

    // Enfoca el input después de que Angular actualice la vista
    setTimeout(() => {
      const input = document.querySelector(
        `.band-card-${index} .band-name-input`
      ) as HTMLInputElement;
      if (input) {
        input.focus();
        input.select(); // Selecciona todo el texto para facilitar la edición
      }
    });
  }
  // Para guardar los cambios de la edición
  saveEdit(index: number, editedName: string): void {
    if (editedName && editedName.trim() !== '') {
      this.bandList[index].name = editedName.trim();

      // Actualizar opciones si es necesario
      if (this.activeCardIndex === index) {
        this.getOptions(this.bandList[index].name, this.bandList[index].img_zone);
      }
    }

    // Limpiar y desactivar edición
    this.editedNames[index] = '';
  }

  // Variable para almacenar los timers de actualización para cada banda
  private updateTimers: { [key: number]: any } = {};

  // Método para gestionar la edición con actualización automática
  onEditInput(index: number): void {
    const  nameSearch : String = this.editedNames[index];
    // Limpiar cualquier timer existente para esta banda
    if (this.updateTimers[index]) {
      clearTimeout(this.updateTimers[index]);
    }
    // Configurar un nuevo timer que se activará después de 800ms de inactividad
    this.updateTimers[index] = setTimeout(() => {
      // Solo actualizar si el valor de editedNames ha cambiado y no está vacío, y this.getOptions
      if (nameSearch && nameSearch.trim() !== '' &&
      nameSearch.trim() !== this.bandList[index].name) {
        console.log(`Actualizando opciones para "${this.editedNames}"`);
        this.getOptions(nameSearch.trim(), this.bandList[index].img_zone);
      }
    }, 800); // 800ms es el tiempo de espera - ajústalo según necesites
  }
}
