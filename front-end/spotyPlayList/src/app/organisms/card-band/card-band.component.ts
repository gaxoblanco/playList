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
import { ListBand, optionBand } from 'src/app/models/list_band';
import { ApiRequestService } from 'src/app/services/api-request.service';
import { OptionsListComponent } from 'src/app/molecule/options-list/options-list.component';

@Component({
  selector: 'app-card-band',
  standalone: true,
  templateUrl: './card-band.component.html',
  styleUrls: ['./card-band.component.scss'],
  imports: [
    CommonModule,
    MatCardModule,
    MatChipsModule,
    MatIconModule,
    CommonModule,
    OptionsListComponent,
  ],
})
export class CardBandComponent {
  @Input() bandList: ListBand[] = []; // Se recibe desde el componente padre
  optionsBand: optionBand[] = [
    { name: 'loading', img: 'https://via.placeholder.com/150' },
    { name: 'loading', img: 'https://via.placeholder.com/150' },
    { name: 'loading', img: 'https://via.placeholder.com/150' },
  ];
  activeCardIndex: number | null = null;

  constructor(private apiRequestService: ApiRequestService) {}

  // --- obtener lista de opciones
  getOptions(name: string): void {
    this.apiRequestService.getNameOptions(name).subscribe({
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
      this.getOptions(name); // Llama a getOptions para obtener las opciones
    }
  }
}
