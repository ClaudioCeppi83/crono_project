import unittest
import time
from unittest.mock import patch
from timer_engine import TimerEngine

class TestTimerEngine(unittest.TestCase):
    """Pruebas unitarias para la clase TimerEngine."""

    def setUp(self):
        """Configura un nuevo motor de cronómetro para cada prueba."""
        self.engine = TimerEngine()

    def test_initial_state(self):
        """Verifica que el estado inicial del cronómetro sea correcto."""
        self.assertEqual(self.engine.elapsed_time, 0.0)
        self.assertFalse(self.engine.is_running)
        self.assertEqual(self.engine.laps, [])
        self.assertIsNone(self.engine._start_time)
        self.assertEqual(self.engine.get_current_time(), 0.0)

    def test_start(self):
        """Prueba la funcionalidad de inicio del cronómetro."""
        self.engine.start()
        self.assertTrue(self.engine.is_running)
        self.assertIsNotNone(self.engine._start_time)

    def test_start_when_already_running(self):
        """Prueba que start() no hace nada si ya está corriendo."""
        self.engine.start()
        start_time_1 = self.engine._start_time
        self.engine.start() # Segundo llamado
        self.assertEqual(self.engine._start_time, start_time_1)

    @patch('time.perf_counter')
    def test_pause(self, mock_perf_counter):
        """Prueba la funcionalidad de pausa del cronómetro."""
        mock_perf_counter.side_effect = [10.0, 12.5] # Inicio, Pausa
        self.engine.start()
        self.engine.pause()
        self.assertFalse(self.engine.is_running)
        self.assertAlmostEqual(self.engine.elapsed_time, 2.5)
        self.assertAlmostEqual(self.engine.get_current_time(), 2.5)

    def test_pause_when_not_running(self):
        """Prueba que pause() no hace nada si no está corriendo."""
        initial_elapsed_time = self.engine.elapsed_time
        self.engine.pause()
        self.assertEqual(self.engine.elapsed_time, initial_elapsed_time)

    @patch('time.perf_counter')
    def test_get_current_time_while_running(self, mock_perf_counter):
        """Prueba que get_current_time() funciona mientras corre."""
        mock_perf_counter.side_effect = [100.0, 102.0, 105.0] # start, get_time, get_time
        self.engine.start()
        self.assertAlmostEqual(self.engine.get_current_time(), 2.0)
        self.assertAlmostEqual(self.engine.get_current_time(), 5.0)

    @patch('time.perf_counter')
    def test_record_lap_while_running(self, mock_perf_counter):
        """Prueba el registro de vueltas."""
        mock_perf_counter.side_effect = [0.0, 1.5, 3.0] # start, lap1, lap2
        self.engine.start()
        self.engine.record_lap()
        self.engine.record_lap()
        self.assertEqual(len(self.engine.laps), 2)
        self.assertAlmostEqual(self.engine.laps[0], 1.5)
        self.assertAlmostEqual(self.engine.laps[1], 3.0)

    def test_record_lap_when_not_running(self):
        """Prueba que no se registran vueltas si no está corriendo."""
        self.engine.record_lap()
        self.assertEqual(self.engine.laps, [])

    def test_reset(self):
        """Prueba la funcionalidad de reseteo."""
        self.engine.start()
        time.sleep(0.1)
        self.engine.pause()
        self.engine.record_lap() # No debería añadir nada
        self.engine.reset()
        self.test_initial_state() # Debería volver al estado inicial

    @patch('time.perf_counter')
    def test_full_cycle(self, mock_perf_counter):
        """Prueba un ciclo completo de uso: start -> pause -> start -> lap -> reset."""
        mock_perf_counter.side_effect = [
            10.0, # start
            11.5, # pause
            13.0, # resume (start)
            14.0, # record_lap
            15.0  # get_current_time after lap
        ]
        # 1. Start
        self.engine.start()
        # 2. Pause after 1.5s
        self.engine.pause()
        self.assertFalse(self.engine.is_running)
        self.assertAlmostEqual(self.engine.get_current_time(), 1.5)
        # 3. Resume
        self.engine.start()
        self.assertTrue(self.engine.is_running)
        # 4. Record lap after 1s more (total 2.5s)
        self.engine.record_lap()
        self.assertEqual(len(self.engine.laps), 1)
        self.assertAlmostEqual(self.engine.laps[0], 2.5) # 1.5 (paused) + 1.0 (running)
        # 5. Check current time
        self.assertAlmostEqual(self.engine.get_current_time(), 3.5) # 1.5 + 2.0
        # 6. Reset
        self.engine.reset()
        self.test_initial_state()

if __name__ == '__main__':
    unittest.main()