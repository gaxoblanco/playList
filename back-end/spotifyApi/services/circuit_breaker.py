import time
from spotifyApi.services.create_error_response import create_error_response


class CircuitBreaker:
    # Estados del circuit breaker
    CLOSED = "CLOSED"       # Funcionamiento normal
    OPEN = "OPEN"           # Circuito abierto, rechaza peticiones
    HALF_OPEN = "HALF_OPEN"  # Prueba si el servicio se ha recuperado

    def __init__(self, failure_threshold=5, recovery_time=60, test_requests=2):
        self.state = self.CLOSED
        self.failure_count = 0
        self.failure_threshold = failure_threshold
        self.recovery_time = recovery_time
        self.test_requests = test_requests
        self.remaining_test_requests = test_requests
        self.last_failure_time = 0

    async def execute(self, func, *args, **kwargs):
        current_time = time.time()

        # Verifica si debe transicionar de OPEN a HALF_OPEN
        if self.state == self.OPEN and current_time - self.last_failure_time > self.recovery_time:
            print("Circuit Breaker: Cambiando de OPEN a HALF_OPEN")
            self.state = self.HALF_OPEN
            self.remaining_test_requests = self.test_requests

        # Si está OPEN, rechaza inmediatamente
        if self.state == self.OPEN:
            print("Circuit Breaker: Circuito abierto, rechazando petición")
            return {
                'id': "-circuit-breaker-rejection",
                'img': "img_error",
                'genres': [],
                'name': args[2] if len(args) > 2 else "Unknown",  # artist_name
                'popularity': 0
            }

        try:
            # Intenta ejecutar la función
            result = await func(*args, **kwargs)

            # Si está en HALF_OPEN y la petición tuvo éxito
            if self.state == self.HALF_OPEN:
                self.remaining_test_requests -= 1
                if self.remaining_test_requests <= 0:
                    print("Circuit Breaker: Pruebas exitosas, cambiando a CLOSED")
                    self.state = self.CLOSED
                    self.failure_count = 0

            return result

        except Exception as e:
            # Incrementa el contador de fallos
            self.failure_count += 1
            self.last_failure_time = time.time()

            # Si excede el umbral, abre el circuito
            if self.state == self.CLOSED and self.failure_count >= self.failure_threshold:
                print(
                    f"Circuit Breaker: Demasiados fallos ({self.failure_count}), abriendo circuito")
                self.state = self.OPEN

            # Si está en HALF_OPEN, vuelve a OPEN
            elif self.state == self.HALF_OPEN:
                print("Circuit Breaker: Falló en modo prueba, volviendo a OPEN")
                self.state = self.OPEN

            # Re-lanza la excepción para que el código de backoff la maneje
            raise e
