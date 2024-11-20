import { Component, EventEmitter, Input, Output } from '@angular/core';
import { CommonModule } from '@angular/common';

@Component({
  standalone: true,
  selector: 'app-error-container',
  templateUrl: './error-container.component.html',
  styleUrls: ['./error-container.component.scss'],
  imports: [CommonModule],
})
export class ErrorContainerComponent {
  @Input() loading: string = '';
  @Input() step: number = 0;
  @Input() imgSelected: boolean = false;

  // Emisores de eventos para las funciones
  @Output() trayAgain = new EventEmitter<void>();
  @Output() trayAgainStep1 = new EventEmitter<void>();
  @Output() trayAgainStep2 = new EventEmitter<void>();

  // Método para emitir eventos desde el HTML
  emitTrayAgain(): void {
    this.trayAgain.emit();
  }

  emitTrayAgainStep1(): void {
    this.trayAgainStep1.emit();
  }

  emitTrayAgainStep2(): void {
    this.trayAgainStep2.emit();
  }
}
