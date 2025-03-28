import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-step-card',
  templateUrl: './step-card.component.html',
  styleUrls: ['./step-card.component.scss']
})
export class StepCardComponent {
  @Input() title: string = ''; // Título dinámico
  @Input() parrafo: string = ''; // Párrafo dinámico
  @Input() opciones: string[] = []; // Listado de opciones dinámicas
  @Input() imageSrc: string = ''; // Fuente de la imagen
  @Input() imageAlt: string = ''; // Texto alternativo de la imagen
}
