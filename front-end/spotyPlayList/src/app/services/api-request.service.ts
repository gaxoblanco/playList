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

  headers = new HttpHeaders({
    access_token: this.authService.getToken() || '',
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
  postList(data: any): Observable<any> {
    console.log('data -->', data);
    console.log('headers -->', this.headers);

    // return this.http.post<any>(`${this.apiUrl}/band_list`, data, {
    //   headers: this.headers,
    // });
    return data;
  }
}
