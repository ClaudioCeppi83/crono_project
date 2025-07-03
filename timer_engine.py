import time
from typing import List, Tuple

class TimerEngine:
    """Gestiona la lógica de un cronómetro secuencial de alta precisión.

    Esta clase encapsula el estado y las operaciones de un cronómetro,
    incluyendo inicio, pausa, registro de vueltas y reseteo. Está diseñada
    para ser un componente de lógica pura, sin dependencias de UI.
    """

    def __init__(self):
        """Inicializa una nueva instancia de TimerEngine."""
        self.elapsed_time: float = 0.0
        self.is_running: bool = False
        self.laps: List[Tuple[str, float]] = []  # Cambia a lista de tuplas (nombre, tiempo)
        self._start_time: float | None = None

    def start(self) -> None:
        """Inicia o reanuda el cronómetro.

        Si el cronómetro no está en funcionamiento, lo inicia, registrando
        el tiempo de inicio.
        """
        if not self.is_running:
            self.is_running = True
            self._start_time = time.perf_counter()

    def pause(self) -> None:
        """Pausa el cronómetro.

        Si el cronómetro está en funcionamiento, detiene la cuenta y acumula
        el tiempo transcurrido.
        """
        if self.is_running:
            self.elapsed_time += time.perf_counter() - self._start_time
            self.is_running = False

    def record_lap(self, name: str) -> None:
        """Registra una vuelta (lap) con nombre.

        Si el cronómetro está en marcha, añade el nombre y el tiempo actual a la lista de vueltas.
        """
        if self.is_running:
            lap_time = self.get_current_time()
            self.laps.append((name, lap_time))

    def reset(self) -> None:
        """Resetea el cronómetro a su estado inicial.

        Detiene el cronómetro y reinicia todos los contadores y registros.
        """
        self.elapsed_time = 0.0
        self.is_running = False
        self.laps = []
        self._start_time = None

    def get_current_time(self) -> float:
        """Obtiene el tiempo transcurrido actual del cronómetro.

        Returns:
            float: El tiempo total transcurrido en segundos.
                     Si el cronómetro está en marcha, incluye el tiempo desde
                     el último inicio. Si está pausado, devuelve el tiempo
                     acumulado hasta la pausa.
        """
        if self.is_running and self._start_time is not None:
            return self.elapsed_time + (time.perf_counter() - self._start_time)
        return self.elapsed_time