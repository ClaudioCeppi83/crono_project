import tkinter as tk
from datetime import datetime
import uuid

from ..model.timer_engine import TimerEngine
from ..model.event_manager import EventManager, EventMode
from ..model.storage_service import StorageService
from ..view.main_window import MainWindow
from ..view.history_window import HistoryWindow
from ..view.dialogs import Dialogs

class AppController:
    """Controlador principal que conecta el modelo y la vista."""

    def __init__(self, root):
        self.root = root
        self.engine = TimerEngine()
        self.event_manager = EventManager()
        self.storage = StorageService()
        self.view = MainWindow(root, self)

        self._reset_session()
        self.change_mode(EventMode.INFINITE)
        self._update_timer()

    def _reset_session(self):
        self.session_id = str(uuid.uuid4())
        self.session_start = datetime.now().isoformat()
        self.session_name = None

    def toggle_start_pause(self):
        if self.engine.is_running:
            self.engine.pause()
            self.view.set_start_pause_button("Start", "#39FF14", "#000000")
        else:
            self.engine.start()
            self.view.set_start_pause_button("Pause", "#FF4136", "#FFFFFF")
        
        self.view.set_lap_button_state(tk.NORMAL if self.engine.is_running else tk.DISABLED)
        self.view.set_reset_button_state(tk.NORMAL)

    def record_lap(self):
        if not self.event_manager.can_record_lap():
            Dialogs.show_warning("Lap Limit", "The maximum number of laps has been reached.")
            return

        lap_time_float = self.engine.get_current_time()
        time_str, ms_str = self._format_time(lap_time_float)
        lap_time_str = f"{time_str}.{ms_str}"

        self.event_manager.record_lap(lap_time_str)
        self.view.update_lap_display(self.event_manager.get_laps())

        if not self.event_manager.can_record_lap():
            self.view.lap_button.config(text="Stop", command=self.toggle_start_pause)

    def reset(self):
        self.engine.reset()
        self.event_manager.reset_laps()
        self.view.update_lap_display([])
        self.view.set_start_pause_button("Start", "#39FF14", "#000000")
        self.view.lap_button.config(text="Lap", command=self.record_lap)
        self.view.set_lap_button_state(tk.DISABLED)
        self.view.set_reset_button_state(tk.DISABLED)
        self.view.update_time_display("00:00:00", "00")
        self._reset_session()

    def change_mode(self, mode):
        if self.view.side_menu_visible:
            self.view.toggle_side_menu()

        kwargs = {}
        if mode == EventMode.MAXIMUM:
            max_laps = Dialogs.ask_max_laps(self.root)
            if max_laps is None: return
            kwargs['max_laps'] = max_laps
        elif mode == EventMode.PREDEFINED:
            names = Dialogs.ask_predefined_names(self.root)
            if not names: return
            kwargs['lap_names'] = names

        self.event_manager.configure_session(mode, **kwargs)
        self.reset()
        mode_name = self.event_manager.get_mode_name().replace('_', ' ').title()
        self.view.set_mode_display(mode_name)

    def save_session_prompt(self):
        if self.view.side_menu_visible:
            self.view.toggle_side_menu()
        session_name = Dialogs.ask_session_name(self.root)
        if session_name is None: return
        self.save_session(session_name)

    def save_session(self, session_name):
        if not session_name:
            session_name = f"Session {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}"
        
        self.session_name = session_name
        session_data = {
            "session_id": self.session_id,
            "session_name": self.session_name,
            "start_time": self.session_start,
            "end_time": datetime.now().isoformat(),
            "mode": self.event_manager.get_mode_name(),
            "laps": [{ "name": name, "time": time } for name, time in self.event_manager.get_laps()]
        }
        self.storage.guardar_sesion(session_data)
        Dialogs.show_info("Session Saved", f"Session '{session_name}' has been saved.")

    def show_history(self):
        if self.view.side_menu_visible:
            self.view.toggle_side_menu()
        sessions = self.storage.obtener_sesiones()
        HistoryWindow(self.root, sessions)

    def _update_timer(self):
        if self.engine.is_running:
            elapsed_time = self.engine.get_current_time()
            time_str, ms_str = self._format_time(elapsed_time)
            self.view.update_time_display(time_str, ms_str)
        self.root.after(10, self._update_timer)

    def _format_time(self, time_float):
        total_seconds = int(time_float)
        milliseconds = int((time_float - total_seconds) * 100)
        minutes, seconds = divmod(total_seconds, 60)
        hours, minutes = divmod(minutes, 60)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}", f"{milliseconds:02d}"
