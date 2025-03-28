import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { environment } from '../environments/environment';
import { HeaderService } from './services/header.service';
import { ListBand } from './models/list_band';
import { PlaylistDate } from './models/playlist';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  headerText: string = 'Lineup Playlist';
  title = 'Lineup Playlist';

  constructor(
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
  step: number = 3;
  playlistInfo: PlaylistDate = {
      playlists: {
        band_id: '',
        name: 'Loading...',
        href: '',
        img: [''],
      },
      bandInfo: {
        failed_bands: [
          'loading...',
          'loading...',
          'loading...',
        ],
        top_add: 0,
        top_failed: 0,
      },
    };
  wor() {
    console.log('holas');
  }
  // funcion login que llama la url http://localhost:5000/login
  login() {
    window.location.href = `${environment.apiUrl}/login`;
  }

  // Método que maneja el callback después de la autenticación
  ngOnInit() {
    this.textHeader();
  }

  // Función para actualizar la variable headerText con el valor del header
  textHeader() {
    this.headerService.header$.subscribe((header) => {
      this.headerText = header;
      this.cdr.detectChanges(); // Forzar la detección de cambios
    });
  }
}
