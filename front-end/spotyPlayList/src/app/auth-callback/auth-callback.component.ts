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

  accessToken: any = '';

  ngOnInit(): void {
    // Obtener el access_token y refresh_token de la URL
    this.route.queryParams.subscribe((params) => {
      const refreshToken = params['refresh_token'];
      const code = params['code'];
      if (code) {
        // Almacenar los tokens en el localStorage de manera segura
        // localStorage.setItem('access_token', accessToken);
        localStorage.setItem('refresh_token', refreshToken);
        console.log('code:', code);

        // le paso el authCode a handleCallback que es un observable y devuelve un array
        this.authService.handleCallback(code).subscribe((data) => {
          // actualizo el token en el localStorage
          // console.log('data**:', data.access_token);
          this.authService.setToken(data.access_token);
        });
      }
    });
  }
}
