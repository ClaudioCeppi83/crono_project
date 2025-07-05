import json
import os
from typing import List, Dict, Any
from datetime import datetime

class StorageService:
    """Servicio para guardar y cargar sesiones de cronómetro en archivos JSON locales."""
    def __init__(self, file_path: str = "sessions.json"):
        self.file_path = file_path

    def guardar_sesion(self, sesion: Dict[str, Any]):
        sesiones = self.obtener_sesiones()
        sesiones.append(sesion)
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(sesiones, f, ensure_ascii=False, indent=2, default=str)

    def obtener_sesiones(self) -> List[Dict[str, Any]]:
        if not os.path.exists(self.file_path):
            return []
        with open(self.file_path, "r", encoding="utf-8") as f:
            return json.load(f)

    def eliminar_sesion(self, sesion_id: str):
        sesiones = self.obtener_sesiones()
        sesiones = [s for s in sesiones if s.get("id") != sesion_id]
        with open(self.file_path, "w", encoding="utf-8") as f:
            json.dump(sesiones, f, ensure_ascii=False, indent=2)
