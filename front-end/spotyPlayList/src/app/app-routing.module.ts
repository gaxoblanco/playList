import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';
import { AuthCallbackComponent } from './auth-callback/auth-callback.component';
import { UpImgComponent } from './up-img/up-img.component';
import { WorkflowComponent } from './workflow/workflow.component';

const routes: Routes = [
  { path: '',  component: WorkflowComponent},
  { path: 'callback', component: AuthCallbackComponent },
  {
    path: 'create-playlist',
    component: UpImgComponent,
  },
];

@NgModule({
  imports: [RouterModule.forRoot(routes)],
  exports: [RouterModule],
})
export class AppRoutingModule {}
