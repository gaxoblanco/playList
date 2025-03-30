import { Component, ElementRef, ViewChild } from '@angular/core';
import { LanguageService } from '../services/language.service';

@Component({
  selector: 'app-workflow',
  templateUrl: './workflow.component.html',
  styleUrls: ['./workflow.component.scss']
})
export class WorkflowComponent {
  @ViewChild('audioPlayer') audioPlayer!: ElementRef<HTMLAudioElement>;
  isPlaying: boolean = false; // Variable para rastrear el estado de reproducción
  listen_step: any = {}; // Contendrá los datos según el idioma
  steps: any = {}; // Contendrá los pasos según el idioma


  constructor(private languageService: LanguageService) {}

  ngOnInit(): void {
    this.languageService.language$.subscribe((language) => {
      this.listen_step =
        language === 'en' ? this.listen_step_en[0] : this.listen_step_es[0];
      this.steps =
        language === 'en' ? this.steps_en : this.steps_es;
    });
  }

  toggleAudio(): void {
    const audio = this.audioPlayer.nativeElement;
    if (audio.paused) {
      audio.play();
      this.isPlaying = true; // Cambia el estado a "reproduciendo"
      console.log('Playing');

    } else {
      audio.pause();
      this.isPlaying = false; // Cambia el estado a "pausado"
    }
  }


  listen_step_es = [
    {title: 'Escucha cómo funciona LineUp Playlist',
    parrafo: '¡Descubre cómo LineUp Playlist te ayuda a crear la playlist perfecta para tu festival favorito!',}
  ]
  listen_step_en = [
    {title: 'Listen to how LineUp Playlist works',
    parrafo: 'Play this audio introduction to quickly understand how to use our app.',}
  ]
  steps_es = [
    {
      title: 'Captura el Line-up',
      parrafo: '¡Viste un póster de festival que te interesa! Simplemente abre la pagina web y toma una foto del banner.',
      opciones: [
        'Funciona con todo tipo de pósters y diseños de lineup',
        'Reconoce incluso tipografías artísticas y difíciles',
        'Reconoce listas de articas creadas por uno mismo'
      ],
      imageSrc: '/api/placeholder/300/180',
      imageAlt: 'Captura de pantalla mostrando la interfaz de captura de póster',
      iconRef: '📷'
    },
    {
      title: 'Revisa y Personaliza',
      parrafo: 'Identificaremos todas las bandas del póster y te mostrará una lista completa.',
      opciones: [
        'Recorta la imagen para mejorar la detección',
        'Verifica que todas las bandas se hayan detectado correctamente',
        'Agrega manualmente cualquier banda que falten',
        'Elimina artistas que no te interesen escuchar'
      ],
      imageSrc: '/api/placeholder/300/180',
      imageAlt: 'Interfaz de revisión de bandas detectadas',
      iconRef: '✏️'
    },
    {
      title: 'Crea tu Playlist',
      parrafo: 'Con un solo toque, generamos una playlist personalizada con todas las bandas seleccionadas.',
      opciones: [
        'Inclusión automática de los temas más populares de cada artista',
        'Dale un nombre personalizado a tu playlist',
        'Integración perfecta con tu plataforma de streaming favorita'
      ],
      imageSrc: '/api/placeholder/300/180',
      imageAlt: 'Proceso de creación de playlist con las bandas detectadas',
      iconRef: '🎧'
    },
    {
      title: 'Descubre y Decide',
      parrafo: 'Escucha la música, descubre nuevos artistas y decide si el festival merece la pena.',
      opciones: [
        'Marca tus artistas favoritos para destacarlos',
        'Comparte la playlist con amigos para decidir en grupo',
        'Úsala para prepararte antes del festival'
      ],
      imageSrc: '/api/placeholder/300/180',
      imageAlt: 'Reproducción de la playlist y descubrimiento de nuevos artistas',
      iconRef: '🎵'
    }
  ];
  steps_en = [
    {
      title: 'Capture the Line-up',
      parrafo: 'Spotted a festival poster that caught your eye? Simply open the web page and snap a photo of the banner.',
      opciones: [
        'Works with all types of posters and lineup designs',
        'Recognizes even artistic and complex typography',
        'Processes self-created artist lists'
      ],
      imageSrc: '/api/placeholder/300/180',
      imageAlt: 'Screenshot showing the poster capture interface',
      iconRef: '📷'
    },
    {
      title: 'Review and Customize',
      parrafo: "We'll identify all the bands from the poster and display a complete list for you.",
      opciones: [
        'Crop the image to improve detection accuracy',
        'Verify that all bands have been correctly identified',
        'Manually add any missing bands',
        "'Remove artists you're not interested in hearing"
      ],
      imageSrc: '/api/placeholder/300/180',
      imageAlt: 'Interface for reviewing detected bands',
      iconRef: '✏️'
    },
    {
      title: 'Create Your Playlist',
      parrafo: 'With just one tap, we generate a custom playlist with all your selected bands.',
      opciones: [
        "Automatic inclusion of each artist's most popular tracks",
        'Give your playlist a personalized name',
        'Seamless integration with your favorite streaming platform'
      ],
      imageSrc: '/api/placeholder/300/180',
      imageAlt: 'Process of creating a playlist with detected bands',
      iconRef: '🎧'
    },
    {
      title: 'Discover and Decide',
      parrafo: 'Listen to the music, discover new artists, and decide if the festival is worth attending.',
      opciones: [
        'Mark your favorite artists to highlight them',
        'Share the playlist with friends to decide as a group',
        'Use it to prepare before the festival'
      ],
      imageSrc: '/api/placeholder/300/180',
      imageAlt: 'Playlist playback and discovery of new artists',
      iconRef: '🎵'
    }
  ];

}
