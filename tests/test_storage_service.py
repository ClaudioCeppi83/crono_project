import unittest
import os
import json
from src.model.storage_service import StorageService

class TestStorageService(unittest.TestCase):
    """Pruebas para la clase StorageService."""

    def setUp(self):
        """Configura un servicio de almacenamiento con un archivo de prueba."""
        self.test_file = "test_sessions.json"
        self.storage = StorageService(file_path=self.test_file)
        # Asegurarse de que el archivo de prueba no exista al empezar
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def tearDown(self):
        """Limpia el archivo de prueba después de cada prueba."""
        if os.path.exists(self.test_file):
            os.remove(self.test_file)

    def test_guardar_y_obtener_sesiones(self):
        """Prueba que las sesiones se guarden y se obtengan correctamente."""
        sesion1 = {"session_id": "1", "data": "test1"}
        sesion2 = {"session_id": "2", "data": "test2"}

        self.storage.guardar_sesion(sesion1)
        self.storage.guardar_sesion(sesion2)

        sesiones = self.storage.obtener_sesiones()
        self.assertEqual(len(sesiones), 2)
        self.assertEqual(sesiones[0]["data"], "test1")
        self.assertEqual(sesiones[1]["data"], "test2")

    def test_eliminar_sesion(self):
        """Prueba que una sesión se elimine correctamente."""
        sesiones_iniciales = [
            {"session_id": "1", "data": "test1"},
            {"session_id": "2", "data": "test2"},
            {"session_id": "3", "data": "test3"}
        ]
        with open(self.test_file, 'w') as f:
            json.dump(sesiones_iniciales, f)

        self.storage.eliminar_sesion("2")
        sesiones = self.storage.obtener_sesiones()
        self.assertEqual(len(sesiones), 2)
        self.assertEqual([s["session_id"] for s in sesiones], ["1", "3"])

    def test_obtener_sesiones_archivo_no_existente(self):
        """Prueba que se devuelva una lista vacía si el archivo no existe."""
        sesiones = self.storage.obtener_sesiones()
        self.assertEqual(sesiones, [])

    def test_manejo_archivo_vacio(self):
        """Prueba que el servicio maneje correctamente un archivo JSON vacío."""
        # Crear un archivo vacío
        open(self.test_file, 'w').close()
        sesiones = self.storage.obtener_sesiones()
        self.assertEqual(sesiones, [])

if __name__ == '__main__':
    unittest.main()
