import {
  Component,
  ChangeDetectorRef,
  OnInit,
  ViewChild,
  ElementRef,
} from '@angular/core';
import { environment } from '../environments/environment';
import { HeaderService } from './services/header.service';
import { ListBand } from './models/list_band';
import { PlaylistDate } from './models/playlist';
import { LanguageService } from './services/language.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  @ViewChild('langBtn') langBtn!: ElementRef;
  @ViewChild('langDropdown') langDropdown!: ElementRef;
  @ViewChild('langText') langText!: ElementRef;
  headerText: string = 'Lineup Playlist';
  // title = 'Lineup Playlist';
  currentLanguage: string = 'en';
  // Textos dinámicos para los botones
  loginText: string = 'Login';
  createPlaylistText: string = 'Create Play List';

  constructor(
    private languageService: LanguageService,
    private headerService: HeaderService,
    private cdr: ChangeDetectorRef
  ) {}

  //  delelet
  bandList: ListBand[] = [
    {
      band_id: '1',
      name: 'The Beatles',
      img_zone: [0, 0, 0, 0],
      img_url: 'https://via.placeholder.com/150',
      genres: ['Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop'],
    },
    {
      band_id: '2',
      name: 'The Rolling Stones',
      img_zone: [0, 0, 0, 0],
      img_url: 'https://via.placeholder.com/150',
      genres: ['Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop'],
    },
    {
      band_id: '3',
      name: 'Queen',
      img_zone: [0, 0, 0, 0],
      img_url: 'https://via.placeholder.com/150',
      genres: ['Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop'],
    },
    {
      band_id: '4',
      name: 'The Doors',
      img_zone: [0, 0, 0, 0],
      img_url: 'https://via.placeholder.com/150',
      genres: ['Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop'],
    },
  ];
  updatePointerPosition(position: number[]): void {
    console.log('Pointer position updated:', position);
  }
  step: number = 3;
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
  ngOnInit() {
    this.textHeader();
    this.languageService.language$.subscribe((language) => {
      this.currentLanguage = language; // Actualiza el idioma actual
      this.cdr.detectChanges(); // Forzar la detección de cambios
      this.updateButtonTexts(language); // Actualiza los textos de los botones según el idioma
    });
  }

  toggleLanguage(): void {
    const newLanguage = this.currentLanguage === 'en' ? 'es' : 'en';
    this.languageService.setLanguage(newLanguage); // Cambia el idioma globalmente
  }
  // funcion login que llama la url http://localhost:5000/login
  login() {
    window.location.href = `${environment.apiUrl}/login`;
  }

  // Función para actualizar la variable headerText con el valor del header
  textHeader() {
    this.headerService.header$.subscribe((header) => {
      this.headerText = header;
      this.cdr.detectChanges(); // Forzar la detección de cambios
    });
  }
  toggleLanguageDropdown(event: Event): void {
    event.stopPropagation();
    const dropdown = this.langDropdown.nativeElement;
    dropdown.classList.toggle('show');
  }

  closeLanguageDropdown(event: Event): void {
    const dropdown = this.langDropdown.nativeElement;
    if (!this.langBtn.nativeElement.contains(event.target)) {
      dropdown.classList.remove('show');
    }
  }
  changeLanguage(lang: string): void {
    this.languageService.setLanguage(lang);
    this.currentLanguage = lang;

    // Cerrar el dropdown después de 3 segundos
    setTimeout(() => {
      const dropdown = this.langDropdown.nativeElement;
      dropdown.classList.remove('show');
    }, 3000);
  }
  private updateButtonTexts(language: string): void {
    if (language === 'en') {
      this.loginText = 'Login';
      this.createPlaylistText = 'Create Play List';
    } else {
      this.loginText = 'Iniciar Sesión';
      this.createPlaylistText = 'Crear Lista de Reproducción';
    }
  }
}
