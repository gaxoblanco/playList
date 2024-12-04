import {
  Component,
  ElementRef,
  EventEmitter,
  HostListener,
  Input,
  Output,
  QueryList,
  ViewChild,
  ViewChildren,
} from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { CommonModule } from '@angular/common';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatIconModule } from '@angular/material/icon';
import {
  trigger,
  state,
  style,
  transition,
  animate,
} from '@angular/animations';
import { FormsModule } from '@angular/forms';

import { ListBand, optionBand } from 'src/app/models/list_band';
import { ApiRequestService } from 'src/app/services/api-request.service';
import { OptionsListComponent } from 'src/app/molecule/options-list/options-list.component';
import { MobileClickDirective } from 'src/app/directive/mobile-click.directive';

@Component({
  selector: 'app-card-band',
  standalone: true,
  templateUrl: './card-band.component.html',
  styleUrls: ['./card-band.component.scss'],
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
export class CardBandComponent {
  @Input() bandList: ListBand[] = []; // Se recibe desde el componente padre
  //  posicionamiento del puntero en img con bandList[0].img_zone
  @Output() hoverPosition = new EventEmitter<Array<number>>();
  @ViewChild('bandListOptions', { static: false }) bandListOptions!: ElementRef;
  @ViewChildren('bandCard') bandCards!: QueryList<ElementRef>;
  optionsBand: ListBand[] = [
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
      img: 'https://via.placeholder.com/150',
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
      img: 'https://via.placeholder.com/150',
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
      img: 'https://via.placeholder.com/150',
    },
  ];

  editedNames: string = '';
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
    img: '../../../assets/addBand.jpg',
  };
  addBandHtml: string = '';
  constructor(
    private apiRequestService: ApiRequestService,
    private http: HttpClient
  ) {}

  ngOnInit(): void {
    // una vez cargado bandList en el ultimo elemento le agrego , elemento mas
    this.http
      .get('assets/addBand.html', { responseType: 'text' })
      .subscribe((data) => {
        this.addBandHtml = data;
      });
    if (this.bandList.length > 0) {
      const lastBand = this.bandList[this.bandList.length - 1];
      this.addBand.img_zone = lastBand.img_zone;
      this.bandList.push(this.addBand);
    }
  }

  // --- obtener lista de opciones
  getOptions(name: string, img_zone: [number, number, number, number]): void {
    this.apiRequestService.getNameOptions(name).subscribe({
      // obtener el nombre correcto
      next: (data) => {
        // agrego img_zone a cada elemento de la lista
        data.forEach((element: ListBand) => {
          element.img_zone = img_zone;
        });
        this.optionsBand = data;
        console.log('optionList-->', data);
      },
      error: (error) => {
        console.error('Error al obtener las opciones:', error);
      },
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
      this.getOptions(editedName, safeImgZone); // Llama a getOptions con el nombre editado
      console.log('editetName-->', editedName);
      // limpio el formulario
      this.editedNames = '';
      this.startTimeout();
    }
  }

  // --- Borrar la opción seleccionada
  deleteOpcion(index: number): void {
    // valido que bandList tenga elementos
    if (this.bandList.length > 0) {
      this.bandList.splice(index, 1);
    }
  }
  // --- editar la posicion del puntero al hacer hover sobre la card
  onCardHover(index: number, event: MouseEvent): void {
    const hoverElement = this.bandList[index];
    const positionArray = hoverElement.img_zone; // Assuming this is the array
    // console.log('position index --> ', index);
    // console.log('this band list --> ', this.bandList);

    // console.log('positionArray-->', positionArray);

    // Emit the position array
    if (Array.isArray(positionArray) && positionArray.length >= 2) {
      this.hoverPosition.emit(positionArray);
    } else {
      console.error('Invalid position array:', positionArray);
    }
  }

  saludo(
    i: number,
    name: string,
    img_zone: [number, number, number, number]
  ): void {
    console.log(`Saludo ${i}`);
    const positionArray = img_zone;
    // Emit the position array
    if (Array.isArray(positionArray) && positionArray.length >= 2) {
      this.hoverPosition.emit(positionArray);
    } else {
      console.error('Invalid position array:', positionArray);
    }

    const cardElement = document.querySelector(`.band-card-${i}`);
    if (this.activeCardIndex === i) {
      this.activeCardIndex = null; // Desactiva si se hace clic de nuevo
      cardElement?.classList.remove('active');
    } else {
      if (this.activeCardIndex !== null) {
        const previousCardElement = document.querySelector(
          `.band-card-${this.activeCardIndex}`
        );
        previousCardElement?.classList.remove('active');
      }
      this.activeCardIndex = i; // Activa la tarjeta seleccionada
      cardElement?.classList.add('active');
      const editedName = name;
      this.getOptions(editedName, img_zone); // Llama a getOptions con el nombre editado
      console.log('editetName-->', editedName);
      // limpio el formulario
      this.editedNames = '';
      // Enfoca el input en el siguiente ciclo de detección
      setTimeout(() => {
        const input = document.querySelector(
          `.band-card-${i} .band-name-input`
        ) as HTMLInputElement;
        if (input) {
          input.focus();
        }
      });
    }
  }

  getSaludoFunction(i: number): () => void {
    return () => {
      this.saludo(i, this.bandList[i].name, this.bandList[i].img_zone);
      this.scrollToActiveCard(i);
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
    console.log('hover');

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
  // Maneja el evento wheel para desplazamiento lateral
  onWheel(event: WheelEvent) {
    if (this.isHovered && this.bandListOptions) {
      const element = this.bandListOptions.nativeElement as HTMLElement;

      // Desplazamiento suave
      element.scrollBy({
        left: event.deltaY, // Ajusta la dirección del desplazamiento
        behavior: 'smooth', // Hace que el movimiento sea suave
      });

      // Previene el comportamiento predeterminado del scroll vertical
      event.preventDefault();
    }
  }
}
