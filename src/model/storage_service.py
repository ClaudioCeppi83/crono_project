import json
import os
from typing import List, Dict, Any

class StorageService:
    """Servicio para guardar y cargar sesiones de cronómetro en archivos JSON locales."""
    def __init__(self, file_path: str = "sessions.json"):
        self.file_path = file_path

    def guardar_sesion(self, sesion: Dict[str, Any]):
        """Guarda una sesión, actualizándola si ya existe."""
        sesiones = self.obtener_sesiones()
        # Filtrar la sesión antigua si existe
        sesiones = [s for s in sesiones if s.get("session_id") != sesion.get("session_id")]
        sesiones.append(sesion)
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(sesiones, f, ensure_ascii=False, indent=4, default=str)
        except IOError as e:
            print(f"Error al guardar el archivo de sesiones: {e}")

    def obtener_sesiones(self) -> List[Dict[str, Any]]:
        """Obtiene todas las sesiones, manejando errores y archivos vacíos."""
        if not os.path.exists(self.file_path):
            return []
        try:
            # Comprobar si el archivo está vacío para evitar errores de decodificación
            if os.path.getsize(self.file_path) == 0:
                return []
            with open(self.file_path, "r", encoding="utf-8") as f:
                return json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error al leer o decodificar el archivo de sesiones: {e}")
            return []

    def eliminar_sesion(self, sesion_id: str):
        """Elimina una sesión por su ID."""
        sesiones = self.obtener_sesiones()
        sesiones_filtradas = [s for s in sesiones if s.get("session_id") != sesion_id]
        try:
            with open(self.file_path, "w", encoding="utf-8") as f:
                json.dump(sesiones_filtradas, f, ensure_ascii=False, indent=4, default=str)
        except IOError as e:
            print(f"Error al guardar el archivo de sesiones después de eliminar: {e}")