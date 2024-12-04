import { Component, ChangeDetectorRef, OnInit } from '@angular/core';
import { environment } from '../environments/environment';
import { HeaderService } from './services/header.service';
import { ListBand } from './models/list_band';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent implements OnInit {
  headerText: string = 'SpotyPlayList';
  title = 'spotyPlayList';

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
      img: 'https://via.placeholder.com/150',
      genres: ['Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop'],
    },
    {
      band_id: '2',
      name: 'The Rolling Stones',
      img_zone: [0, 0, 0, 0],
      img: 'https://via.placeholder.com/150',
      genres: ['Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop'],
    },
    {
      band_id: '3',
      name: 'Queen',
      img_zone: [0, 0, 0, 0],
      img: 'https://via.placeholder.com/150',
      genres: ['Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop'],
    },
    {
      band_id: '4',
      name: 'The Doors',
      img_zone: [0, 0, 0, 0],
      img: 'https://via.placeholder.com/150',
      genres: ['Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop', 'Rock', 'Pop'],
    },
  ];
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
