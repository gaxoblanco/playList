import { Component, OnInit } from '@angular/core';
import { ActivatedRoute, Router } from '@angular/router';

@Component({
  selector: 'app-auth-callback',
  templateUrl: './auth-callback.component.html',
  styleUrls: ['./auth-callback.component.scss'],
})
export class AuthCallbackComponent implements OnInit {
  constructor(private route: ActivatedRoute, private router: Router) {}

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
        localStorage.setItem('code', code);
        // console.log('code:', code);

        // hago post a la url http://localhost:5000/collback con el code y obtengo el token de spotify
        fetch('http://localhost:5000/callback', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            code: code,
          },
          // body: JSON.stringify({ code }),
        })
          .then((response) => response.json())
          .then((data) => {
            // console.log('Success:', data);
            localStorage.setItem('access_token', data.access_token);
          })
          .catch((error) => {
            console.error('Error:', error);
          });

        // Redirigir al home o donde prefieras después de guardar el token
        this.router.navigate(['/']);
      } else {
        // Manejo de error en caso de no obtener los tokens
        console.error('Error al obtener tokens de Spotify');
      }
    });
  }
}
