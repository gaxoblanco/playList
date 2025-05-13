import { CommonModule } from '@angular/common';
import { Component, Input } from '@angular/core';
import { MatButtonModule } from '@angular/material/button';
import { MatCardModule } from '@angular/material/card';
import { MatChipsModule } from '@angular/material/chips';
import { MatFormFieldModule } from '@angular/material/form-field';
import { MatIconModule } from '@angular/material/icon';
import { MatInputModule } from '@angular/material/input';
import { LanguageService } from '../../services/language.service';

@Component({
  standalone: true,
  selector: 'app-playlistinfo',
  templateUrl: './playlistinfo.component.html',
  styleUrls: ['./playlistinfo.component.scss'],
  imports: [
    CommonModule,
    MatCardModule,
    MatChipsModule,
    MatIconModule,
    MatFormFieldModule,
    MatInputModule,
    MatButtonModule,
  ],
})
export class PlaylistinfoComponent {
  @Input() playlistInfo: any;
  @Input() step: number | undefined;
  constructor(
    private languageService: LanguageService,
  ) {
    this.initializeLanguage();
  }
  // Add these variables to your component class
  texts: { [key: string]: any } = {
    en: {
      processInfo: 'Process information',
      bandsAdded: 'Bands:',
      bandsNotAdded: "couldn't be added",
      notFoundTitle: 'Bands that could not been found',
      listenPlaylist: 'Listen to playlist',
      donationText: 'If you found this useful, please consider donating to support the'
    },
    es: {
      processInfo: 'Información del proceso',
      bandsAdded: 'Bandas:',
      bandsNotAdded: 'no pudieron ser añadidas',
      notFoundTitle: 'Bandas que no se pudieron encontrar',
      listenPlaylist: 'Escuchar playlist',
      donationText: 'Si te resultó útil, considera hacer una donación para apoyar el'
    }
  };

  // Add a variable to track the current language
  public currentLang = 'en'; // Default to English

  private initializeLanguage(): void {
    this.languageService.language$.subscribe((language) => {
      this.currentLang = language;
    });
  }
}
