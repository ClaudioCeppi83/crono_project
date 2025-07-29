import unittest
import time
from src.model.timer_engine import TimerEngine

class TestTimerEngine(unittest.TestCase):
    """Pruebas para la clase TimerEngine."""

    def setUp(self):
        """Configura un nuevo motor de cronómetro para cada prueba."""
        self.engine = TimerEngine()

    def test_initial_state(self):
        """Verifica que el estado inicial del cronómetro sea correcto."""
        self.assertEqual(self.engine.get_current_time(), 0.0)
        self.assertFalse(self.engine.is_running)
        self.assertEqual(self.engine.laps, [])

    def test_start(self):
        """Prueba que el método start inicie el cronómetro correctamente."""
        self.engine.start()
        self.assertTrue(self.engine.is_running)

    def test_pause(self):
        """Prueba que el método pause detenga el cronómetro y conserve el tiempo."""
        self.engine.start()
        time.sleep(0.1)
        self.engine.pause()
        self.assertFalse(self.engine.is_running)
        self.assertAlmostEqual(self.engine.get_current_time(), 0.1, delta=0.05)

    def test_reset(self):
        """Prueba que el método reset reinicie el estado del cronómetro."""
        self.engine.start()
        time.sleep(0.1)
        self.engine.record_lap("Lap 1")
        self.engine.reset()

        self.assertEqual(self.engine.get_current_time(), 0.0)
        self.assertFalse(self.engine.is_running)
        self.assertEqual(self.engine.laps, [])

    def test_get_current_time(self):
        """Verifica que el tiempo se mida correctamente mientras el cronómetro corre."""
        self.engine.start()
        time.sleep(0.2)
        self.assertAlmostEqual(self.engine.get_current_time(), 0.2, delta=0.05)
        self.engine.pause()
        # El tiempo no debería cambiar mientras está en pausa
        self.assertAlmostEqual(self.engine.get_current_time(), self.engine.elapsed_time, delta=0.05)

    def test_record_lap(self):
        """Prueba que las vueltas se registren correctamente."""
        self.engine.start()
        time.sleep(0.1)
        self.engine.record_lap("Lap 1")
        self.assertEqual(len(self.engine.laps), 1)
        self.assertEqual(self.engine.laps[0][0], "Lap 1")
        self.assertAlmostEqual(self.engine.laps[0][1], 0.1, delta=0.05)

        time.sleep(0.1)
        self.engine.record_lap("Lap 2")
        self.assertEqual(len(self.engine.laps), 2)
        self.assertAlmostEqual(self.engine.laps[1][1], 0.2, delta=0.05)

if __name__ == '__main__':
    unittest.main()
