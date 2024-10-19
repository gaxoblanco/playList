import { Component, Input } from '@angular/core';
import { CommonModule } from '@angular/common';
import { optionBand } from 'src/app/models/list_band';
import { MatCardModule } from '@angular/material/card';
import { MatIconModule } from '@angular/material/icon';
import { MatChipsModule } from '@angular/material/chips';

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
  @Input() band!: optionBand;
}
