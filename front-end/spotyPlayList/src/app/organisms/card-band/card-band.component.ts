import { Component, EventEmitter, Input, Output } from '@angular/core';
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
import { FormsModule } from '@angular/forms';

import { ListBand, optionBand } from 'src/app/models/list_band';
import { ApiRequestService } from 'src/app/services/api-request.service';
import { OptionsListComponent } from 'src/app/molecule/options-list/options-list.component';

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
  ],
})
export class CardBandComponent {
  @Input() bandList: ListBand[] = []; // Se recibe desde el componente padre
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
      img: 'https://via.placeholder.com/150',
    },
  ];
  //  posicionamiento del puntero en img con bandList[0].img_zone
  @Output() hoverPosition = new EventEmitter<Array<number>>();
  activeCardIndex: number | null = null;
  editedNames: string = '';

  constructor(private apiRequestService: ApiRequestService) {}

  // --- obtener lista de opciones
  getOptions(name: string): void {
    this.apiRequestService.getNameOptions(name).subscribe({
      // obtener el nombre correcto
      next: (data) => {
        this.optionsBand = data;
        console.log('optionList-->', data);
      },
      error: (error) => {
        console.error('Error al obtener las opciones:', error);
      },
    });
  }
  // --- activar solo en la tarjeta seleccionada
  toggleOptions(index: number, name: string): void {
    if (this.activeCardIndex === index) {
      this.activeCardIndex = null; // Desactiva si se hace clic de nuevo
    } else {
      this.activeCardIndex = index; // Activa la tarjeta seleccionada
      const editedName = this.editedNames || name;
      this.getOptions(editedName); // Llama a getOptions con el nombre editado
      console.log('editetName-->', editedName);
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
    console.log('position index --> ', index);
    console.log('this band list --> ', this.bandList);

    console.log('positionArray-->', positionArray);

    // Emit the position array
    if (Array.isArray(positionArray) && positionArray.length >= 2) {
      this.hoverPosition.emit(positionArray);
    } else {
      console.error('Invalid position array:', positionArray);
    }
  }
}
