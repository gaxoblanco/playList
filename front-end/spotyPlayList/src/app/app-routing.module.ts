import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthCallbackComponent } from './auth-callback/auth-callback.component';
import { UpImgComponent } from './up-img/up-img.component';

const routes: Routes = [
  { path: 'callback', component: AuthCallbackComponent },
  { path: 'create-playlist', component: UpImgComponent },
  { path: '', redirectTo: 'create-playlist', pathMatch: 'full' }, // Redirige a create-playlist por defecto
  { path: '**', redirectTo: '', pathMatch: 'full' }, // Redirige cualquier ruta desconocida al inicio
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
