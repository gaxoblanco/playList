import { NgModule, CUSTOM_ELEMENTS_SCHEMA } from '@angular/core';
import { BrowserModule } from '@angular/platform-browser';
import { HttpClientModule, HTTP_INTERCEPTORS } from '@angular/common/http';
import { AppRoutingModule } from './app-routing.module';
import { AppComponent } from './app.component';
import { AuthCallbackComponent } from './auth-callback/auth-callback.component';
import { AuthInterceptor } from './interceptors/auth.interceptor';
import { AuthService } from './services/auth.service';
import { RouterModule } from '@angular/router';
import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { MatCardModule } from '@angular/material/card';
import { MatButtonModule } from '@angular/material/button';
import { MatInputModule } from '@angular/material/input';
import { UpImgComponent } from './up-img/up-img.component';
import { MatChipsModule } from '@angular/material/chips';

import { MatIconModule } from '@angular/material/icon';
import { OptionsListComponent } from './molecule/options-list/options-list.component';
import { CardBandComponent } from './organisms/card-band/card-band.component';
@NgModule({
  declarations: [AppComponent, AuthCallbackComponent],
  imports: [
    BrowserModule,
    HttpClientModule,
    RouterModule.forRoot([]),
    BrowserAnimationsModule,
    MatCardModule,
    MatButtonModule,
    MatInputModule,
    MatChipsModule,
    MatIconModule,
    RouterModule.forRoot([]),
    AppRoutingModule,
    UpImgComponent,
    CardBandComponent,
    OptionsListComponent,
  ],
  providers: [
    AuthService, // Añadir el servicio de autenticación como proveedor
    {
      provide: HTTP_INTERCEPTORS, // Configurar el interceptor
      useClass: AuthInterceptor,
      multi: true, // Esto permite agregar múltiples interceptores si es necesario
    },
  ],
  bootstrap: [AppComponent],
})
export class AppModule {}
