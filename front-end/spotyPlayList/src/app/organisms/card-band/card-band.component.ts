import { Component, Input } from '@angular/core';
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
}
