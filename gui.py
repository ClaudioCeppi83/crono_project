import os
import sys
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
import tkinter as tk
from tkinter import font, simpledialog, messagebox
from timer_engine import TimerEngine
from eventos import EventManager, EventMode
from storage_service import StorageService
import uuid
from datetime import datetime



class StopwatchApp:
    """Clase principal para la aplicación de cronómetro con GUI."""

    def __init__(self, root):
        """Inicializa la aplicación."""
        self.root = root
        self.root.title("Cronómetro")
        self.root.geometry("400x500")
        self.root.configure(bg="#282c34")

        self.engine = TimerEngine()
        self.event_manager = EventManager()
        self.storage = StorageService()
        self.session_id = str(uuid.uuid4())
        self.session_start = datetime.now().isoformat()
        self.session_name = None

        self._configure_styles()
        self._create_menu()
        self._create_widgets()
        self._create_history_and_save_buttons()
        self._update_timer()

        # Iniciar en modo infinito por defecto
        self.change_mode(EventMode.INFINITE)

    def _create_menu(self):
        menubar = tk.Menu(self.root)
        self.root.config(menu=menubar)

        mode_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Modo", menu=mode_menu)

        mode_menu.add_command(label="Infinito", command=lambda: self.change_mode(EventMode.INFINITE))
        mode_menu.add_command(label="Máximo de Vueltas", command=lambda: self.change_mode(EventMode.MAXIMUM))
        mode_menu.add_command(label="Nombres Predefinidos", command=lambda: self.change_mode(EventMode.PREDEFINED))

    def change_mode(self, mode):
        kwargs = {}
        if mode == EventMode.MAXIMUM:
            max_laps = simpledialog.askinteger("Máximo de Vueltas", "Introduce el número máximo de vueltas:", minvalue=1)
            if max_laps is None: return
            kwargs['max_laps'] = max_laps
        elif mode == EventMode.PREDEFINED:
            names = self._ask_predefined_names()
            if not names:
                return
            kwargs['lap_names'] = names

        self.event_manager.configure_session(mode, **kwargs)
        self.reset()
        self.update_mode_display()

    def _configure_styles(self):
        """Configura los estilos para los widgets."""
        self.time_font = font.Font(family="Consolas", size=60, weight="bold")
        self.button_font = font.Font(family="Arial", size=12)
        self.laps_font = font.Font(family="Consolas", size=14)

    def _create_widgets(self):
        """Crea y posiciona los widgets en la ventana."""
        # Frame para el tiempo
        time_frame = tk.Frame(self.root, bg="#282c34")
        time_frame.pack(pady=20)
        self.time_label = tk.Label(time_frame, text="00:00:00.000", font=self.time_font, fg="#61afef", bg="#282c34")
        self.time_label.pack()

        self.mode_label = tk.Label(time_frame, text="", font=("Arial", 12), fg="#abb2bf", bg="#282c34")
        self.mode_label.pack(pady=5)

        # Frame para los botones
        button_frame = tk.Frame(self.root, bg="#282c34")
        button_frame.pack(pady=10)

        self.start_pause_button = tk.Button(button_frame, text="Iniciar", command=self.toggle_start_pause, width=10, font=self.button_font, bg="#98c379", fg="#282c34")
        self.start_pause_button.pack(side=tk.LEFT, padx=10)

        self.lap_button = tk.Button(button_frame, text="Vuelta", command=self.record_lap, width=10, font=self.button_font, bg="#c678dd", fg="#282c34", state=tk.DISABLED)
        self.lap_button.pack(side=tk.LEFT, padx=10)

        self.reset_button = tk.Button(button_frame, text="Reiniciar", command=self.reset, width=10, font=self.button_font, bg="#e06c75", fg="#282c34", state=tk.DISABLED)
        self.reset_button.pack(side=tk.LEFT, padx=10)

        # Frame para las vueltas
        laps_frame = tk.Frame(self.root, bg="#282c34")
        laps_frame.pack(pady=20, fill=tk.BOTH, expand=True)

        self.laps_listbox = tk.Listbox(laps_frame, font=self.laps_font, bg="#3b4048", fg="#abb2bf", selectbackground="#61afef", borderwidth=0, highlightthickness=0)
        self.laps_listbox.pack(fill=tk.BOTH, expand=True, padx=20, pady=10)

        self.update_mode_display()

    def _create_history_and_save_buttons(self):
        button_frame = tk.Frame(self.root, bg="#282c34")
        button_frame.pack(pady=2)
        tk.Button(button_frame, text="Guardar sesión", command=self.save_session_prompt, bg="#61afef", fg="#23272e", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)
        tk.Button(button_frame, text="Ver historial", command=self.show_history, bg="#e5c07b", fg="#23272e", font=("Arial", 10)).pack(side=tk.LEFT, padx=5)

    def toggle_start_pause(self):
        """Inicia o pausa el cronómetro."""
        if self.engine.is_running:
            self.engine.pause()
            self.start_pause_button.config(text="Reanudar", bg="#98c379")
            self.lap_button.config(state=tk.DISABLED)
        else:
            self.engine.start()
            self.start_pause_button.config(text="Pausar", bg="#e5c07b")
            self.lap_button.config(state=tk.NORMAL)
            self.reset_button.config(state=tk.NORMAL)

    def record_lap(self):
        """Registra una vuelta."""
        if self.event_manager.can_record_lap():
            lap_name = self.event_manager.get_next_lap_name()
            self.engine.record_lap(lap_name)
            self.event_manager.advance_lap()

            self.laps_listbox.delete(0, tk.END)
            for name, lap_time in reversed(self.engine.laps):
                formatted_time = self._format_time(lap_time)
                self.laps_listbox.insert(tk.END, f" {name}: {formatted_time}")

            if not self.event_manager.can_record_lap():
                if self.event_manager.mode in (EventMode.MAXIMUM, EventMode.PREDEFINED):
                    self.lap_button.config(text="Stop", command=self.stop_at_max_laps)
                else:
                    self.lap_button.config(state=tk.DISABLED)

    def save_session_prompt(self):
        name = simpledialog.askstring("Nombre de sesión", "Introduce un nombre para la sesión:")
        if name is not None:
            if not name.strip():
                name = f"Sesión-{datetime.now().strftime('%H%M%S')}"
            # Genera un nuevo id y fecha para cada guardado manual
            self.session_id = str(uuid.uuid4())
            self.session_start = datetime.now().isoformat()
            self.session_name = name
            self.save_session()
            messagebox.showinfo("Guardado", f"Sesión guardada como: {name}")

    def save_session(self):
        session_data = {
            "id": self.session_id,
            "nombreEvento": self.session_name or f"Sesión {self.session_start[:19].replace('T',' ')}",
            "fechaInicio": self.session_start,
            "duracionTotal": self.engine.get_current_time(),
            "modoEvento": self.event_manager.mode.name if self.event_manager.mode else None,
            "registros": [
                {"nombreRegistro": name, "tiempoRegistrado": lap_time}
                for name, lap_time in self.engine.laps
            ]
        }
        self.storage.guardar_sesion(session_data)

    def reset(self):
        """Reinicia el cronómetro."""
        self.engine.reset()
        self.event_manager.reset()
        self.time_label.config(text="00:00:00.000")
        self.start_pause_button.config(text="Iniciar", bg="#98c379", state=tk.NORMAL)
        self.lap_button.config(text="Vuelta", command=self.record_lap, state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.laps_listbox.delete(0, tk.END)
        self.session_id = str(uuid.uuid4())
        self.session_start = datetime.now().isoformat()
        self.session_name = None

    def stop_at_max_laps(self):
        self.engine.pause()
        self.start_pause_button.config(text="Reanudar", bg="#98c379", state=tk.DISABLED)
        self.lap_button.config(state=tk.DISABLED)

    def _ask_predefined_names(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Nombres de Vueltas")
        dialog.geometry("300x250")
        tk.Label(dialog, text="Introduce los nombres de las vueltas, uno por línea:").pack(pady=5)
        text_area = tk.Text(dialog, height=10, width=35)
        text_area.pack(pady=5, padx=10)
        names = []

        def on_ok():
            nonlocal names
            names = [name.strip() for name in text_area.get("1.0", tk.END).split('\n') if name.strip()]
            dialog.destroy()

        ok_button = tk.Button(dialog, text="OK", command=on_ok)
        ok_button.pack(pady=10)
        dialog.transient(self.root)
        dialog.grab_set()
        self.root.wait_window(dialog)
        return names

    def update_mode_display(self):
        mode_name = self.event_manager.mode.name.replace('_', ' ').title() if self.event_manager.mode else "Infinito"
        self.mode_label.config(text=f"Modo: {mode_name}")

    def _update_timer(self):
        """Actualiza el display del tiempo cada 10ms."""
        current_time = self.engine.get_current_time()
        formatted_time = self._format_time(current_time)
        self.time_label.config(text=formatted_time)
        self.root.after(10, self._update_timer)

    def _format_time(self, seconds):
        """Formatea el tiempo en HH:MM:SS.ms."""
        minutes, seconds = divmod(seconds, 60)
        hours, minutes = divmod(minutes, 60)
        milliseconds = int((seconds - int(seconds)) * 1000)
        return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}.{milliseconds:03d}"

    def show_history(self):
        sesiones = self.storage.obtener_sesiones()
        if not sesiones:
            messagebox.showinfo("Historial", "No hay sesiones guardadas.")
            return
        hist_win = tk.Toplevel(self.root)
        hist_win.title("Historial de Sesiones")
        hist_win.geometry("400x400")
        listbox = tk.Listbox(hist_win, font=("Consolas", 12))
        listbox.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        for sesion in sesiones:
            nombre = sesion.get("nombreEvento", "Sin nombre")
            fecha = sesion.get("fechaInicio", "")
            dur = sesion.get("duracionTotal", 0)
            listbox.insert(tk.END, f"{nombre} | {fecha[:19].replace('T',' ')} | {dur:.2f}s")

if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()
