import { Component, OnInit } from '@angular/core';
import { ActivatedRoute } from '@angular/router';
import { AuthService } from '../services/auth.service';

@Component({
  selector: 'app-auth-callback',
  templateUrl: './auth-callback.component.html',
  styleUrls: ['./auth-callback.component.scss'],
})
export class AuthCallbackComponent implements OnInit {
  constructor(
    private route: ActivatedRoute,
    private authService: AuthService
  ) {}

  ngOnInit(): void {
    // Obtener el access_token y refresh_token de la URL
    this.route.queryParams.subscribe((params) => {
      const accessToken = params['access_token'];
      const refreshToken = params['refresh_token'];
      const code = params['code'];

      if (code) {
        // Almacenar los tokens en el localStorage de manera segura
        // localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
        localStorage.setItem('sportify_access_token', code);
        // console.log('code:', code);

        // Hacer post a la URL http://localhost:5000/callback con el code y obtener el token de Spotify
        this.authService.postCode(code).subscribe({
          next: (data) => {
            console.log(data);
          },
          error: (error) => {
            console.error(error);
          },
        });
      }
    });
  }
}
