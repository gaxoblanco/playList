import { NgModule } from '@angular/core';
import { CommonModule } from '@angular/common';
import { Component } from '@angular/core';
import { MatCardModule } from '@angular/material/card';
import {
  MatChipEditedEvent,
  MatChipInputEvent,
  MatChipsModule,
} from '@angular/material/chips';
import { LoadingModel } from '../models/loading';
import { MatIconModule } from '@angular/material/icon';
import { LiveAnnouncer } from '@angular/cdk/a11y';

@Component({
  selector: 'app-up-img',
  templateUrl: './up-img.component.html',
  styleUrls: ['./up-img.component.scss'],
  standalone: true,
  imports: [MatCardModule, MatChipsModule, MatIconModule, CommonModule],
})
export class UpImgComponent {
  selectedFile: File | null = null;

  loading: LoadingModel = 'up';
  optionList = [
    { id: 1, name: 'Option 1' },
    { id: 2, name: 'Option 2' },
    { id: 3, name: 'Option 3' },
  ];
  selectedList: number = 0;
  announcer: LiveAnnouncer | undefined;

  onFileSelected(event: Event): void {
    const input = event.target as HTMLInputElement;
    if (input.files && input.files.length > 0) {
      this.selectedFile = input.files[0];
    }
    this.loading = 'loading';
    try {
      // espero la respuesta del servidor si es correcto
      console.log('Archivo seleccionado:', this.selectedFile);
      // Logica para enviar la img a la API-IA
      //----------------------------------------------------------------
      this.loading = 'loaded'; // habitilo el button para seguir
      //
    } catch (error) {
      console.log('Error: ', error);
    }
  }

  uploadImage(): void {
    if (this.selectedFile) {
      console.log('Archivo seleccionado:', this.selectedFile);
      // Aquí puedes implementar la lógica para subir la imagen a tu API
    } else {
      console.log('No se ha seleccionado ninguna imagen');
    }
  }
  //----------------------------------------------------------------
  add(event: MatChipInputEvent): void {
    const value = (event.value || '').trim();

    // Add our fruit
    if (value) {
      // this.optionList = [...this.optionList, { name: value }];
    }

    // Clear the input value
    event.chipInput!.clear();
  }

  remove(fruit: any): void {
    const index = this.optionList.indexOf(fruit);
    if (index >= 0) {
      this.optionList.splice(index, 1);
      if (this.announcer) {
        this.announcer.announce(`Removed ${fruit.name}`);
      }
    }
  }

  edit(option: any, event: MatChipEditedEvent) {
    const value = event.value.trim();

    // Remove option if it no longer has a name
    if (!value) {
      this.remove(option);
      return;
    }

    // Remove option if it no longer has a name
    if (!value) {
      this.remove(option);
      return;
    }

    // Edit existing option
    this.optionList = this.optionList.map((item: any) => {
      if (item === option) {
        return { ...item, name: value };
      }
      return item;
    });
  }
}
