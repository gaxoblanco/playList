import { Injectable } from '@angular/core';
import { HttpClient, HttpHeaders } from '@angular/common/http';
import { CookieService } from 'ngx-cookie-service';
import { Observable } from 'rxjs';
import { ObservablesService } from './observables.service';
import { AuthService } from './auth.service';

@Injectable({
  providedIn: 'root',
})
export class ApiRequestService {
  private apiUrl = 'http://localhost:5000';
  constructor(
    private http: HttpClient,
    private cookieService: CookieService,
    private observablesService: ObservablesService,
    private authService: AuthService
  ) {}

  //convierto el access_token del localStorage en un string
  spotify_token: string = this.authService.getToken() || '';
  headers = new HttpHeaders({
    Authorization: this.spotify_token,
  });

  // Envio la img y obtengo el json
  postImg(img: FormData): Observable<any> {
    // console.log('img -->', img);
    // Guardo la img en una variable
    this.cookieService.set('img', img.get('img') as string);

    // No es necesario establecer 'Content-Type' para FormData
    return this.http.post<any>(`${this.apiUrl}/up_img`, img);
  }

  // Envio el json con correciones y obtengo el band_id
  postList(list: any): Observable<any> {
    const data = list.source._value;
    console.log('data -->', data);
    // console.log('headers -->', this.headers);

    return this.http.post<any>(`${this.apiUrl}/band_list`, data, {
      headers: this.headers,
    });
  }

  // Optengo una lista de opciones para las bandas mal escritas
  getNameOptions(name: string): Observable<any> {
    //envio el name con headers
    console.log('getNameOptions - name -->', name);
    // envuelvo el name en un objeto
    const names = { name: name };

    return this.http.post<any>(
      `${this.apiUrl}/search_options`,
      { data: name },
      { headers: this.headers }
    );
  }
}
