import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from './services/auth.service';
import { environment } from '../environments/environment';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss'],
})
export class AppComponent {
  constructor(
    private router: Router,
    private authService: AuthService,
    private route: ActivatedRoute
  ) {}
  title = 'spotyPlayList';

  // funcion login que llama la url http://localhost:5000/login
  login() {
    window.location.href = `${environment.apiUrl}/login`;
  }

  // Método que maneja el callback después de la autenticación
  ngOnInit() {}
}
