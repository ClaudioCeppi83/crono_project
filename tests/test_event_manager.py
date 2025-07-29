import unittest
from src.model.event_manager import EventManager, EventMode

class TestEventManager(unittest.TestCase):
    """Pruebas para la clase EventManager."""

    def setUp(self):
        """Configura un nuevo gestor de eventos para cada prueba."""
        self.manager = EventManager()

    def test_initial_state(self):
        """Verifica el estado inicial del gestor de eventos."""
        self.assertIsNone(self.manager.mode)
        self.assertEqual(self.manager.laps, [])
        self.assertEqual(self.manager.next_lap_index, 0)

    def test_configure_infinite_mode(self):
        """Prueba la configuración del modo Infinito."""
        self.manager.configure_session(EventMode.INFINITE)
        self.assertEqual(self.manager.mode, EventMode.INFINITE)
        self.assertTrue(self.manager.can_record_lap())
        self.assertEqual(self.manager.get_next_lap_name(), "Lap 1")

    def test_configure_max_laps_mode(self):
        """Prueba la configuración del modo Máximo de Vueltas."""
        self.manager.configure_session(EventMode.MAXIMUM, max_laps=3)
        self.assertEqual(self.manager.mode, EventMode.MAXIMUM)
        self.assertEqual(self.manager.max_laps, 3)
        self.assertTrue(self.manager.can_record_lap())

    def test_configure_predefined_mode(self):
        """Prueba la configuración del modo Nombres Predefinidos."""
        lap_names = ["Start", "Middle", "End"]
        self.manager.configure_session(EventMode.PREDEFINED, lap_names=lap_names)
        self.assertEqual(self.manager.mode, EventMode.PREDEFINED)
        self.assertEqual(self.manager.lap_names, lap_names)
        self.assertEqual(self.manager.get_next_lap_name(), "Start")

    def test_lap_recording_and_limits(self):
        """Verifica la lógica de grabación de vueltas y sus límites."""
        # Modo Máximo de Vueltas
        self.manager.configure_session(EventMode.MAXIMUM, max_laps=2)
        self.manager.record_lap("00:01.00")
        self.assertTrue(self.manager.can_record_lap())
        self.manager.record_lap("00:02.00")
        self.assertFalse(self.manager.can_record_lap())
        self.assertEqual(len(self.manager.get_laps()), 2)

        # Modo Nombres Predefinidos
        self.manager.reset_laps()
        lap_names = ["First", "Second"]
        self.manager.configure_session(EventMode.PREDEFINED, lap_names=lap_names)
        self.manager.record_lap("00:03.00")
        self.assertEqual(self.manager.get_laps()[0][0], "First")
        self.assertTrue(self.manager.can_record_lap())
        self.manager.record_lap("00:04.00")
        self.assertEqual(self.manager.get_laps()[1][0], "Second")
        self.assertFalse(self.manager.can_record_lap())

    def test_reset_laps(self):
        """Prueba que el reseteo de vueltas funcione correctamente."""
        self.manager.configure_session(EventMode.INFINITE)
        self.manager.record_lap("00:01.00")
        self.manager.reset_laps()
        self.assertEqual(self.manager.laps, [])
        self.assertEqual(self.manager.next_lap_index, 0)

if __name__ == '__main__':
    unittest.main()
