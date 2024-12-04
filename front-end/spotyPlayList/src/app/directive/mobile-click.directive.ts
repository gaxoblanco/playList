// mobile-click.directive.ts
import { Directive, HostListener, Input } from '@angular/core';

@Directive({
  standalone: true,
  selector: '[appMobileClick]',
})
export class MobileClickDirective {
  @Input() appMobileClick!: () => void;

  @HostListener('click', ['$event'])
  onClick(event: Event) {
    if (window.innerWidth <= 960) {
      // Puedes ajustar el tamaño según tus necesidades
      this.appMobileClick();
    }
  }
}
