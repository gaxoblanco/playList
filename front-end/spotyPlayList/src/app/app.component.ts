import { Component } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';
import { AuthService } from './services/auth.service';

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
    window.location.href = 'http://localhost:5000/login';
  }

  // Método que maneja el callback después de la autenticación
  ngOnInit() {
    // this.route.queryParams.subscribe((params) => {
    //   const code = params['code'];
    //   if (code) {
    //     // Si hay un código de autorización, lo usamos para obtener el token
    //     this.authService.handleCallback(code).subscribe(
    //       (response) => {
    //         this.authService.setToken(response.access_token);
    //         this.router.navigate(['/']); // Redirige después de guardar el token
    //       },
    //       (error) => {
    //         console.error('Error al obtener el token', error);
    //       }
    //     );
    //   }
    // });
  }
}
