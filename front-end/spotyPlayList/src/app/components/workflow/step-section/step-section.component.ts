import { Component, Input } from '@angular/core';

@Component({
  selector: 'app-step-section',
  templateUrl: './step-section.component.html',
  styleUrls: ['./step-section.component.scss']
})
export class StepSectionComponent {
  @Input() title: string = ''; // Título dinámico
  @Input() parrafo: string = ''; // Párrafo dinámico
  @Input() opciones: string[] = []; // Listado de opciones dinámicas
  @Input() imageSrc: string = ''; // Fuente de la imagen
  @Input() imageAlt: string = ''; // Texto alternativo de la imagen
  @Input() iconRef: string = ''; // Referencia para el ícono
  @Input() isOdd: boolean = false; // Bandera para alternar estilos
}
