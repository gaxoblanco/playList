import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { Observable } from 'rxjs';
import { Router } from '@angular/router';

@Injectable({
  providedIn: 'root',
})
export class AuthService {
  private authUrl = 'http://localhost:5000'; // URL de tu backend Flask
  private accessToken: string | null = null;

  constructor(private http: HttpClient, private router: Router) {}

  // Guardar el accessToken en el LocalStorage o en memoria
  public setToken(token: string): void {
    this.accessToken = token;
    localStorage.setItem('access_token', token); // O usar sessionStorage
  }

  // Obtener el token
  public getToken(): string | null {
    return this.accessToken || localStorage.getItem('access_token');
  }

  // Iniciar el proceso de autenticación
  public login(): void {
    window.location.href = `${this.authUrl}/login`;
  }

  // Obtener el token desde el back-end
  public handleCallback(authCode: string): Observable<any> {
    const body = { code: authCode };

    return this.http.post(`${this.authUrl}/callback`, body);
  }

  // Cerrar sesión
  public logout(): void {
    this.accessToken = null;
    localStorage.removeItem('access_token');
    this.router.navigate(['/']);
  }

  // Obtengo el token de acceso
  postCode(code: string): Observable<any> {
    const headers = new HttpHeaders({
      'Content-Type': 'application/json',
      code: code,
    });

    return this.http.post<any>(
      `${this.authUrl}/callback`,
      { code },
      { headers }
    );
  }
}
