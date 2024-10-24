

- Observables
optionListSubject y optionList$:
    optionListSubject es un BehaviorSubject que almacena la lista de opciones.
    optionList$ es el observable que expone esa lista para que los componentes puedan suscribirse y recibir las actualizaciones.

optionErrorSubject y optionError$:
    optionErrorSubject maneja los errores (o sugerencias de corrección) para las bandas.
    optionError$ expone la lista de errores para mostrarla en la UI.

bandListCorect y bandListCorect$:
    bandListCorect es un BehaviorSubject que guarda las bandas corregidas.
    bandListCorect$ expone el array de bandas corregidas para que la UI se actualice.

nextStepSubject y nextStep$:
    Maneja el flujo de pasos (como un contador de etapas) que avanza conforme los pasos del juego de corrección se completan.

showContinueButtonSubject:
    Controla cuándo mostrar el botón de "continuar" para avanzar al siguiente grupo de opciones.
