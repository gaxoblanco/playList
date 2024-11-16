import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { ListBand, optionBand } from 'src/app/models/list_band';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';
import { take } from 'rxjs/operators';

import { ObservablesService } from 'src/app/services/observables.service';
import { UpImgComponent } from 'src/app/up-img/up-img.component';

@Component({
  selector: 'app-options-list',
  templateUrl: './options-list.component.html',
  styleUrls: ['./options-list.component.scss'],
  standalone: true,
  imports: [
    MatCardModule,
    MatChipsModule,
    MatIconModule,
    CommonModule,
    OptionsListComponent,
  ],
})
export class OptionsListComponent {
  @Input() band!: ListBand;
  @Input() index!: number; // Recibe el índice 'i' desde el padre
  upListByIndex: ListBand[] = [];

  constructor(
    private observablesService: ObservablesService,
    private upImgComponent: UpImgComponent
  ) {}

  changBand(index: number): void {
    console.log('changBand->index:', index);

    const bandListCorectSubject = this.observablesService['bandListCorect$'];
    // Valido que llega el index
    if (index === undefined || index === null) {
      console.error('index is undefined or null');
      return;
    }
    // Validar que this.band no sea undefined o null
    if (this.band) {
      // imprimo el valor de band y index
      // console.log('band:', this.band);
      // console.log('index:', index);

      // guardo la lista actual en una variable temporal
      this.upListByIndex = this.observablesService['bandListCorect'].getValue();
      // actualizo la lista temporal con el valor de this.band segun el index
      this.upListByIndex[index] = this.band;

      // actualizo la lista con la funcion updateBandListCorect
      this.observablesService.updateBandListCorect(this.upListByIndex);
    }
    // imprimo la nueva lista actualizada
    console.log(
      'bandListCorect updated:',
      this.observablesService['bandListCorect'].getValue()
    );
  }
}
