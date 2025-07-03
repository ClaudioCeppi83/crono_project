import tkinter as tk
from tkinter import font, messagebox
from timer_engine import TimerEngine
from event_manager import EventManager, EventMode

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
        self._configure_styles()
        self._create_widgets()
        self._update_timer()

    def _configure_styles(self):
        """Configura los estilos para los widgets."""
        self.time_font = font.Font(family="Consolas", size=60, weight="bold")
        self.button_font = font.Font(family="Arial", size=12)
        self.laps_font = font.Font(family="Consolas", size=14)

    def _create_widgets(self):
        """Crea y posiciona los widgets en la ventana."""
        # Panel de configuración superior
        self.config_frame = tk.Frame(self.root, bg="#23272e", pady=8)
        self.config_frame.pack(fill=tk.X)
        tk.Label(self.config_frame, text="Modo:", fg="#abb2bf", bg="#23272e", font=("Arial", 11)).pack(side=tk.LEFT, padx=5)
        self.mode_var = tk.StringVar(value="INFINITE")
        modes = [
            ("Infinito", "INFINITE"),
            ("Predefinido", "PREDEFINED"),
            ("Máximo", "MAXIMUM")
        ]
        for text, value in modes:
            tk.Radiobutton(self.config_frame, text=text, variable=self.mode_var, value=value, fg="#abb2bf", bg="#23272e", selectcolor="#3b4048", font=("Arial", 10), command=self._on_mode_change).pack(side=tk.LEFT, padx=2)
        # Área dinámica para nombres o máximo
        self.dynamic_config = tk.Frame(self.config_frame, bg="#23272e")
        self.dynamic_config.pack(side=tk.LEFT, padx=10)
        self.lap_names = []
        self.max_laps_var = tk.IntVar(value=5)
        self._update_dynamic_config()
        # Botón aplicar configuración
        tk.Button(self.config_frame, text="Aplicar", command=self._apply_config, bg="#61afef", fg="#23272e", font=("Arial", 10)).pack(side=tk.LEFT, padx=10)

        # Frame para el tiempo
        time_frame = tk.Frame(self.root, bg="#282c34")
        time_frame.pack(pady=20)
        self.time_label = tk.Label(time_frame, text="00:00:00.000", font=self.time_font, fg="#61afef", bg="#282c34")
        self.time_label.pack()

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

    def _on_mode_change(self):
        self.lap_names = []
        self.max_laps_var.set(5)
        self._update_dynamic_config()

    def _update_dynamic_config(self):
        for widget in self.dynamic_config.winfo_children():
            widget.destroy()
        mode = self.mode_var.get()
        if mode == "PREDEFINED":
            tk.Label(self.dynamic_config, text="Nombres de vueltas:", fg="#abb2bf", bg="#23272e").pack(anchor=tk.W)
            self.lap_entry = tk.Entry(self.dynamic_config)
            self.lap_entry.pack(anchor=tk.W, pady=2)
            tk.Button(self.dynamic_config, text="Agregar", command=self._add_lap_name, bg="#98c379", fg="#23272e").pack(anchor=tk.W, pady=2)
            self.lap_listbox = tk.Listbox(self.dynamic_config, height=3)
            self.lap_listbox.pack(fill=tk.X, pady=2)
        elif mode == "MAXIMUM":
            tk.Label(self.dynamic_config, text="Máximo de vueltas:", fg="#abb2bf", bg="#23272e").pack(anchor=tk.W)
            tk.Entry(self.dynamic_config, textvariable=self.max_laps_var, width=5).pack(anchor=tk.W, pady=2)
        # Infinito no requiere campos adicionales

    def _add_lap_name(self):
        name = self.lap_entry.get().strip()
        if name:
            self.lap_names.append(name)
            self.lap_listbox.insert(tk.END, name)
            self.lap_entry.delete(0, tk.END)

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
        """Registra una vuelta con nombre según el modo de evento."""
        if self.event_manager.can_record_lap():
            lap_name = self.event_manager.get_next_lap_name()
            self.engine.record_lap(lap_name)
            self.event_manager.advance_lap()
            self._update_laps_listbox()
            # Deshabilita el botón si ya no se pueden registrar más vueltas
            if not self.event_manager.can_record_lap():
                self.lap_button.config(state=tk.DISABLED)

    def _update_laps_listbox(self):
        self.laps_listbox.delete(0, tk.END)
        for i, (lap_name, lap_time) in enumerate(reversed(self.engine.laps)):
            formatted_time = self._format_time(lap_time)
            self.laps_listbox.insert(tk.END, f"{lap_name}: {formatted_time}")

    def reset(self):
        """Reinicia el cronómetro."""
        self.engine.reset()
        self.time_label.config(text="00:00:00.000")
        self.start_pause_button.config(text="Iniciar", bg="#98c379")
        self.lap_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)
        self.laps_listbox.delete(0, tk.END)
        self.event_manager.next_lap_index = 0

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

    def _apply_config(self):
        mode = self.mode_var.get()
        if mode == "PREDEFINED" and not self.lap_names:
            messagebox.showwarning("Faltan nombres", "Agrega al menos un nombre de vuelta.")
            return
        if mode == "MAXIMUM" and self.max_laps_var.get() <= 0:
            messagebox.showwarning("Valor inválido", "El máximo debe ser mayor que cero.")
            return
        if mode == "INFINITE":
            self.event_manager.configure_session(EventMode.INFINITE)
        elif mode == "PREDEFINED":
            self.event_manager.configure_session(EventMode.PREDEFINED, lap_names=self.lap_names)
        elif mode == "MAXIMUM":
            self.event_manager.configure_session(EventMode.MAXIMUM, max_laps=self.max_laps_var.get())
        self.engine.reset()
        self._update_laps_listbox()
        self.time_label.config(text="00:00:00.000")
        self.start_pause_button.config(text="Iniciar", bg="#98c379")
        self.lap_button.config(state=tk.DISABLED)
        self.reset_button.config(state=tk.DISABLED)

if __name__ == "__main__":
    root = tk.Tk()
    app = StopwatchApp(root)
    root.mainloop()